# Facebook Graph API Reference cho Fanpage

API version: v21.0 (cập nhật 2025)
Base URL: `https://graph.facebook.com/v21.0`

---

## Authentication

Mọi request đều cần Header:
```
Authorization: Bearer {PAGE_ACCESS_TOKEN}
```

---

## 1. Fanpage Info

| Endpoint | Method | Mô tả |
|----------|--------|-------|
| `/{PAGE_ID}?fields=name,followers_count,fan_count,about` | GET | Thông tin fanpage |
| `/{PAGE_ID}/picture?type=large` | GET | Avatar fanpage |

## 2. Đăng bài

| Endpoint | Method | Params | Mô tả |
|----------|--------|--------|-------|
| `/{PAGE_ID}/feed` | POST | `message` | Đăng bài text |
| `/{PAGE_ID}/photos` | POST | `url`, `caption` | Đăng ảnh + caption |
| `/{PAGE_ID}/videos` | POST | `file_url`, `description` | Đăng video |
| `/{PAGE_ID}/feed` | POST | `message`, `link` | Đăng bài có link |

## 3. Quản lý bài viết

| Endpoint | Method | Mô tả |
|----------|--------|-------|
| `/{PAGE_ID}/posts?fields=message,created_time,likes.summary(true),comments.summary(true),shares&limit=10` | GET | Danh sách bài viết |
| `/{POST_ID}` | DELETE | Xóa bài viết |
| `/{POST_ID}` | POST | `message` | Sửa bài viết |

## 4. Comments

| Endpoint | Method | Params | Mô tả |
|----------|--------|--------|-------|
| `/{POST_ID}/comments?fields=from,message,created_time` | GET | | Lấy comments |
| `/{COMMENT_ID}/comments` | POST | `message` | Reply comment |
| `/{COMMENT_ID}` | DELETE | | Xóa/ẩn comment |

## 5. Messenger

| Endpoint | Method | Params | Mô tả |
|----------|--------|--------|-------|
| `/{PAGE_ID}/conversations?fields=participants,messages{message,from,created_time}&limit=10` | GET | | Danh sách conversations |
| `/{PAGE_ID}/messages` | POST | JSON body (xem dưới) | Gửi tin nhắn |

### Gửi tin nhắn Messenger

```json
{
  "recipient": {"id": "USER_PSID"},
  "message": {"text": "Nội dung tin nhắn"}
}
```

Gửi ảnh:
```json
{
  "recipient": {"id": "USER_PSID"},
  "message": {
    "attachment": {
      "type": "image",
      "payload": {"url": "https://example.com/image.jpg"}
    }
  }
}
```

Gửi quick replies:
```json
{
  "recipient": {"id": "USER_PSID"},
  "message": {
    "text": "Bạn muốn hỗ trợ gì?",
    "quick_replies": [
      {"content_type": "text", "title": "Giá sản phẩm", "payload": "PRICE"},
      {"content_type": "text", "title": "Tư vấn", "payload": "CONSULT"},
      {"content_type": "text", "title": "Khiếu nại", "payload": "COMPLAINT"}
    ]
  }
}
```

## 6. Insights

| Endpoint | Params | Mô tả |
|----------|--------|-------|
| `/{PAGE_ID}/insights?metric=page_impressions,page_engaged_users,page_fans&period=day` | GET | Thống kê page |
| `/{POST_ID}/insights?metric=post_impressions,post_engaged_users,post_clicks` | GET | Thống kê bài viết |

### Metrics phổ biến

| Metric | Ý nghĩa |
|--------|---------|
| `page_impressions` | Lượt xem page |
| `page_engaged_users` | Người tương tác |
| `page_fans` | Tổng lượt thích page |
| `page_fan_adds` | Lượt thích mới |
| `post_impressions` | Lượt xem bài viết |
| `post_engaged_users` | Người tương tác bài viết |
| `post_clicks` | Lượt click bài viết |

---

## Rate Limits

- ~200 requests/giờ cho mỗi Page token
- Batch requests: tối đa 50 operations/batch
- Nếu bị rate limit: response có header `x-app-usage` với % đã dùng

## Links tham khảo

- Graph API Explorer: https://developers.facebook.com/tools/explorer/
- Access Token Debugger: https://developers.facebook.com/tools/debug/accesstoken/
- Tài liệu chính thức: https://developers.facebook.com/docs/graph-api/
- Messenger Platform: https://developers.facebook.com/docs/messenger-platform/
