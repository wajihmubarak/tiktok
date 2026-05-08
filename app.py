from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp
import os

app = Flask(__name__)
CORS(app)  # عشان يسمح للـ HTML يتصل بالبايثون بدون مشاكل أمنية

@app.route('/download', methods=['POST'])
def download_api():
    try:
        # استلام البيانات القادمة من الواجهة
        content = request.json
        video_url = content.get('url')

        if not video_url:
            return jsonify({"status": "error", "message": "الرابط مفقود"}), 400

        # إعدادات مكتبة yt-dlp لسحب الفيديو بأفضل جودة
        ydl_opts = {
            'format': 'best',
            'quiet': True,
            'no_warnings': True,
            'nocheckcertificate': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # استخراج المعلومات بدون تحميل الفيديو على السيرفر (لتوفير المساحة)
            info = ydl.extract_info(video_url, download=False)
            
            # الحصول على رابط الفيديو المباشر ومعلومات إضافية
            direct_link = info.get('url')
            title = info.get('title', 'TikTok Video')
            thumbnail = info.get('thumbnail')

            return jsonify({
                "status": "success",
                "download_link": direct_link,
                "title": title,
                "thumbnail": thumbnail
            })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    # تشغيل السيرفر على بورت 5000
    app.run(host='0.0.0.0', port=5000, debug=True)
