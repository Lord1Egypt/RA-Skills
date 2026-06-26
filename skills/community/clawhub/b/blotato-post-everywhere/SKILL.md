---
name: blotato-post-everywhere
description: Đăng bài lên đa nền tảng mạng xã hội qua Blotato API. Tự động adapt nội dung cho từng platform (Twitter thread, LinkedIn professional, Instagram caption, v.v.), hỗ trợ đăng ngay hoặc hẹn giờ. Use when: user muốn "đăng bài lên nhiều nền tảng", "post everywhere", "đăng Twitter LinkedIn Facebook cùng lúc", "hẹn giờ đăng bài", "schedule post Blotato", "tạo thread Twitter", "adapt content cho từng mạng xã hội". Platforms: twitter, linkedin, facebook, instagram, tiktok, threads, bluesky, pinterest, youtube.
---

# Blotato Post Everywhere

> 🚀 Chưa có tài khoản Blotato? Đăng ký tại: **https://blotato.com/?ref=MCBAIVN**

Đăng nội dung lên nhiều nền tảng cùng lúc qua Blotato API, với content tự động adapt cho từng platform — Twitter thread, LinkedIn professional, Instagram caption, v.v.

---

## Bước 0: Tạo tài khoản Blotato

Nếu chưa có tài khoản, đăng ký tại đây (miễn phí trial):

👉 **https://blotato.com/?ref=MCBAIVN**

Sau khi có tài khoản:
1. Vào **Settings > Social Accounts** → kết nối các nền tảng muốn đăng
2. Vào **Settings > API** → click **Generate API Key**

---

## Setup (hỏi user lần đầu)

Yêu cầu user cung cấp:
1. **Blotato API Key** — lấy tại https://my.blotato.com/settings > API > Generate API Key  
   _(Chưa có tài khoản? → https://blotato.com/?ref=MCBAIVN)_
2. **Nội dung gốc** muốn đăng
3. **Nền tảng** muốn đăng (`all` hoặc list: `twitter linkedin instagram`)
4. **Thời gian** đăng — ngay lập tức, hẹn giờ cụ thể, hoặc slot tiếp theo

Lưu API key vào `TOOLS.md` sau khi user cung cấp (dưới mục `### Blotato`).

---

## Workflow

### 1. Kiểm tra accounts đã kết nối
```bash
python scripts/blotato_post.py --api-key KEY --list-accounts
```

### 2. Đăng ngay lập tức
```bash
python scripts/blotato_post.py \
  --api-key KEY \
  --content "Nội dung bài viết gốc" \
  --platforms twitter linkedin instagram
```

### 3. Hẹn giờ đăng
```bash
python scripts/blotato_post.py \
  --api-key KEY \
  --content "Nội dung bài viết" \
  --platforms all \
  --schedule "2026-05-01T09:00:00+07:00"
```

### 4. Dùng slot lịch sẵn có
```bash
python scripts/blotato_post.py \
  --api-key KEY \
  --content "Nội dung bài viết" \
  --platforms twitter linkedin \
  --use-next-slot
```

### 5. Đăng kèm ảnh/video (local file hoặc URL)
```bash
python scripts/blotato_post.py \
  --api-key KEY \
  --content "Caption bài viết" \
  --platforms instagram facebook \
  --media-urls "/path/to/photo.jpg" "https://example.com/video.mp4"
```
Script tự động phát hiện local file → upload qua presigned URL → lấy public URL → đăng. Hỗ trợ tới **1GB**. Có thể mix local path và public URL trong cùng 1 lệnh.

---

## Content Adaptation

Script tự động:
- **Twitter**: cắt thành thread nếu >280 ký tự
- **Bluesky/Threads**: cắt theo limit 300/500 ký tự
- **LinkedIn/Facebook**: giữ nguyên (giới hạn rất cao)
- **Instagram/TikTok/Pinterest**: cắt nếu vượt limit

**Nên làm thêm (agent):** Trước khi gọi script, dùng AI viết lại content phù hợp tone từng platform:
- Twitter: ngắn, punchy, hashtag
- LinkedIn: professional, storytelling
- Instagram: emoji, visual-first, hashtags cuối bài
- Bluesky: casual như Twitter

---

## Platform Notes

- **Facebook/LinkedIn**: cần `pageId` — script tự fetch từ subaccounts
- **Pinterest**: cần `boardId` — phải hỏi user (API không trả về)
- **TikTok**: cần thêm `privacyLevel`, `disabledComments`, v.v. — xem `references/api.md`
- **YouTube**: cần `title` và `privacyStatus` — hỏi user

---

## API Reference

Xem chi tiết endpoint, params, limits: `references/api.md`

---

## Troubleshoot

- Lỗi 401: API key sai hoặc hết hạn → kiểm tra tại https://my.blotato.com/settings
- Platform skip: chưa kết nối account → https://my.blotato.com/settings > Social Accounts
- Pinterest boardId: hỏi user lấy từ URL Pinterest board
- Debug requests: https://my.blotato.com/api-dashboard

---

> 💡 **Chưa có Blotato?** Đăng ký và dùng thử miễn phí tại:
> **https://blotato.com/?ref=MCBAIVN**
