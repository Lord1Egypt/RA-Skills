# 📘 Facebook Page Manager — by MCB AI

Skill quản lý và đăng nội dung **tự động** lên Facebook Fanpage qua **Graph API v19.0**.

> 🌐 [English version](https://github.com/mcbaivn/openclaw-skills-mcbai-en/tree/main/skills/social-media/facebook-page-manager)

---

## ✨ Tính năng

| Tính năng | Hỗ trợ |
|-----------|--------|
| Đăng text | ✅ |
| Đăng ảnh đơn | ✅ |
| Carousel (nhiều ảnh) | ✅ tối đa 10 ảnh |
| Đăng video | ✅ |
| Reels | ✅ 3–90 giây |
| Story ảnh/video | ✅ |
| Hẹn giờ đăng bài | ✅ |
| Xem/xóa/reschedule bài | ✅ |
| Comment vào bài viết | ✅ |
| Reply comment | ✅ |
| Xóa comment | ✅ |

---

## 🚀 Cài đặt nhanh

```bash
npx clawhub@latest install facebook-management-skills-by-mcbai
```

Hoặc copy thủ công vào `~/.agents/skills/`

---

## ⚙️ Setup

### 1. Cài dependencies
```bash
pip install requests
```

### 2. Lấy Page Access Token
- Vào [Graph API Explorer](https://developers.facebook.com/tools/explorer/)
- Chọn permissions: `pages_manage_posts`, `pages_read_engagement`, `pages_manage_engagement`, `publish_video`
- Gọi `GET /me/accounts` → lấy **Page Access Token** và **Page ID**
- Xem hướng dẫn chi tiết: [`references/get-token.md`](./references/get-token.md)

### 3. Tạo file config
Tạo `scripts/fb_config.json`:
```json
{
  "access_token": "EAAxxxxxxxxxxxxxxx",
  "page_id": "123456789012345"
}
```

---

## 📖 Cách dùng

### Đăng bài
```bash
python fb_post.py text --message "Nội dung bài viết"
python fb_post.py photo --message "Caption" --images anh1.jpg anh2.jpg
python fb_post.py video --message "Caption" --video clip.mp4
python fb_post.py video --message "Caption" --video clip.mp4 --reel
python fb_post.py story --type photo --media story.jpg
python fb_post.py story --type video --media story.mp4
```

### Hẹn giờ đăng
```bash
python fb_post.py text --message "Bài sáng thứ Hai" --schedule "2024-12-25 08:00"
python fb_post.py photo --message "Caption" --images anh.jpg --schedule "2024-12-25 10:00"
```

### Quản lý lịch đăng
```bash
python fb_post.py list-scheduled
python fb_post.py delete --post-id PAGE_ID_POST_ID
python fb_post.py reschedule --post-id PAGE_ID_POST_ID --schedule "2024-12-26 09:00"
```

### Comment & Reply
```bash
python fb_post.py comment --post-id PAGE_ID_POST_ID --message "Nội dung comment"
python fb_post.py reply --comment-id COMMENT_ID --message "Nội dung reply"
python fb_post.py list-comments --post-id PAGE_ID_POST_ID
python fb_post.py delete-comment --comment-id COMMENT_ID
```

---

## 🔑 Permissions cần thiết

| Tính năng | Permission |
|-----------|------------|
| Đăng text/ảnh/video/story | `pages_manage_posts` |
| Đăng video/Reels | `pages_manage_posts` + `publish_video` |
| Xem/xóa bài | `pages_read_engagement` |
| Comment/Reply/Xóa comment | `pages_manage_engagement` |

---

## 📁 Cấu trúc

```
facebook-page-manager/
├── SKILL.md                    ← OpenClaw đọc file này
├── README.md                   ← Hướng dẫn (file này)
├── scripts/
│   └── fb_post.py              ← Script chính
└── references/
    ├── get-token.md            ← Hướng dẫn lấy token từng bước
    └── api-reference.md        ← Chi tiết endpoints & format
```

---

## ⚠️ Lưu ý

- Page phải ở trạng thái **Published** (không phải Unpublished/Restricted)
- Video upload có thể mất vài phút xử lý
- Story **không hỗ trợ** hẹn giờ
- **Không commit** `fb_config.json` lên GitHub

---

## 🔗 Liên kết

🌐 [mcbai.vn](https://www.mcbai.vn) · 📘 [Fanpage MCB AI](https://www.facebook.com/mcb.ai.vn) · 🎬 [YouTube @mcbaivn](https://www.youtube.com/@mcbaivn)

Made with ❤️ by [MCB AI](https://www.mcbai.vn)
