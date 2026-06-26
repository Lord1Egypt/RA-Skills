# download-aio — Tải video từ 1000+ nền tảng

> Skill OpenClaw tự động tải video, audio, playlist, subtitle từ YouTube, TikTok, Facebook, Instagram và hơn 1000 nền tảng khác. Sau khi tải xong, **tự động gửi file về Telegram**.

---

## Skill này dùng để làm gì?

Bạn muốn lưu lại một video TikTok hay? Tải nhạc từ YouTube? Lưu cả playlist? Trước đây bạn phải:
1. Vào web convert → quảng cáo đầy → chất lượng thấp
2. Cài app → rác máy tính
3. Copy lệnh yt-dlp phức tạp → dễ sai

Với skill này, chỉ cần **paste URL vào chat** — agent lo hết, xong gửi file thẳng về Telegram cho bạn.

---

## Tính năng

| Tính năng | Chi tiết |
|-----------|---------|
| 🎬 Tải video | Best quality hoặc chọn 1080p / 720p / 480p / 360p |
| 🎵 Tải audio | MP3 hoặc M4A (không cần ffmpeg) |
| 📋 Tải playlist | Toàn bộ hoặc giới hạn số lượng |
| 📝 Tải subtitle | Phụ đề tự động + chính thức, nhiều ngôn ngữ |
| 🖼️ Tải thumbnail | Ảnh bìa chất lượng cao |
| 📤 Auto gửi Telegram | Tự động gửi file <= 50MB về chat |
| 🔧 Auto install | Script tự cài Python, yt-dlp, ffmpeg |

---

## Nền tảng hỗ trợ

**Phổ biến nhất:**

| Nền tảng | Ghi chú |
|----------|---------|
| YouTube | Video, Shorts, Live, Playlist, Channel |
| TikTok | Hầu hết không có watermark |
| Facebook | Public video, Reel, Watch |
| Instagram | Public post, Reel (private cần đăng nhập) |
| Twitter / X | Video tweets |
| Twitch | VOD, Clips |
| Vimeo | Full support |
| SoundCloud | Audio tracks |
| Reddit | Video posts |
| Bilibili | Video Trung Quốc |

> Tổng cộng hỗ trợ **1000+ nền tảng**. Xem danh sách đầy đủ tại [supported sites](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md).

---

## Cài đặt

### Yêu cầu
- Windows 10/11 (PowerShell)
- Python 3.10+ (script sẽ nhắc nếu chưa có)
- OpenClaw đã cài đặt

### Bước 1 — Copy skill vào OpenClaw

```powershell
Copy-Item -Recurse download-aio $env:USERPROFILE\.agents\skills\
```

### Bước 2 — Chạy script cài đặt tự động

```powershell
powershell -ExecutionPolicy Bypass -File $env:USERPROFILE\.agents\skills\download-aio\scripts\install.ps1
```

Script sẽ tự động:
- ✅ Kiểm tra Python (nhắc cài nếu thiếu)
- ✅ Cài / update yt-dlp lên bản mới nhất
- ✅ Cài ffmpeg qua Chocolatey (nếu có)
- ✅ Tạo thư mục `Downloads\yt-dlp\`

---

## Cách dùng

### Cách đơn giản nhất

Chỉ cần paste URL vào chat với OpenClaw agent:

```
https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

Agent tự hiểu, tải về, gửi file Telegram cho bạn. Xong.

### Tùy chỉnh nâng cao

Bạn có thể yêu cầu cụ thể hơn bằng ngôn ngữ tự nhiên:

```
Tải audio mp3 từ https://youtu.be/...

Tải playlist này, chỉ lấy 10 video đầu: https://youtube.com/playlist?list=...

Tải video 720p từ https://www.tiktok.com/@...

Tải phụ đề tiếng Việt từ https://youtu.be/...

Tải thumbnail từ https://www.facebook.com/reel/...
```

### Logic gửi Telegram

| Dung lượng file | Hành động |
|----------------|-----------|
| <= 50MB | Tự động gửi file về Telegram |
| > 50MB | Báo vị trí file trên máy, không gửi |

---

## Cấu trúc files

```
download-aio/
├── README.md              ← Bạn đang đọc file này
├── SKILL.md               ← Điều khiển agent (không cần đọc)
├── scripts/
│   ├── install.ps1        ← Cài đặt tự động toàn bộ dependencies
│   ├── check.ps1          ← Kiểm tra nhanh mọi thứ đã sẵn sàng chưa
│   └── find-python.ps1    ← Auto detect Python path trên máy
└── references/
    ├── commands.md        ← Lệnh yt-dlp chi tiết cho mọi use case
    ├── platforms.md       ← Danh sách nền tảng + lưu ý riêng
    └── troubleshooting.md ← Xử lý lỗi thường gặp
```

---

## Xử lý sự cố

| Lỗi | Cách fix |
|-----|---------|
| Python không tìm thấy | Chạy lại `install.ps1`, cài Python tại [python.org](https://python.org) |
| HTTP 429 / Rate limit | Agent tự thêm delay, hoặc dùng `--cookies-from-browser chrome` |
| Video cần đăng nhập | Mở Chrome, đăng nhập, agent dùng `--cookies-from-browser chrome` |
| ffmpeg not found | Chạy `choco install ffmpeg` hoặc tải tại [ffmpeg.org](https://ffmpeg.org) |
| File > 50MB | File được lưu tại `Downloads\yt-dlp\`, agent thông báo đường dẫn |

---

## Update yt-dlp

Các nền tảng thay đổi thường xuyên, nên update yt-dlp định kỳ:

```powershell
python -m pip install -U yt-dlp
```

---

<p align="center">
  <a href="https://www.mcbai.vn">MCB AI</a> &nbsp;·&nbsp;
  <a href="https://www.youtube.com/@mcbaivn">YouTube</a> &nbsp;·&nbsp;
  <a href="https://openclaw.mcbai.vn">OpenClaw Cheatsheet</a> &nbsp;·&nbsp;
  <a href="https://openclaw.mcbai.vn/openclaw101">Khoá học OpenClaw 101</a> &nbsp;·&nbsp;
  <a href="https://www.facebook.com/groups/openclawxvn">Cộng đồng Facebook</a> &nbsp;·&nbsp;
  <a href="https://zalo.me/g/mmqkhi259">MCB AI Academy (Zalo)</a>
</p>
