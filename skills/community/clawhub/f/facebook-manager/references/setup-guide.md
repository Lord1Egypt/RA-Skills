# Hướng dẫn lấy Facebook Access Token

Hướng dẫn chi tiết lấy **cả 2 loại token**: Page Token (vĩnh viễn) và User Token (60 ngày).

> **Yêu cầu:** Tài khoản Facebook cá nhân. Nếu quản lý Fanpage thì phải là Admin.

---

## Bước 1: Đăng ký tài khoản Meta for Developers

1. Truy cập: **https://developers.facebook.com**
2. Click **Get Started**
3. Đăng nhập bằng tài khoản Facebook cá nhân
4. Hoàn tất: chọn vai trò Developer, xác nhận email

---

## Bước 2: Tạo App

1. Truy cập: **https://developers.facebook.com/apps**
2. Click **Tạo ứng dụng** (Create App)
3. Chọn loại: **Other** → **Business**
4. Nhập tên App (VD: "OpenClaw Agent"), email liên hệ
5. Bước Doanh nghiệp: chọn **Không kết nối hồ sơ doanh nghiệp**
6. Click **Tạo ứng dụng**

Lưu lại **App ID** và **App Secret** (Settings → Basic → Show).

---

## Bước 3: Lấy Token qua Graph API Explorer

Truy cập: **https://developers.facebook.com/tools/explorer/**

### 3A: Lấy USER TOKEN (cho tìm nhóm, search)

1. Dropdown **Meta App** → chọn App vừa tạo
2. Dropdown **User or Page** → chọn **Get User Access Token**
3. Click **Add a Permission**, thêm:
   - `public_profile`
   - `user_posts`
   - `groups_access_member_info`
   - `pages_show_list`
4. Click **Generate Access Token** → đồng ý cấp quyền
5. Copy token từ ô Access Token

**Token này là Short-lived (~1-2 giờ).** Đổi sang Long-lived ở Bước 4.

### 3B: Lấy PAGE TOKEN (cho quản lý Fanpage)

1. Giống 3A nhưng thêm quyền:
   - `pages_messaging`
   - `pages_manage_metadata`
   - `pages_manage_posts`
   - `pages_read_engagement`
   - `pages_read_user_content`
   - `pages_manage_engagement`
2. Click **Generate Access Token** → chọn Fanpage → đồng ý
3. Trong ô query, nhập: `me/accounts` → click **Submit**
4. Kết quả JSON:
   - `"id"` → **Page ID**
   - `"access_token"` → **Short-lived Page Token**

---

## Bước 4: Đổi sang Token dài hạn

### 4A: Short-lived → Long-lived User Token (60 ngày)

Trong Graph API Explorer, nhập:

```
oauth/access_token?grant_type=fb_exchange_token&client_id={APP_ID}&client_secret={APP_SECRET}&fb_exchange_token={SHORT_LIVED_USER_TOKEN}
```

Submit → kết quả `access_token` mới có hạn **~60 ngày**.

### 4B: Long-lived User Token → Permanent Page Token

1. Đặt Long-lived User Token vào ô Access Token
2. Query: `me/accounts` → Submit
3. Token trả về cho mỗi page là **VĨNH VIỄN**

### Kiểm tra

Truy cập: **https://developers.facebook.com/tools/debug/accesstoken/**

- **Page Token:** Expires = Never ✅
- **User Token:** Expires = ~60 ngày ✅

---

## Bước 5: Cấu hình vào OpenClaw

```json
{
  "skills": {
    "entries": {
      "facebook-manager": {
        "env": {
          "FACEBOOK_PAGE_ID": "123456789012345",
          "FACEBOOK_PAGE_TOKEN": "EAAG...page_token...ZD",
          "FACEBOOK_USER_TOKEN": "EAAG...user_token...ZD"
        }
      }
    }
  }
}
```

---

## Refresh User Token (mỗi 50 ngày)

```bash
#!/bin/bash
# refresh-fb-token.sh
NEW_TOKEN=$(curl -s "https://graph.facebook.com/v22.0/oauth/access_token?\
grant_type=fb_exchange_token&\
client_id=$APP_ID&\
client_secret=$APP_SECRET&\
fb_exchange_token=$FACEBOOK_USER_TOKEN" | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])")

echo "New token: ${NEW_TOKEN:0:20}..."

# Cập nhật openclaw.json (cần jq)
if command -v jq &>/dev/null; then
  jq --arg t "$NEW_TOKEN" \
    '.skills.entries["facebook-manager"].env.FACEBOOK_USER_TOKEN = $t' \
    ~/.openclaw/openclaw.json > /tmp/oc.json && mv /tmp/oc.json ~/.openclaw/openclaw.json
  echo "Đã cập nhật openclaw.json"
fi
```

Cronjob: `0 0 */50 * * /path/to/refresh-fb-token.sh`

---

## Xử lý sự cố

| Lỗi | Giải pháp |
|-----|-----------|
| `(#200) Requires ... permission` | Thêm quyền → Generate Token lại |
| `Invalid OAuth access token` | Token hết hạn → lấy mới (Bước 3→4) |
| `(#11) Search is not supported` | Dùng cách: tìm nhóm → đọc bài nhóm |
| `App Not Live` | App Dashboard → App Review → chuyển Live |
| Rate limit | Giảm tần suất, batch requests, cache |

⚠️ **KHÔNG BAO GIỜ chia sẻ App Secret hay Token!**
