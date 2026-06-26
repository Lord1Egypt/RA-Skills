# Facebook Graph API Reference v22.0

Base URL: `https://graph.facebook.com/v22.0`

---

## Authentication

Mọi request cần Header:
```
Authorization: Bearer {ACCESS_TOKEN}
```

Dùng Page Token cho Fanpage API, User Token cho Search/Group API.

---

## PAGE TOKEN APIs (quản lý Fanpage)

### Thông tin Fanpage
| Endpoint | Method | Mô tả |
|----------|--------|-------|
| `/{PAGE_ID}?fields=name,followers_count,fan_count,about` | GET | Thông tin page |

### Đăng bài
| Endpoint | Method | Params | Mô tả |
|----------|--------|--------|-------|
| `/{PAGE_ID}/feed` | POST | `message` | Đăng bài text |
| `/{PAGE_ID}/photos` | POST | `url`, `caption` | Đăng ảnh |
| `/{PAGE_ID}/videos` | POST | `file_url`, `description` | Đăng video |
| `/{PAGE_ID}/feed` | POST | `message`, `link` | Đăng link |

### Quản lý bài viết
| Endpoint | Method | Mô tả |
|----------|--------|-------|
| `/{PAGE_ID}/posts?fields=message,created_time,likes.summary(true),comments.summary(true)&limit=10` | GET | Danh sách bài |
| `/{POST_ID}` | DELETE | Xóa bài |

### Comments
| Endpoint | Method | Mô tả |
|----------|--------|-------|
| `/{POST_ID}/comments?fields=from,message,created_time` | GET | Lấy comments |
| `/{COMMENT_ID}/comments` | POST | Reply comment (param: `message`) |

### Messenger
| Endpoint | Method | Mô tả |
|----------|--------|-------|
| `/{PAGE_ID}/conversations?fields=participants,messages{message,from,created_time}` | GET | Conversations |
| `/{PAGE_ID}/messages` | POST | Gửi tin nhắn (JSON body) |

Gửi tin nhắn:
```json
{"recipient":{"id":"USER_PSID"},"message":{"text":"Nội dung"}}
```

Gửi quick replies:
```json
{"recipient":{"id":"USER_PSID"},"message":{"text":"Chọn:","quick_replies":[
  {"content_type":"text","title":"Tư vấn","payload":"CONSULT"},
  {"content_type":"text","title":"Giá","payload":"PRICE"}
]}}
```

### Insights
| Endpoint | Mô tả |
|----------|-------|
| `/{PAGE_ID}/insights?metric=page_impressions,page_engaged_users,page_fans&period=day` | Thống kê page |
| `/{POST_ID}/insights?metric=post_impressions,post_engaged_users,post_clicks` | Thống kê bài |

---

## USER TOKEN APIs (tìm kiếm, nhóm)

### Tìm kiếm
| Endpoint | Mô tả |
|----------|-------|
| `/search?q={keyword}&type=group&limit=10` | Tìm nhóm |
| `/search?q={keyword}&type=page&limit=10&fields=name,fan_count,category` | Tìm trang |
| `/search?q={keyword}&type=post&limit=10` | Tìm bài viết (hạn chế) |

### Nhóm
| Endpoint | Mô tả |
|----------|-------|
| `/me/groups?fields=name,member_count,privacy&limit=20` | Nhóm đã tham gia |
| `/{GROUP_ID}/feed?fields=message,from,created_time,attachments&limit=20` | Bài trong nhóm |

### Thông tin cá nhân
| Endpoint | Mô tả |
|----------|-------|
| `/me?fields=id,name,email` | Thông tin user |
| `/me/posts?fields=message,created_time&limit=10` | Bài đã đăng |

---

## Rate Limits

- ~200 requests/giờ cho mỗi token
- Batch requests: tối đa 50 operations/batch
- Header `x-app-usage` cho biết % đã dùng

## Links tham khảo

- Graph API Explorer: https://developers.facebook.com/tools/explorer/
- Token Debugger: https://developers.facebook.com/tools/debug/accesstoken/
- Tài liệu: https://developers.facebook.com/docs/graph-api/
- Permissions: https://developers.facebook.com/docs/permissions/
