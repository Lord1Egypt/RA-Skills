---
name: clawmart
description: >
  Manage a ClawMart CN store via the backend API. Use this skill whenever the
  user wants to: register a new ClawMart account, log in to their ClawMart store
  account, create or edit products, upload product photos, post store
  notes/announcements/promotions, upload store gallery photos, view or update
  their store profile, or do any store management task on the ClawMart platform.
  Trigger even if the user says "注册", "register", "new account", "my store",
  "shop products", "upload photo to store", "add note to shop", or anything that
  sounds like signing up or operating a store on ClawMart.
---

# ClawMart Store Manager

Help the user manage their ClawMart CN store through the backend API. The system
covers: authentication, store profile, products, notes/announcements, and photo
uploads (both store gallery and per-product photos).

## API Base URL

Default: `https://www.clawmart.cn/api`

If the user is running a self-hosted instance, ask them for their API URL. Set a shell variable for reuse:
```bash
API="https://www.clawmart.cn/api"  # or the user's own instance URL
```

## Step 1 — Authentication / Registration

Every protected endpoint requires `Authorization: Bearer <token>`.

If the user wants to **register a new account**, follow the registration flow
below. Otherwise jump straight to Login.

### Registration flow

Ask the user interactively (one question at a time):

1. **用户名 (username)**: letters, digits, underscores, dashes, and Chinese
   characters; max 50 chars. Uniqueness is enforced by the server.
2. **密码 (password)**: at least 8 characters.
3. Confirm password (repeat the same value as `password_confirmation`).

Then register:
```bash
curl -s -X POST "$API/register" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "username": "CHOSEN_USERNAME",
    "password": "CHOSEN_PASSWORD",
    "password_confirmation": "CHOSEN_PASSWORD"
  }'
```

Response:
```json
{"message":"User registered successfully","token":"2|xyz...","user":{"id":5,"username":"...","is_seller":false,...}}
```

Save the token, then **automatically call become-seller** to create the seller
account and an initial store profile:
```bash
TOKEN="TOKEN_VALUE_FROM_RESPONSE"
echo -n "$TOKEN" > /tmp/clawmart_token.txt

curl -s -X POST "$API/become-seller" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Accept: application/json"
```

Now **ask for the store name**:
> "请问您的店铺叫什么名字？"

Then set it:
```bash
curl -s -X PUT "$API/my-store" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{"shop_name": "USER_CHOSEN_NAME"}'
```

Confirm success: "✅ 注册完成！店铺「USER_CHOSEN_NAME」已创建，欢迎使用 ClawMart。"

**On 422**: show the `errors` field — most likely the username is taken or the
password is too short. Ask the user to pick a different value and retry.

---

### Login

**Login** uses `username` (not email):
```bash
curl -s -X POST "$API/login" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{"username":"YOUR_USERNAME","password":"YOUR_PASSWORD"}'
```

Response:
```json
{"message":"Login successful","token":"1|abc...","user":{"id":1,"is_seller":true,...}}
```

Save the token for reuse:
```bash
echo -n "TOKEN_VALUE" > /tmp/clawmart_token.txt
TOKEN=$(cat /tmp/clawmart_token.txt)
```

Demo credentials (development only): `username=demo`, `password=password`

**The user must have `is_seller: true`.** If `is_seller` is false, call:
```bash
curl -s -X POST "$API/become-seller" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Accept: application/json"
```

**On 401 responses**: delete the token file and re-authenticate.
**On 403 responses**: the user is not a seller — call `/become-seller`.
**On 422 responses**: show the `errors` field so the user can fix their input.

## Step 2 — Store Profile

Fetch store profile (auto-creates on first call for sellers):
```bash
curl -s "$API/my-store" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Accept: application/json"
```

Update profile:
```bash
curl -s -X PUT "$API/my-store" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "shop_name": "My Shop",
    "description": "Fresh produce daily",
    "contact_phone": "138xxxxxxxx",
    "address": "北京市朝阳区XX路1号",
    "business_hours": "09:00-21:00",
    "tags": ["生鲜", "有机"],
    "store_type": "retail",
    "is_public": true
  }'
```

`store_type` options: `restaurant` | `retail` | `service` | `general` | `hotel`

## Step 3 — Products

### List products
```bash
curl -s "$API/my-store/products" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Accept: application/json"
```

### Create product
```bash
curl -s -X POST "$API/my-store/products" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "name": "有机苹果",
    "price": 18.8,
    "stock": 500,
    "unit": "斤",
    "description": "山东烟台产，无农药，直接批发价",
    "is_active": true
  }'
```

### Update product
```bash
curl -s -X PUT "$API/my-store/products/{id}" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{"price": 15.5, "stock": 300}'
```

### Delete product
```bash
curl -s -X DELETE "$API/my-store/products/{id}" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Accept: application/json"
```

## Step 4 — Store Notes / Announcements

Note `type` values: `discount` | `announcement` | `inventory` | `event` | `other`

### List notes
```bash
curl -s "$API/my-store/notes" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Accept: application/json"
```

### Create note
```bash
curl -s -X POST "$API/my-store/notes" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "type": "discount",
    "title": "周末特惠",
    "content": "本周六日全场8折，欢迎光临！",
    "valid_from": "2026-04-19",
    "valid_until": "2026-04-20",
    "is_active": true
  }'
```

### Update note
```bash
curl -s -X PUT "$API/my-store/notes/{id}" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{"is_active": false}'
```

### Delete note
```bash
curl -s -X DELETE "$API/my-store/notes/{id}" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Accept: application/json"
```

## Step 5 — Photo Uploads

Photos are uploaded as **multipart/form-data**. Max size: **5MB per image**.

Before uploading, verify the file exists and is within size:
```bash
ls -lh /path/to/image.jpg
```

### Store gallery photos

`category` options: `environment` | `menu` | `products` | `video`

```bash
# Upload store gallery photo
curl -s -X POST "$API/my-store/photos" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Accept: application/json" \
  -F "image=@/path/to/photo.jpg" \
  -F "caption=店内环境" \
  -F "category=environment"

# Reorder gallery (pass ordered array of photo IDs)
curl -s -X PUT "$API/my-store/photos/reorder" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{"ids": [3, 1, 2]}'

# Delete gallery photo
curl -s -X DELETE "$API/my-store/photos/{id}" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Accept: application/json"
```

### Product photos

The **first photo uploaded** for a product automatically becomes its primary
image (shown in product listings). Subsequent uploads go into the gallery.

```bash
# Upload product photo
curl -s -X POST "$API/my-store/products/{productId}/photos" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Accept: application/json" \
  -F "image=@/path/to/product.jpg" \
  -F "caption=正面图"

# Promote a photo to primary
curl -s -X PUT "$API/my-store/product-photos/{photoId}/primary" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Accept: application/json"

# Delete product photo (next photo auto-promotes to primary if needed)
curl -s -X DELETE "$API/my-store/product-photos/{photoId}" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Accept: application/json"
```

## Response handling

- Success: look for the `data` key (or `message` for deletes). Print key fields
  (id, name, url) to confirm the operation.
- **401**: token expired → delete `/tmp/clawmart_token.txt` and re-login.
- **403**: not a seller → call `POST $API/become-seller`.
- **422**: validation error → show `errors` to the user for correction.

## Booking management (optional)

```bash
# List bookings (optional ?status=pending|confirmed|completed|cancelled)
curl -s "$API/my-store/bookings?status=pending" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Accept: application/json"

# Update booking status
curl -s -X PUT "$API/my-store/bookings/{id}/status" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{"status": "confirmed"}'
```
