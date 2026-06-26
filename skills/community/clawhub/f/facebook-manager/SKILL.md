---
name: facebook-manager
description: >
  Skill quản lý Facebook toàn diện cho OpenClaw: hỗ trợ CẢ Fanpage (Page Token)
  VÀ tài khoản cá nhân (User Token). Fanpage: đăng bài, reply comment, auto-reply
  Messenger, xem insights. User Token: tìm nhóm, đọc bài trong nhóm, tìm trang khác,
  tìm kiếm bài viết công khai. Hướng dẫn lấy token từ A đến Z.
  Sử dụng khi người dùng nhắc đến: Facebook, Fanpage, Messenger, nhóm Facebook,
  group, đăng bài, auto reply, tìm bài, search Facebook, Page ID, access token,
  Graph API, quản lý fanpage, social media.
version: 2.0.0
metadata:
  openclaw:
    author: Pham Triet
    community: OpenClaw Việt Nam
    community_link: https://zalo.me/g/lajsqc334jqc5fezevvo
    emoji: "📘"
    requires:
      env:
        - FACEBOOK_ACCESS_TOKEN
      bins:
        - curl
    tags:
      - facebook
      - messenger
      - fanpage
      - groups
      - social-media
      - auto-reply
      - user-token
      - vietnamese
---

# Facebook Manager v2 cho OpenClaw

> **Author:** Pham Triet
> **Cộng đồng:** [OpenClaw Việt Nam](https://zalo.me/g/lajsqc334jqc5fezevvo)

Skill quản lý Facebook toàn diện — hỗ trợ **2 chế độ token**:

## Chọn chế độ nào?

| Nhu cầu | Chế độ | Token |
|---------|:------:|-------|
| Quản lý Fanpage (đăng bài, reply, Messenger, insights) | **Page** | Page Access Token (vĩnh viễn) |
| Tìm nhóm, đọc bài nhóm, tìm trang khác, search bài viết | **User** | User Access Token (~60 ngày) |
| Cả hai | **Cả hai** | Cấu hình 2 token riêng |

**→ Đọc `references/setup-guide.md` để lấy token từng bước.**

---

## So sánh quyền Page Token vs User Token

| Tính năng | Page Token | User Token |
|-----------|:----------:|:----------:|
| Đăng bài Fanpage | ✅ | ✅ (nếu là admin) |
| Reply comment trên Fanpage | ✅ | ✅ |
| Gửi tin nhắn Messenger | ✅ | ❌ |
| Xem Insights Fanpage | ✅ | ❌ |
| Tìm nhóm Facebook | ❌ | ✅ |
| Đọc bài trong nhóm (là thành viên) | ❌ | ✅ |
| Tìm trang/Fanpage khác | ❌ | ✅ |
| Tìm kiếm bài viết công khai | ❌ | ✅ (hạn chế) |
| Đọc thông tin cá nhân | ❌ | ✅ |
| Hết hạn | Vĩnh viễn | ~60 ngày |

---

## Cấu hình OpenClaw

```json
{
  "skills": {
    "entries": {
      "facebook-manager": {
        "env": {
          "FACEBOOK_PAGE_ID": "123456789012345",
          "FACEBOOK_PAGE_TOKEN": "EAAG...page_token_vinh_vien...ZD",
          "FACEBOOK_USER_TOKEN": "EAAG...user_token_60_ngay...ZD"
        }
      }
    }
  }
}
```

Chỉ cần token nào bạn dùng — không bắt buộc cả hai.

---

## CHẾ ĐỘ 1: QUẢN LÝ FANPAGE (Page Token)

### Đăng bài

```bash
# Đăng bài text
curl -X POST "https://graph.facebook.com/v22.0/$FACEBOOK_PAGE_ID/feed" \
  -H "Authorization: Bearer $FACEBOOK_PAGE_TOKEN" \
  -d "message=Nội dung bài đăng"

# Đăng bài có ảnh
curl -X POST "https://graph.facebook.com/v22.0/$FACEBOOK_PAGE_ID/photos" \
  -H "Authorization: Bearer $FACEBOOK_PAGE_TOKEN" \
  -F "url=https://example.com/image.jpg" \
  -F "caption=Nội dung kèm ảnh"

# Đăng bài có link
curl -X POST "https://graph.facebook.com/v22.0/$FACEBOOK_PAGE_ID/feed" \
  -H "Authorization: Bearer $FACEBOOK_PAGE_TOKEN" \
  -d "message=Xem thêm tại đây" -d "link=https://example.com"
```

### Reply comment

```bash
# Lấy comments
curl "https://graph.facebook.com/v22.0/{post_id}/comments?fields=from,message,created_time" \
  -H "Authorization: Bearer $FACEBOOK_PAGE_TOKEN"

# Reply
curl -X POST "https://graph.facebook.com/v22.0/{comment_id}/comments" \
  -H "Authorization: Bearer $FACEBOOK_PAGE_TOKEN" \
  -d "message=Cảm ơn bạn đã quan tâm!"
```

### Auto-reply Messenger

```bash
# Gửi tin nhắn
curl -X POST "https://graph.facebook.com/v22.0/$FACEBOOK_PAGE_ID/messages" \
  -H "Authorization: Bearer $FACEBOOK_PAGE_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"recipient":{"id":"USER_PSID"},"message":{"text":"Xin chào!"}}'

# Lấy conversations
curl "https://graph.facebook.com/v22.0/$FACEBOOK_PAGE_ID/conversations?\
fields=participants,messages{message,from,created_time}&limit=10" \
  -H "Authorization: Bearer $FACEBOOK_PAGE_TOKEN"
```

### Xem Insights

```bash
curl "https://graph.facebook.com/v22.0/$FACEBOOK_PAGE_ID/insights?\
metric=page_impressions,page_engaged_users,page_fans&period=day" \
  -H "Authorization: Bearer $FACEBOOK_PAGE_TOKEN"
```

---

## CHẾ ĐỘ 2: TÌM KIẾM & NHÓM (User Token)

### Tìm nhóm Facebook

```bash
# Tìm nhóm theo từ khóa
curl "https://graph.facebook.com/v22.0/search?q=BDS+Da+Lat&type=group&limit=10" \
  -H "Authorization: Bearer $FACEBOOK_USER_TOKEN"

# Lấy danh sách nhóm đã tham gia
curl "https://graph.facebook.com/v22.0/me/groups?fields=name,member_count,privacy&limit=20" \
  -H "Authorization: Bearer $FACEBOOK_USER_TOKEN"
```

### Đọc bài trong nhóm (phải là thành viên)

```bash
# Lấy bài viết trong nhóm
curl "https://graph.facebook.com/v22.0/{group_id}/feed?\
fields=message,from,created_time,attachments&limit=20" \
  -H "Authorization: Bearer $FACEBOOK_USER_TOKEN"
```

### Tìm trang/Fanpage khác

```bash
# Tìm trang theo từ khóa
curl "https://graph.facebook.com/v22.0/search?q=BDS+Da+Lat&type=page&limit=10&\
fields=name,fan_count,category,link" \
  -H "Authorization: Bearer $FACEBOOK_USER_TOKEN"

# Lấy bài viết của trang công khai
curl "https://graph.facebook.com/v22.0/{page_id}/posts?\
fields=message,created_time,likes.summary(true)&limit=10" \
  -H "Authorization: Bearer $FACEBOOK_USER_TOKEN"
```

### Tìm kiếm bài viết công khai

```bash
# Tìm bài viết công khai theo từ khóa (hạn chế theo chính sách Meta)
curl "https://graph.facebook.com/v22.0/search?q=cho+thue+phong+Da+Lat&type=post&limit=10" \
  -H "Authorization: Bearer $FACEBOOK_USER_TOKEN"
```

> ⚠️ Facebook hạn chế search API rất nhiều từ 2018. Nếu bị lỗi `(#11) Search is not supported`,
> dùng cách khác: tìm nhóm → đọc bài trong nhóm → lọc theo nội dung.

### Ví dụ thực tế: Tìm BĐS cho thuê Đà Lạt

```
Bước 1: Tìm nhóm BĐS Đà Lạt
  → search?q=BDS+cho+thue+Da+Lat&type=group

Bước 2: Lấy bài mới trong nhóm
  → {group_id}/feed?fields=message,created_time&limit=20

Bước 3: AI lọc bài liên quan (cho thuê, giá, khu vực)
  → Agent phân tích nội dung, tóm tắt cho user
```

---

## Quyền cần thiết

### Cho Page Token (quản lý Fanpage)

```
pages_show_list           ← Xem danh sách fanpage
pages_messaging           ← Gửi/nhận tin nhắn Messenger
pages_manage_metadata     ← Quản lý metadata fanpage
pages_manage_posts        ← Đăng bài, xóa bài
pages_read_engagement     ← Đọc likes, comments, shares
pages_read_user_content   ← Đọc nội dung user post trên page
pages_manage_engagement   ← Reply comment, like comment
```

### Cho User Token (tìm kiếm, nhóm)

```
public_profile            ← Mặc định (luôn có)
user_posts                ← Đọc bài viết cá nhân
groups_access_member_info ← Đọc thông tin nhóm + bài trong nhóm
pages_show_list           ← Tìm trang
```

---

## Lưu ý quan trọng

### Facebook cá nhân KHÔNG có API đăng bài
Facebook đã xóa quyền `publish_actions` từ 2018.
**KHÔNG thể** đăng bài lên tường cá nhân qua API.
Chỉ có thể đăng bài lên **Fanpage** (qua Page Token).

### User Token hết hạn 60 ngày
Cần refresh định kỳ. Xem `references/setup-guide.md` phần "Refresh User Token".

### Rate limit
- Page Token: ~200 requests/giờ
- User Token: ~200 requests/giờ
- Nếu bị rate limit: giảm tần suất, dùng batch requests, cache kết quả

### App Mode
App phải ở chế độ **Live** để hoạt động với người dùng khác.
App ở chế độ **Development** chỉ admin/tester mới dùng được.

---

## Cấu trúc thư mục

```
facebook-manager/
├── SKILL.md                    ← File này
├── references/
│   ├── setup-guide.md          ← Hướng dẫn lấy cả 2 loại token
│   └── api-reference.md        ← Danh sách API endpoints đầy đủ
└── scripts/
    └── check-connection.sh     ← Kiểm tra kết nối (cả Page + User)
```
