# Chat Platform Image API Reference

## Feishu (飞书)

### Authentication
```http
POST /open-apis/auth/v3/tenant_access_token/internal
Content-Type: application/json

{
  "app_id": "cli_xxx",
  "app_secret": "xxx"
}
```

### Get Message
```http
GET /open-apis/im/v1/messages/{message_id}
Authorization: Bearer {tenant_access_token}
```

Response includes:
```json
{
  "body": {
    "content": "{\"image_key\":\"img_v3_xxx\"}"
  },
  "msg_type": "image"
}
```

### Download Image
```http
GET /open-apis/im/v1/messages/{message_id}/resources/{image_key}?type=file
Authorization: Bearer {tenant_access_token}
```

### Required Scopes
- `im:message:readonly`
- `im:resource`

---

## DingTalk (钉钉)

### Authentication
```http
POST https://api.dingtalk.com/v1.0/oauth2/accessToken
Content-Type: application/json

{
  "appKey": "dingxxx",
  "appSecret": "xxx"
}
```

Response:
```json
{
  "accessToken": "xxx",
  "expireIn": 7200
}
```

### Get Message (Stream/Webhook)
Robot messages include `downloadCode`:
```json
{
  "msgtype": "picture",
  "content": {
    "downloadCode": "xxx",
    "picURL": "https://..."
  }
}
```

### Download Image (Robot Messages)
```http
GET https://api.dingtalk.com/v1.0/robot/messageFiles/download?downloadCode={downloadCode}
x-acs-dingtalk-access-token: {access_token}
```

### Download Image (User Messages)
For 1-on-1 or group chat images via stream:
```http
GET https://api.dingtalk.com/v1.0/im/conversations/{conv_id}/messages/{message_id}
x-acs-dingtalk-access-token: {access_token}
```

### Required Permissions
- `IMessage` - Read messages
- `Chat` - Access chat content
- `IMessageFile` - Download message files

---

## WeChat / WeCom (企业微信)

### Authentication
```http
GET https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={corp_id}&corpsecret={corp_secret}
```

Response:
```json
{
  "errcode": 0,
  "errmsg": "ok",
  "access_token": "xxx",
  "expires_in": 7200
}
```

### Get Media (Temporary)
```http
GET https://qyapi.weixin.qq.com/cgi-bin/media/get?access_token={access_token}&media_id={media_id}
```

Response: Binary image data

### Message Structure
```json
{
  "MsgType": "image",
  "Image": {
    "MediaId": "xxx",
    "PicUrl": "https://..."
  }
}
```

### Upload Media (for comparison)
```http
POST https://qyapi.weixin.qq.com/cgi-bin/media/upload?access_token={access_token}&type=image
Content-Type: multipart/form-data
```

### Required Permissions
- `media_get` - Download media
- `message_receive` - Receive messages (via callback)

---

## WeChat (个人微信) - Limited Support

Personal WeChat has limited official API. Options:

1. **Webhook/Bot approaches**: Some third-party solutions exist
2. **Bridge solutions**: Use bridges like `wechaty` or `openwechat`
3. **Local file**: User provides local path

When bridged through OpenClaw, images typically come as local file paths.

---

## Discord

### Message Structure
```json
{
  "attachments": [
    {
      "id": "123456789",
      "filename": "image.png",
      "url": "https://cdn.discordapp.com/attachments/xxx/image.png",
      "proxy_url": "https://media.discordapp.net/attachments/xxx/image.png",
      "size": 12345,
      "width": 1920,
      "height": 1080,
      "content_type": "image/png"
    }
  ]
}
```

### Download
Direct download from `url` or `proxy_url` - no authentication needed for public channels.

---

## Telegram Bot API

### Get File Info
```http
GET https://api.telegram.org/bot{token}/getFile?file_id={file_id}
```

Response:
```json
{
  "ok": true,
  "result": {
    "file_id": "AgACAgIAAxkBAAI...",
    "file_unique_id": "AQADevoiG...gAE",
    "file_size": 12345,
    "file_path": "photos/file_0.jpg"
  }
}
```

### Download File
```http
GET https://api.telegram.org/file/bot{token}/{file_path}
```

### Message Types
- `photo`: Array of photo sizes (use largest)
- `document`: General file (check mime_type)
- `sticker`: WebP image

---

## WhatsApp Business API

### Get Media URL
```http
GET https://graph.facebook.com/v17.0/{media_id}
Authorization: Bearer {access_token}
```

Response:
```json
{
  "url": "https://lookaside.fbsbx.com/whatsapp/...",
  "mime_type": "image/jpeg"
}
```

### Download Media
```http
GET {media_url}
Authorization: Bearer {access_token}
```

---

## Signal

Signal uses local attachments when bridged through OpenClaw. The attachment path is typically provided directly in the message metadata.

---

## Slack

### Get File Info
```http
GET https://slack.com/api/files.info?file={file_id}
Authorization: Bearer {bot_token}
```

### Download File
```http
GET {file.url_private_download}
Authorization: Bearer {bot_token}
```

---

## LINE Messaging API

### Get Message Content
```http
GET https://api-data.line.me/v2/bot/message/{message_id}/content
Authorization: Bearer {channel_access_token}
```

---

## iMessage

When bridged through OpenClaw (via BlueBubbles or similar), attachments are typically provided as local file paths.

---

## Common Patterns

### Rate Limits
| Platform | Limit | Window |
|----------|-------|--------|
| Feishu | 100 req/min | Per app |
| DingTalk | 100 req/min | Per app |
| WeChat | 3000 req/min | Per corp |
| Discord | 50 req/sec | Per bot |
| Telegram | 30 req/sec | Per bot |
| WhatsApp | 80 req/hr | Per number |

### Image Size Limits
| Platform | Max Size |
|----------|----------|
| Feishu | 30MB |
| DingTalk | 20MB |
| WeChat | 20MB |
| Discord | 25MB (free) |
| Telegram | 20MB (bot) |
| WhatsApp | 16MB |
| Slack | 1GB |

### Supported Formats
Most platforms support: JPG, PNG, GIF, WebP

---

## Error Codes

### Feishu
- `99991663`: File not found
- `99991664`: File expired
- `99991400`: Permission denied

### DingTalk
- `88`: File not found
- `601`: Token expired
- `600001`: Permission denied

### WeChat
- `40001`: Invalid credential
- `40014`: Invalid access_token
- `42001`: access_token expired

### Telegram
- `400 Bad Request`: Invalid file_id
- `403 Forbidden`: Bot not in chat

### Discord
- `403 Forbidden`: Missing permissions
- `404 Not Found`: Attachment deleted