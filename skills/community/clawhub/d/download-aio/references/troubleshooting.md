# Troubleshooting - Download AIO

## Lỗi thường gặp

### ERROR: No module named yt_dlp
```
Nguyên nhân: yt-dlp chưa cài hoặc sai Python path
Fix: C:\Users\PCM\AppData\Local\Programs\Python\Python311\python.exe -m pip install yt-dlp
```

### ERROR: Requested format not available
```
Nguyên nhân: Format/quality không tồn tại cho video này
Fix: Chạy -F để xem format có sẵn, chọn format ID phù hợp
     Hoặc dùng: -f "best"
```

### ERROR: Unable to download webpage (HTTP 429)
```
Nguyên nhân: Bị rate limit
Fix: Thêm --sleep-interval 3 --max-sleep-interval 8
     Hoặc dùng --cookies-from-browser chrome
```

### ERROR: Sign in to confirm you're not a bot
```
Nguyên nhân: YouTube bot detection
Fix: --cookies-from-browser chrome
     Đảm bảo Chrome đang mở và đã đăng nhập YouTube
```

### ERROR: Private video / Login required
```
Fix: --cookies-from-browser chrome
     Hoặc export cookies: xem references/auth.md
```

### ERROR: ffmpeg not found (khi merge video+audio)
```
Nguyên nhân: ffmpeg chưa cài
Fix 1: choco install ffmpeg
Fix 2: Dùng format không cần merge: -f "best[ext=mp4]"
```

### Video tải về nhưng không có tiếng
```
Nguyên nhân: Tải sai format (video-only)
Fix: Dùng format string đúng:
     -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"
```

### TikTok có watermark
```
Fix: Thêm flag (tùy phiên bản yt-dlp):
     Một số phiên bản tự động lấy no-watermark version
     Nếu không: dùng --format "download_addr-2" nếu có trong -F
```

### Instagram: só thể tải public content
```
Private account hoặc story đã hết hạn sẽ báo lỗi
Fix: --cookies-from-browser chrome (nếu đã follow account đó)
```

## Update yt-dlp

```powershell
C:\Users\PCM\AppData\Local\Programs\Python\Python311\python.exe -m pip install -U yt-dlp
```

Nên update thường xuyên vì các nền tảng hay thay đổi.
