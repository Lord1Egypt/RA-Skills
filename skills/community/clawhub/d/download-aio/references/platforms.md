# Nền tảng hỗ trợ - Download AIO

## Hỗ trợ đầy đủ (không cần đăng nhập)

| Nền tảng | URL mẫu | Ghi chú |
|----------|---------|---------|
| YouTube | youtube.com/watch?v=... | Video, Shorts, Live, Playlist, Channel |
| YouTube Music | music.youtube.com/... | Audio streams |
| TikTok | tiktok.com/@user/video/... | Hầu hết không có watermark |
| Facebook | facebook.com/reel/... | Public video/reel |
| Facebook | facebook.com/watch/?v=... | Public watch |
| Vimeo | vimeo.com/123456 | Full support |
| Twitch | twitch.tv/videos/... | VOD, Clips |
| SoundCloud | soundcloud.com/artist/track | Audio |
| Reddit | reddit.com/r/.../comments/... | Video posts |
| Dailymotion | dailymotion.com/video/... | Full support |
| Bilibili | bilibili.com/video/BV... | Video Trung Quốc |
| Rumble | rumble.com/... | Full support |
| Odysee/LBRY | odysee.com/@... | Full support |
| Streamable | streamable.com/... | Short clips |
| Imgur | imgur.com/... | GIF/Video |

## Cần đăng nhập (dùng cookie)

| Nền tảng | Yêu cầu | Lệnh |
|----------|---------|------|
| Instagram | Đăng nhập để xem private | `--cookies-from-browser chrome` |
| Twitter/X | Một số video cần login | `--cookies-from-browser chrome` |
| YouTube (private) | Video private/members | `--cookies-from-browser chrome` |
| Twitch (sub-only) | Kênh subscription | `--cookies-from-browser chrome` |
| Facebook (private) | Group/profile riêng tư | `--cookies-from-browser chrome` |

## Lưu ý theo nền tảng

### YouTube
- Shorts: URL dạng youtube.com/shorts/VIDEO_ID
- Playlist: youtube.com/playlist?list=PLAYLIST_ID
- Channel toàn bộ: youtube.com/c/ChannelName/videos
- Live (đang phát): thêm `--live-from-start` để tải từ đầu

### TikTok
- Hầu hết video tải được không watermark
- Nếu có watermark: thử thêm `-f "download_addr-2"` nếu có trong `-F`
- Profile: `--playlist-end 20` để giới hạn số video

### Facebook
- Chỉ tải được public content
- Private group/profile cần cookie: `--cookies-from-browser chrome`
- Reels: facebook.com/reel/REEL_ID

### Instagram
- Public post/reel: OK không cần login
- Private account: bắt buộc dùng `--cookies-from-browser chrome`
- Stories: cần login
- Highlight: cần login

### Twitter/X
- Hầu hết video public OK
- Một số cần login: thêm `--cookies-from-browser chrome`

## Kiểm tra nền tảng có hỗ trợ không

```powershell
$python = & scripts/find-python.ps1
& $python -m yt_dlp --list-extractors | Select-String "tên-nền-tảng"
```

Hoặc xem danh sách đầy đủ 1000+ trang web tại:
https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md
