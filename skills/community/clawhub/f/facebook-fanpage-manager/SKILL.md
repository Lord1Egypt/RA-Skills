---
name: facebook-fanpage-manager
description: >
  Skill quản lý Fanpage Facebook toàn diện cho OpenClaw: tự động trả lời tin nhắn Messenger,
  đăng bài Fanpage, reply comment, xem insights. Bao gồm hướng dẫn chi tiết từng bước
  lấy Page ID và Page Access Token vĩnh viễn. Sử dụng khi người dùng nhắc đến: Facebook,
  Fanpage, Messenger, đăng bài, auto reply, trả lời tin nhắn tự động, Page ID, access token,
  Graph API, webhook, quản lý fanpage, social media automation.
version: 1.0.0
metadata:
  openclaw:
    author: Pham Triet
    community: OpenClaw Việt Nam
    community_link: https://zalo.me/g/lajsqc334jqc5fezevvo
    emoji: "📘"
    requires:
      env:
        - FACEBOOK_PAGE_ID
        - FACEBOOK_ACCESS_TOKEN
      bins:
        - curl
    tags:
      - facebook
      - messenger
      - fanpage
      - social-media
      - auto-reply
      - vietnamese
---

# Facebook Fanpage Manager cho OpenClaw

> **Author:** Pham Triet
> **Cộng đồng:** [OpenClaw Việt Nam](https://zalo.me/g/lajsqc334jqc5fezevvo)

Skill quản lý Fanpage Facebook toàn diện: đăng bài, reply comment, auto-reply Messenger.
Bao gồm hướng dẫn lấy token từ A đến Z.

## Mục lục

1. [Hướng dẫn lấy Page ID & Token (BẮT BUỘC đọc trước)](#1-hướng-dẫn-lấy-page-id--access-token)
2. [Cấu hình OpenClaw](#2-cấu-hình-openclaw)
3. [Đăng bài Fanpage](#3-đăng-bài-fanpage)
4. [Reply comment](#4-reply-comment)
5. [Auto-reply Messenger](#5-auto-reply-messenger)
6. [Xem Insights](#6-xem-insights)

**→ Đọc `references/setup-guide.md` để xem hướng dẫn CÓ HÌNH chi tiết từng bước.**
**→ Đọc `references/api-reference.md` để xem danh sách API endpoints.**

---

## 1. Hướng dẫn lấy Page ID & Access Token

**Đây là bước QUAN TRỌNG NHẤT — không có token thì skill không hoạt động.**

**→ Hướng dẫn đầy đủ có trong file `references/setup-guide.md`**

Tóm tắt nhanh 4 bước:

```
Bước 1: Tạo tài khoản Meta for Developers
         → developers.facebook.com → Get Started

Bước 2: Tạo App
         → developers.facebook.com/apps → Tạo ứng dụng
         → Chọn "Tương tác với khách hàng trên Messenger"

Bước 3: Lấy Page ID + Short-lived Token
         → developers.facebook.com/tools/explorer/
         → Chọn App → Thêm quyền → Generate Access Token
         → Query "me/accounts" → lấy "id" và "access_token"

Bước 4: Đổi sang Token vĩnh viễn
         → Lấy App ID + App Secret từ Settings → Basic
         → Query đổi token (xem chi tiết trong setup-guide.md)
```

---

## 2. Cấu hình OpenClaw

Sau khi có Page ID và Token vĩnh viễn, cấu hình trong `~/.openclaw/openclaw.json`:

```json
{
  "skills": {
    "entries": {
      "facebook-fanpage-manager": {
        "env": {
          "FACEBOOK_PAGE_ID": "123456789012345",
          "FACEBOOK_ACCESS_TOKEN": "EAAG...your_permanent_page_token..."
        }
      }
    }
  }
}
```

**Kiểm tra kết nối:**

```bash
curl "https://graph.facebook.com/v21.0/$FACEBOOK_PAGE_ID?fields=name,followers_count" \
  -H "Authorization: Bearer $FACEBOOK_ACCESS_TOKEN"
```

Nếu trả về tên Fanpage và số followers → kết nối thành công.

---

## 3. Đăng bài Fanpage

### Đăng bài text

```bash
curl -X POST "https://graph.facebook.com/v21.0/$FACEBOOK_PAGE_ID/feed" \
  -H "Authorization: Bearer $FACEBOOK_ACCESS_TOKEN" \
  -d "message=Nội dung bài đăng"
```

### Đăng bài có ảnh

```bash
curl -X POST "https://graph.facebook.com/v21.0/$FACEBOOK_PAGE_ID/photos" \
  -H "Authorization: Bearer $FACEBOOK_ACCESS_TOKEN" \
  -F "url=https://example.com/image.jpg" \
  -F "caption=Nội dung kèm ảnh"
```

### Đăng bài có link

```bash
curl -X POST "https://graph.facebook.com/v21.0/$FACEBOOK_PAGE_ID/feed" \
  -H "Authorization: Bearer $FACEBOOK_ACCESS_TOKEN" \
  -d "message=Xem thêm tại đây" \
  -d "link=https://example.com"
```

### Lấy danh sách bài đã đăng

```bash
curl "https://graph.facebook.com/v21.0/$FACEBOOK_PAGE_ID/posts?fields=message,created_time,shares,likes.summary(true),comments.summary(true)&limit=10" \
  -H "Authorization: Bearer $FACEBOOK_ACCESS_TOKEN"
```

---

## 4. Reply comment

### Lấy comments của bài viết

```bash
curl "https://graph.facebook.com/v21.0/{post_id}/comments?fields=from,message,created_time" \
  -H "Authorization: Bearer $FACEBOOK_ACCESS_TOKEN"
```

### Reply một comment

```bash
curl -X POST "https://graph.facebook.com/v21.0/{comment_id}/comments" \
  -H "Authorization: Bearer $FACEBOOK_ACCESS_TOKEN" \
  -d "message=Cảm ơn bạn đã quan tâm!"
```

### Quy trình auto-reply comment (AI soạn nội dung)

1. Lấy danh sách bài viết mới nhất
2. Lấy comments chưa reply
3. Dùng AI phân tích nội dung comment
4. Soạn reply phù hợp
5. Gửi reply qua API

---

## 5. Auto-reply Messenger

### Gửi tin nhắn cho người dùng

```bash
curl -X POST "https://graph.facebook.com/v21.0/$FACEBOOK_PAGE_ID/messages" \
  -H "Authorization: Bearer $FACEBOOK_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "recipient": {"id": "USER_PSID"},
    "message": {"text": "Xin chào! Cảm ơn bạn đã nhắn tin."}
  }'
```

### Lấy danh sách conversations

```bash
curl "https://graph.facebook.com/v21.0/$FACEBOOK_PAGE_ID/conversations?fields=participants,messages{message,from,created_time}&limit=10" \
  -H "Authorization: Bearer $FACEBOOK_ACCESS_TOKEN"
```

### Webhook cho Messenger (realtime auto-reply)

Để nhận tin nhắn realtime, cần setup webhook. Xem chi tiết trong `references/setup-guide.md` phần "Setup Webhook".

**Lưu ý:** Webhook cần server chạy liên tục (VPS, ngrok, hoặc Cloudflare Tunnel).
Nếu không có server, vẫn có thể dùng cách polling (lấy tin nhắn định kỳ).

### Cách polling (không cần webhook)

```bash
# Lấy tin nhắn mới mỗi 30 giây
curl "https://graph.facebook.com/v21.0/$FACEBOOK_PAGE_ID/conversations?fields=messages.limit(1){message,from,created_time}&limit=5" \
  -H "Authorization: Bearer $FACEBOOK_ACCESS_TOKEN"
```

Quy trình polling:
1. Cứ mỗi 30–60 giây, lấy danh sách conversations mới
2. Kiểm tra tin nhắn chưa reply
3. Dùng AI soạn reply
4. Gửi reply qua Send API

---

## 6. Xem Insights

### Thống kê Fanpage

```bash
curl "https://graph.facebook.com/v21.0/$FACEBOOK_PAGE_ID/insights?metric=page_impressions,page_engaged_users,page_fans&period=day" \
  -H "Authorization: Bearer $FACEBOOK_ACCESS_TOKEN"
```

### Thống kê bài viết

```bash
curl "https://graph.facebook.com/v21.0/{post_id}/insights?metric=post_impressions,post_engaged_users,post_clicks" \
  -H "Authorization: Bearer $FACEBOOK_ACCESS_TOKEN"
```

---

## Lưu ý quan trọng

- **Token vĩnh viễn vẫn có thể hết hạn** nếu: đổi mật khẩu Facebook, gỡ quyền App, hoặc App bị vô hiệu hóa. Khi đó cần lấy token mới.
- **Rate limit**: Facebook giới hạn khoảng 200 requests/giờ. Không gọi API quá nhiều.
- **Quyền cần có**: `pages_show_list`, `pages_messaging`, `pages_manage_metadata`, `pages_manage_posts`, `pages_read_engagement`.
- **App Mode**: App phải ở chế độ **Live** (không phải Development) để hoạt động với người dùng khác.

---

## Cấu trúc thư mục skill

```
facebook-fanpage-manager/
├── SKILL.md                    ← File này
├── references/
│   ├── setup-guide.md          ← Hướng dẫn lấy token từng bước chi tiết
│   └── api-reference.md        ← Danh sách API endpoints
└── scripts/
    └── check-connection.sh     ← Script kiểm tra kết nối
```
