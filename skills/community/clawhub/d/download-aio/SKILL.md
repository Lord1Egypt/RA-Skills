---
name: download-aio
description: Download videos, audio, playlists, subtitles, and thumbnails from ANY platform (YouTube, TikTok, Instagram, Facebook, Twitter/X, Twitch, Vimeo, SoundCloud, Reddit, and 1000+ more) using yt-dlp. After download, automatically send file to Telegram if under 50MB. Use this skill when the user wants to download video, audio, playlist, reel, short, clip, subtitle, or thumbnail from any website or social media platform. Triggers on phrases like "tải video", "download video", "tải nhạc", "download audio", "tải playlist", "download từ YouTube/TikTok/Facebook/Instagram", "lưu video", "save video", or when user pastes a URL from a video platform.
---

# Download AIO Skill

Tải video, audio, playlist, subtitle, thumbnail từ 1000+ nền tảng bằng yt-dlp. Sau khi tải tự động gửi file về Telegram nếu dung lượng <= 50MB.

## Cài đặt (chạy lần đầu)

Trước khi dùng, chạy script cài đặt để kiểm tra và cài đầy đủ dependencies:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/install.ps1
```

Script sẽ tự động:
1. Kiểm tra Python → hướng dẫn cài nếu thiếu
2. Cài yt-dlp
3. Kiểm tra ffmpeg → cài qua Chocolatey nếu thiếu
4. Tạo thư mục Downloads mặc định
5. Verify toàn bộ setup

## Cách dùng (User Guide)

### Cách đơn giản nhất
Chỉ cần paste URL vào chat là xong:
```
https://www.youtube.com/watch?v=...
https://www.tiktok.com/@user/video/...
https://www.facebook.com/reel/...
```

Agent sẽ tự tải về + gửi vào Telegram.

### Tùy chỉnh nâng cao
Có thể yêu cầu cụ thể hơn:
- "Tải audio mp3 từ [URL]"
- "Tải playlist này, chỉ lấy 10 video đầu: [URL]"
- "Tải video 720p từ [URL]"
- "Tải phụ đề tiếng Việt từ [URL]"
- "Tải thumbnail từ [URL]"

## Workflow

### Step 1: Kiểm tra dependencies

Chạy scripts/check.ps1 để verify yt-dlp và ffmpeg có sẵn. Nếu thiếu, chạy scripts/install.ps1.

### Step 2: Xác định yêu cầu

Thu thập từ user (nếu không có thì dùng default):

| Tham số | Default | Tùy chọn |
|---------|---------|-----------|
| URL | (bắt buộc) | - |
| Loại tải | video | video / audio / playlist / subtitle / thumbnail |
| Chất lượng | best | best / 1080p / 720p / 480p / 360p |
| Format | mp4 (video), mp3 (audio) | mp4 / webm / mkv / mp3 / m4a |
| Thư mục lưu | Downloads\yt-dlp\ | bất kỳ đường dẫn nào |

### Step 3: Chạy lệnh tải

Xem `references/commands.md` để lấy lệnh đúng cho từng use case.

Lệnh cơ bản nhất (video best quality):
```powershell
$PYTHON = scripts/find-python.ps1  # tự detect Python path
& $PYTHON -m yt_dlp `
  -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best" `
  --merge-output-format mp4 `
  -o "$env:USERPROFILE\Downloads\yt-dlp\%(title)s.%(ext)s" `
  "<URL>"
```

### Step 4: Gửi về Telegram (auto)

Sau khi tải xong:

```powershell
$file = Get-ChildItem "$env:USERPROFILE\Downloads\yt-dlp\" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
$sizeMB = [math]::Round($file.Length / 1MB, 2)
```

- File <= 50MB:
  1. Copy file vào workspace tạm: `$env:USERPROFILE\.openclaw\workspace\tmp_send.<ext>`
  2. Dùng `message` tool: action=send, filePath=workspace path, caption="✅ {title} ({sizeMB}MB)"
  3. Xóa file tạm sau khi gửi xong

- File > 50MB: Báo user "File {sizeMB}MB vượt giới hạn 50MB của Telegram. Đã lưu tại: {path}"

- Nếu lỗi khi gửi: thông báo lỗi + đường dẫn file trên máy

## Nền tảng hỗ trợ

Xem `references/platforms.md` để biết danh sách đầy đủ và lưu ý riêng cho từng nền tảng.

Các nền tảng phổ biến: YouTube, TikTok, Facebook, Instagram, Twitter/X, Twitch, Vimeo, SoundCloud, Reddit, Bilibili, Dailymotion, Pinterest, LinkedIn...

## Xử lý lỗi

Xem `references/troubleshooting.md` để xử lý các lỗi thường gặp:
- Lỗi cài đặt / không tìm thấy Python
- HTTP 429 (rate limit)
- Bot detection / cần đăng nhập
- ffmpeg not found
- File quá lớn

## Lưu ý quan trọng

- Playlist > 50 video: hỏi user muốn tải bao nhiêu trước khi chạy
- Nội dung private (Instagram, Twitter): dùng `--cookies-from-browser chrome`
- Rate limit: thêm `--sleep-interval 3 --max-sleep-interval 8`
- Update yt-dlp thường xuyên: `python -m pip install -U yt-dlp`
