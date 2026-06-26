# Download AIO - Lệnh yt-dlp chi tiết

## Setup Python path

```powershell
# Luôn dùng find-python.ps1 để tìm Python đúng
$PYTHON = & "$PSScriptRoot\..\scripts\find-python.ps1"
$OUT = "$env:USERPROFILE\Downloads\yt-dlp"
New-Item -ItemType Directory -Path $OUT -Force | Out-Null
```

## Tải video (best quality - mp4)

```powershell
& $PYTHON -m yt_dlp `
  -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best" `
  --merge-output-format mp4 `
  -o "$OUT\%(title)s.%(ext)s" `
  "<URL>"
```

## Tải video theo chất lượng cụ thể

```powershell
# 1080p
-f "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080]"

# 720p
-f "bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720]"

# 480p
-f "bestvideo[height<=480]+bestaudio/best[height<=480]"

# 360p (nhẹ nhất)
-f "bestvideo[height<=360]+bestaudio/best[height<=360]"
```

## Tải audio only

```powershell
# MP3 (cần ffmpeg)
& $PYTHON -m yt_dlp `
  -x --audio-format mp3 --audio-quality 0 `
  -o "$OUT\%(title)s.%(ext)s" `
  "<URL>"

# M4A (không cần ffmpeg)
& $PYTHON -m yt_dlp `
  -f "bestaudio[ext=m4a]/bestaudio" `
  -o "$OUT\%(title)s.%(ext)s" `
  "<URL>"
```

## Tải playlist

```powershell
# Toàn bộ playlist
& $PYTHON -m yt_dlp `
  -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best" `
  --merge-output-format mp4 `
  -o "$OUT\%(playlist_title)s\%(playlist_index)s - %(title)s.%(ext)s" `
  "<PLAYLIST_URL>"

# Giới hạn số lượng (10 video đầu)
--playlist-end 10

# Bắt đầu từ video thứ N
--playlist-start 5

# Chỉ tải video thứ 3, 5, 7
--playlist-items 3,5,7
```

## Tải subtitle / phụ đề

```powershell
# Phụ đề tự động (auto-generated)
& $PYTHON -m yt_dlp `
  --write-auto-sub --sub-lang "vi,en" --skip-download `
  -o "$OUT\%(title)s.%(ext)s" `
  "<URL>"

# Phụ đề chính thức
--write-sub --sub-lang "vi,en"

# Embed phụ đề vào video
--embed-subs --sub-lang "vi,en"

# Tải cả video lẫn phụ đề
& $PYTHON -m yt_dlp `
  -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best" `
  --merge-output-format mp4 `
  --write-sub --write-auto-sub --sub-lang "vi,en" `
  -o "$OUT\%(title)s.%(ext)s" `
  "<URL>"
```

## Tải thumbnail

```powershell
& $PYTHON -m yt_dlp `
  --write-thumbnail --skip-download --convert-thumbnails jpg `
  -o "$OUT\%(title)s.%(ext)s" `
  "<URL>"
```

## Xem thông tin video (không tải)

```powershell
# Thông tin cơ bản
& $PYTHON -m yt_dlp --dump-json "<URL>" | ConvertFrom-Json | `
  Select-Object title, duration, view_count, like_count, upload_date, uploader

# Liệt kê tất cả format có sẵn
& $PYTHON -m yt_dlp -F "<URL>"
```

## Dùng cookie (cho content cần đăng nhập)

```powershell
# Dùng cookie từ Chrome (phổ biến nhất)
--cookies-from-browser chrome

# Dùng cookie từ Firefox
--cookies-from-browser firefox

# Export cookie thủ công (nếu auto không được)
# Dùng extension "Get cookies.txt LOCALLY" trên Chrome
# Export ra cookies.txt rồi dùng:
--cookies path/to/cookies.txt
```

## Options hữu ích

```powershell
--no-playlist              # Chỉ tải 1 video, bỏ qua playlist
--yes-playlist             # Force tải cả playlist
--download-archive "$OUT\downloaded.txt"  # Lưu lịch sử, skip đã tải
--concurrent-fragments 4   # Tải nhanh hơn (4 luồng song song)
--retries 10               # Retry 10 lần khi lỗi network
--sleep-interval 2         # Chờ 2s giữa các request (tránh rate limit)
--max-sleep-interval 5     # Chờ tối đa 5s
--limit-rate 5M            # Giới hạn tốc độ 5MB/s
--no-overwrites            # Không ghi đè file đã tồn tại
-k                         # Giữ lại file gốc sau khi merge
```

## Gửi file về Telegram (qua OpenClaw message tool)

```powershell
# Sau khi tải xong, lấy file mới nhất
$file = Get-ChildItem $OUT -Filter "*.mp4" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
$sizeMB = [math]::Round($file.Length / 1MB, 2)

if ($sizeMB -le 50) {
    # Copy vào workspace để gửi (OpenClaw chỉ cho phép gửi từ workspace)
    $tmpPath = "$env:USERPROFILE\.openclaw\workspace\tmp_send$($file.Extension)"
    Copy-Item $file.FullName $tmpPath -Force

    # Dùng message tool của OpenClaw:
    # action: send
    # channel: telegram
    # filePath: $tmpPath
    # caption: "✅ $($file.BaseName) ($sizeMB MB)"

    # Sau khi gửi xong, xóa file tạm
    Remove-Item $tmpPath -Force
} else {
    Write-Host "File $sizeMB MB vuot gioi han 50MB Telegram. Da luu tai: $($file.FullName)"
}
```

## Update yt-dlp

```powershell
$PYTHON = & scripts/find-python.ps1
& $PYTHON -m pip install -U yt-dlp
```
