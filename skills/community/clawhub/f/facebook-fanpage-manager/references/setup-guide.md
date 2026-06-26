# Hướng dẫn lấy Facebook Page ID & Access Token vĩnh viễn

Hướng dẫn chi tiết từng bước, dành cho fanpage cá nhân (không cần Business Portfolio).

> **Yêu cầu:** Tài khoản Facebook cá nhân là Admin của Fanpage cần kết nối.

---

## Bước 1: Đăng ký tài khoản Meta for Developers

1. Truy cập: **https://developers.facebook.com**
2. Click **Get Started** (góc trên phải)
3. Đăng nhập bằng tài khoản Facebook cá nhân — **phải là admin** của fanpage
4. Hoàn tất đăng ký:
   - Chọn vai trò: Developer
   - Xác nhận email
   - Đồng ý điều khoản
5. Sau khi đăng ký xong, bạn đã có tài khoản **Meta for Developers**

---

## Bước 2: Tạo App

1. Truy cập: **https://developers.facebook.com/apps**
2. Click **Tạo ứng dụng** (Create App)
3. Nhập thông tin:
   - **Tên App**: đặt tùy ý (VD: "My Fanpage Bot", "OpenClaw Agent")
   - **Email liên hệ**: email của bạn
4. Click **Tiếp**
5. Chọn trường hợp sử dụng: **Tương tác với khách hàng trên Messenger from Meta**
   (tiếng Anh: "Other" → "Manage Business Integrations" hoặc "Business" type)
6. Click **Tiếp**
7. Ở bước **Doanh nghiệp**: chọn **Không kết nối hồ sơ doanh nghiệp**
8. Click **Tiếp** → Xem lại tổng quan → Click **Tạo ứng dụng**

✅ Bạn đã tạo xong App.

---

## Bước 3: Lấy Page ID và Page Access Token

Đây là bước quan trọng nhất — lấy cả Page ID lẫn Token cùng lúc.

### 3.1. Mở Graph API Explorer

Truy cập: **https://developers.facebook.com/tools/explorer/**

### 3.2. Chọn App

Ở dropdown **"Ứng dụng trên Meta"** (Facebook App) → chọn App vừa tạo ở Bước 2.

### 3.3. Chọn loại token

Ở dropdown **"Người dùng hoặc Trang"** (User or Page) → chọn **"Lấy mã người dùng"** (Get User Token).

### 3.4. Thêm quyền (Permissions)

Click **"Thêm quyền"** (Add Permission), tìm và thêm các quyền sau:

```
pages_show_list          ← Xem danh sách fanpage
pages_messaging          ← Gửi/nhận tin nhắn Messenger
pages_manage_metadata    ← Quản lý metadata fanpage
pages_manage_posts       ← Đăng bài, xóa bài
pages_read_engagement    ← Đọc likes, comments, shares
pages_read_user_content  ← Đọc nội dung người dùng post trên page
```

### 3.5. Generate Token

1. Click **"Generate Access Token"** (nút màu xanh)
2. Popup hiện ra → **chọn Fanpage** cần kết nối
3. Click **Tiếp tục** (Continue)
4. Xem lại quyền truy cập → Click **Lưu** (Save)

### 3.6. Lấy Page ID và Token

Quay lại Graph API Explorer:
1. Trong ô query, xóa nội dung cũ, nhập: `me/accounts`
2. Click **Gửi** (Submit)
3. Kết quả trả về JSON:

```json
{
  "data": [
    {
      "access_token": "EAAG...rất_dài...ZD",
      "category": "...",
      "name": "Tên Fanpage Của Bạn",
      "id": "123456789012345",
      "tasks": ["ADVERTISE", "ANALYZE", "CREATE_CONTENT", "MESSAGING", "MODERATE", "MANAGE"]
    }
  ]
}
```

4. **Sao chép lại 2 giá trị:**
   - `"id"` → đây là **Page ID** (VD: `123456789012345`)
   - `"access_token"` → đây là **Short-lived Page Token** (chỉ có hạn 1-2 giờ!)

⚠️ **Token này sẽ hết hạn sau 1-2 giờ!** Phải đổi sang token vĩnh viễn ở Bước 4.

---

## Bước 4: Đổi sang Token vĩnh viễn

### 4.1. Lấy App ID và App Secret

1. Truy cập: **https://developers.facebook.com/apps**
2. Chọn App đã tạo
3. Vào menu bên trái: **Settings → Basic** (Cài đặt → Cơ bản)
4. Sao chép:
   - **App ID**: dãy số (VD: `1234567890123456`)
   - **App Secret**: click "Show" → sao chép (VD: `abc123def456...`)

### 4.2. Đổi Short-lived → Long-lived User Token

Trong Graph API Explorer, xóa query cũ và nhập:

```
oauth/access_token?grant_type=fb_exchange_token&client_id={APP_ID}&client_secret={APP_SECRET}&fb_exchange_token={TOKEN_TỪ_BƯỚC_3}
```

**Thay thế:**
- `{APP_ID}` → App ID từ bước 4.1
- `{APP_SECRET}` → App Secret từ bước 4.1
- `{TOKEN_TỪ_BƯỚC_3}` → access_token lấy từ ô token ở Explorer (User Token, không phải Page Token)

Click **Submit**. Kết quả trả về:

```json
{
  "access_token": "EAAG...token_mới_rất_dài...ZD",
  "token_type": "bearer"
}
```

Đây là **Long-lived User Token** (có hạn ~60 ngày).

### 4.3. Đổi Long-lived User Token → Permanent Page Token

Trong Graph API Explorer, đặt Long-lived User Token vào ô Access Token, rồi query:

```
me/accounts
```

Click **Submit**. Kết quả trả về access_token mới cho mỗi page — **token này là VĨNH VIỄN** (không hết hạn).

```json
{
  "data": [
    {
      "access_token": "EAAG...PAGE_TOKEN_VĨNH_VIỄN...ZD",
      "id": "123456789012345",
      "name": "Tên Fanpage"
    }
  ]
}
```

### 4.4. Kiểm tra token

Truy cập: **https://developers.facebook.com/tools/debug/accesstoken/**

Dán token vào → Click **Debug**. Xác nhận:
- **Expires**: **Never** (vĩnh viễn)
- **Type**: Page
- **Page ID**: đúng fanpage của bạn

✅ **Bạn đã có Page Token vĩnh viễn!**

---

## Bước 5: Cấu hình vào OpenClaw

Mở file `~/.openclaw/openclaw.json` và thêm:

```json
{
  "skills": {
    "entries": {
      "facebook-fanpage-manager": {
        "env": {
          "FACEBOOK_PAGE_ID": "123456789012345",
          "FACEBOOK_ACCESS_TOKEN": "EAAG...PAGE_TOKEN_VĨNH_VIỄN...ZD"
        }
      }
    }
  }
}
```

### Kiểm tra kết nối

```bash
curl "https://graph.facebook.com/v21.0/$FACEBOOK_PAGE_ID?fields=name,followers_count,fan_count" \
  -H "Authorization: Bearer $FACEBOOK_ACCESS_TOKEN"
```

Nếu trả về JSON có tên fanpage → **THÀNH CÔNG!**

---

## Setup Webhook (cho Messenger auto-reply realtime)

Webhook cho phép Facebook gửi tin nhắn mới đến server của bạn ngay lập tức.

### Yêu cầu

- Server có IP/domain công khai (VPS, ngrok, Cloudflare Tunnel)
- HTTPS (bắt buộc)

### Cách setup

1. Trong App dashboard: **Settings → Webhooks** (hoặc **Messenger → Settings**)
2. Click **Subscribe to Events**
3. Nhập:
   - **Callback URL**: `https://your-server.com/webhook/facebook`
   - **Verify Token**: một chuỗi bí mật bạn tự đặt (VD: `my_verify_token_123`)
4. Chọn subscription fields:
   - `messages` — tin nhắn Messenger
   - `messaging_postbacks` — postback buttons
   - `feed` — bài viết, comment trên page
5. Click **Verify and Save**

### Nếu không có server (dùng polling)

Không cần webhook! Dùng cách polling — gọi API mỗi 30-60 giây để kiểm tra tin nhắn mới:

```bash
curl "https://graph.facebook.com/v21.0/$FACEBOOK_PAGE_ID/conversations?\
fields=messages.limit(1){message,from,created_time}&limit=5" \
  -H "Authorization: Bearer $FACEBOOK_ACCESS_TOKEN"
```

---

## Xử lý sự cố

### Token hết hạn / không hoạt động

**Nguyên nhân:**
- Đổi mật khẩu Facebook
- Gỡ quyền App khỏi fanpage
- App bị vô hiệu hóa

**Cách sửa:** Lặp lại Bước 3 → Bước 4 để lấy token mới.

### Lỗi "App Not Live"

App mới tạo ở chế độ Development — chỉ admin mới dùng được.
Để mọi người dùng: vào App dashboard → **App Review** → chuyển sang **Live**.

### Lỗi quyền (Permissions)

Nếu gặp lỗi `(#200) Requires ... permission`, quay lại Graph API Explorer
và thêm quyền còn thiếu, rồi Generate Token lại.

### Lỗi rate limit

Facebook giới hạn ~200 requests/giờ. Nếu bị rate limit:
- Giảm tần suất gọi API
- Dùng batch requests
- Cache kết quả

---

## Tóm tắt: Bạn cần lưu lại gì?

| Thông tin | Ví dụ | Lưu ở đâu |
|-----------|-------|-----------|
| Page ID | `123456789012345` | openclaw.json |
| Page Access Token (vĩnh viễn) | `EAAG...ZD` | openclaw.json |
| App ID | `1234567890123456` | Ghi chú riêng (dùng khi cần lấy token mới) |
| App Secret | `abc123def456...` | Ghi chú riêng (BẢO MẬT!) |

⚠️ **KHÔNG BAO GIỜ chia sẻ App Secret hay Access Token với người khác!**
