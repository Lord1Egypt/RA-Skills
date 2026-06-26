# Feishu IM API Reference

## Image APIs

### Upload Image
Upload an image to Feishu server to get an `image_key` for use in messages.

**Endpoint:** `POST /open-apis/im/v1/images`

**Authentication:** Bearer token (tenant_access_token)

**Request:**
- Content-Type: `multipart/form-data`
- Parameters:
  - `image` (file, required): The image file to upload
  - `image_type` (string, required): Always use `"message"`

**Response:**
```json
{
  "code": 0,
  "msg": "success",
  "data": {
    "image_key": "img_v3_02vm_xxxxx"
  }
}
```

**Example:**
```bash
curl -X POST "https://open.larksuite.com/open-apis/im/v1/images" \
  -H "Authorization: Bearer t-xxxxx" \
  -F "image=@/path/to/image.jpg" \
  -F "image_type=message"
```

---

### Download Image
Download an image using its `image_key`.

**Endpoint:** `GET /open-apis/im/v1/images/{image_key}`

**Authentication:** Bearer token (tenant_access_token)

**Path Parameters:**
- `image_key` (string, required): The image key obtained from upload

**Query Parameters:**
- `download` (boolean, optional): Whether to force download. Default: `false`

**Response:**
- Content-Type: Image data (e.g., `image/jpeg`, `image/png`)
- Body: Binary image data

**Example:**
```bash
curl -X GET "https://open.larksuite.com/open-apis/im/v1/images/img_v3_02vm_xxxxx" \
  -H "Authorization: Bearer t-xxxxx" \
  -o downloaded_image.jpg
```

---

## Authentication APIs

### Get Tenant Access Token
Obtain a tenant access token for API authentication.

**Endpoint:** `POST /open-apis/auth/v3/tenant_access_token/internal`

**Request:**
- Content-Type: `application/json`
- Body:
  ```json
  {
    "app_id": "cli_xxxxxx",
    "app_secret": "xxxxxx"
  }
  ```

**Response:**
```json
{
  "code": 0,
  "msg": "ok",
  "tenant_access_token": "t-xxxxxx",
  "expire": 7200
}
```

---

## Message APIs

### Send Message
Send a message to a user or chat.

**Endpoint:** `POST /open-apis/im/v1/messages`

**Authentication:** Bearer token (tenant_access_token)

**Query Parameters:**
- `receive_id_type` (string, required): ID type - `open_id`, `user_id`, `union_id`, or `chat_id`

**Request:**
- Content-Type: `application/json`
- Body:
  ```json
  {
    "receive_id": "ou_xxxxxx",
    "msg_type": "post",
    "content": "{...}"  // JSON string of post content
  }
  ```

**Post Message Content Format:**
```json
{
  "zh_cn": {
    "title": "图片消息",
    "content": [
      [{"tag": "text", "text": "描述文字"}],
      [{"tag": "img", "image_key": "img_v3_xxxxx"}]
    ]
  }
}
```

---

## Error Codes

| Code | Description |
|------|-------------|
| 0 | Success |
| 99992402 | Missing required field (e.g., `receive_id_type`) |
| 230001 | Invalid message content format |
| 11200 | Invalid access token |
| 99991663 | Invalid app_id or app_secret |

---

## Links

- **Upload Image API**: https://open.larksuite.com/document/server-docs/im-v1/image/create
- **Download Image API**: https://open.larksuite.com/document/server-docs/im-v1/image/get
- **Send Message API**: https://open.larksuite.com/document/server-docs/im-v1/message/create
- **Auth API**: https://open.larksuite.com/document/server-docs/authentication-management/access-token/tenant_access_token_internal
