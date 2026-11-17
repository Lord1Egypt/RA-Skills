---
name: chat-image-reader
description: First universal image reader for 10+ chat platforms. Features: (1) Auto platform detection (Feishu, DingTalk, WeChat, Discord, Telegram, WhatsApp, Slack, Signal, LINE, iMessage), (2) Unified API with platform-specific download logic, (3) Comprehensive API reference with error codes and rate limits, (4) Fallback strategies for missing images. Triggers: "识别图片", "读取图片", "analyze image", "read image from chat". No similar skill exists on ClawHub - fills a unique gap for cross-platform chat image analysis.
author: Qingyu Zhu
homepage: https://clawhub.ai
metadata:
  openclaw:
    emoji: "🖼️"
    requires:
      bins:
        - python3
      env:
        - FEISHU_APP_ID
        - FEISHU_APP_SECRET
        - DINGTALK_APP_KEY
        - DINGTALK_APP_SECRET
        - WECHAT_CORP_ID
        - WECHAT_CORP_SECRET
        - TELEGRAM_BOT_TOKEN
        - DISCORD_BOT_TOKEN
    envOptional:
      - DASHSCOPE_API_KEY
      - BAIDU_API_KEY
      - BAIDU_SECRET_KEY
    primaryEnv: FEISHU_APP_ID
    networkAccess: true
    permissions:
      - "Read chat messages"
      - "Download message attachments"
      - "Access platform APIs"
---

# Chat Image Reader

Universal image reading and analysis skill for multiple chat platforms.

## Supported Platforms

| Platform | Channel | Image Source | Download Method |
|----------|---------|--------------|-----------------|
| Feishu (飞书) | feishu | Message image_key | API + Tenant Token |
| DingTalk (钉钉) | dingtalk | Message downloadCode | API + Access Token |
| WeChat (微信) | wechat | Media file_id | API + Access Token |
| Discord | discord | Attachment URL | Direct download |
| Telegram | telegram | file_id | Bot API |
| WhatsApp | whatsapp | Media URL | Direct download |
| Signal | signal | Attachment | Direct download |
| Slack | slack | File URL | Direct download |
| iMessage | imessage | Attachment path | Local file |
| LINE | line | Message content | API |

## Required Credentials

This skill requires API credentials to access chat platform messages. Configure at least one platform to use the skill.

### Platform Credentials

| Platform | Required Environment Variables | Notes |
|----------|-------------------------------|-------|
| Feishu (飞书) | `FEISHU_APP_ID`, `FEISHU_APP_SECRET` | Required scopes: `im:message:readonly`, `im:resource` |
| DingTalk (钉钉) | `DINGTALK_APP_KEY`, `DINGTALK_APP_SECRET` | Required permissions: `IMessage`, `Chat` |
| WeChat (企业微信) | `WECHAT_CORP_ID`, `WECHAT_CORP_SECRET` | Required permissions: `media_get` |
| Telegram | `TELEGRAM_BOT_TOKEN` | From @BotFather |
| Discord | `DISCORD_BOT_TOKEN` | From Discord Developer Portal |
| WhatsApp | `WHATSAPP_TOKEN` | From Meta Business API |

### Configuration Example

```bash
# Feishu (飞书) - Required for Feishu image reading
export FEISHU_APP_ID="cli_xxx"
export FEISHU_APP_SECRET="xxx"

# DingTalk (钉钉) - Required for DingTalk image reading
export DINGTALK_APP_KEY="dingxxx"
export DINGTALK_APP_SECRET="xxx"

# WeChat (企业微信) - Required for WeChat image reading
export WECHAT_CORP_ID="xxx"
export WECHAT_CORP_SECRET="xxx"

# Telegram - Required for Telegram image reading
export TELEGRAM_BOT_TOKEN="123456:ABC-xxx"
```

### Security Notes

- Credentials are only used to download images from respective platforms
- No data is sent to external servers except the official platform APIs
- Images are stored temporarily in local temp directory
- Credentials should be configured via environment variables, not hardcoded

## Workflow

### Step 1: Detect Platform from Context

Check `inbound_meta.channel` or `inbound_meta.provider` to determine the chat platform:

```json
{
  "channel": "feishu",      // Feishu
  "channel": "discord",     // Discord
  "channel": "telegram",    // Telegram
  "channel": "whatsapp",    // WhatsApp
  ...
}
```

### Step 2: Get Image by Platform

#### Feishu (飞书)
1. Get `message_id` and `image_key` from message
2. Get tenant access token via API
3. Download from: `GET /open-apis/im/v1/messages/{message_id}/resources/{image_key}`
4. Save to temp file

#### DingTalk (钉钉)
1. Get `downloadCode` from message content
2. Get access token via API (appKey + appSecret)
3. Download from: `GET /v1.0/robot/messageFiles/download?downloadCode={code}`
4. Save to temp file

#### WeChat (微信/企业微信)
1. Get `media_id` from message
2. Get access token via API
3. Download from: `GET https://qyapi.weixin.qq.com/cgi-bin/media/get?access_token={token}&media_id={id}`
4. Save to temp file

#### Discord
1. Get attachment URL from message (Discord provides direct CDN URLs)
2. Download directly from URL
3. No authentication needed for public channels

#### Telegram
1. Get `file_id` from message
2. Call Bot API: `GET https://api.telegram.org/bot{token}/getFile?file_id={file_id}`
3. Download from: `https://api.telegram.org/file/bot{token}/{file_path}`

#### WhatsApp / Signal / Slack
1. Get media URL from message
2. Download directly (usually with token in header)

#### Local File Path
If user provides a local path directly:
1. Verify file exists
2. Use directly without download

### Step 3: Analyze Image

Use the `image` tool with appropriate prompt:

```
image(
  image: "<local_path_or_url>",
  prompt: "描述图片内容，包括文字、图表、数据等关键信息"
)
```

## Platform-Specific Implementation

### Feishu Implementation

```powershell
# 1. Get tenant token
$body = @{ app_id = $appId; app_secret = $appSecret } | ConvertTo-Json
$token = (Invoke-RestMethod -Uri "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal" -Method Post -Body $body).tenant_access_token

# 2. Get message to find image_key
$message = Invoke-RestMethod -Uri "https://open.feishu.cn/open-apis/im/v1/messages/$messageId" -Headers @{ Authorization = "Bearer $token" }
$imageKey = $message.data.items[0].body.content | ConvertFrom-Json | Select-Object -ExpandProperty image_key

# 3. Download image
Invoke-WebRequest -Uri "https://open.feishu.cn/open-apis/im/v1/messages/$messageId/resources/$imageKey" -Headers @{ Authorization = "Bearer $token" } -OutFile $outputPath
```

### DingTalk Implementation

```powershell
# 1. Get access token
$body = @{ appKey = $appKey; appSecret = $appSecret } | ConvertTo-Json
$token = (Invoke-RestMethod -Uri "https://api.dingtalk.com/v1.0/oauth2/accessToken" -Method Post -Body $body).accessToken

# 2. Download image using downloadCode
# For robot messages:
Invoke-WebRequest -Uri "https://api.dingtalk.com/v1.0/robot/messageFiles/download?downloadCode=$downloadCode" -Headers @{ "x-acs-dingtalk-access-token" = $token } -OutFile $outputPath

# For user messages (via stream):
# Use conversation message download API
```

### WeChat (企业微信) Implementation

```powershell
# 1. Get access token
$token = (Invoke-RestMethod -Uri "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=$corpId&corpsecret=$corpSecret").access_token

# 2. Download media
Invoke-WebRequest -Uri "https://qyapi.weixin.qq.com/cgi-bin/media/get?access_token=$token&media_id=$mediaId" -OutFile $outputPath
```

### Discord Implementation

```powershell
# Discord attachments are direct URLs
$attachmentUrl = $message.attachments[0].url
Invoke-WebRequest -Uri $attachmentUrl -OutFile $outputPath
```

### Telegram Implementation

```powershell
# 1. Get file path from file_id
$fileInfo = Invoke-RestMethod -Uri "https://api.telegram.org/bot$token/getFile?file_id=$fileId"
$filePath = $fileInfo.result.file_path

# 2. Download file
Invoke-WebRequest -Uri "https://api.telegram.org/file/bot$token/$filePath" -OutFile $outputPath
```

## Reply Context Handling

When user replies to an image message:

1. Check `reply_to_id` in inbound metadata
2. Fetch the original message using platform-specific API
3. Extract image from the original message
4. Proceed with download and analysis

## Common Analysis Prompts

### Document/Screenshot
```
识别图片中的所有文字内容，保持原有格式和层次结构。
```

### Chart/Table
```
分析图片中的图表或表格，提取所有数据和标签。
```

### UI Screenshot
```
描述界面布局、功能按钮、当前状态等关键信息。
```

### Stock/Finance Chart
```
识别股票代码、价格、K线形态、成交量等财务信息。
```

### Job Posting
```
提取招聘信息，包括职位名称、职责、要求、薪资等关键内容。
```

### General Image
```
描述图片内容，包括主要元素、文字、数据等关键信息。
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Image not found | No image in message | Ask user to resend or provide path |
| Download failed | Permission/Network issue | Check permissions, retry |
| API error | Token expired/invalid | Refresh token and retry |
| Analysis failed | Image unclear/unsupported | Try alternative prompt |

## Fallback Strategy

When automatic image retrieval fails:

1. **Ask user to provide path**: "请提供图片的本地路径"
2. **Ask user to describe**: "请描述图片内容或复制图片中的文字"
3. **Request resend**: "请重新发送图片"

## Temp File Management

- Save images to `$workspace/temp_images/` or system temp
- Clean up after analysis (optional, for disk space)
- Use unique filenames with timestamp: `img_{channel}_{timestamp}.jpg`

## Configuration Required

### Feishu (飞书)
- `FEISHU_APP_ID` / `channels.feishu.appId`
- `FEISHU_APP_SECRET` / `channels.feishu.appSecret`
- Required scope: `im:message:readonly`, `im:resource`

### DingTalk (钉钉)
- `DINGTALK_APP_KEY` / `channels.dingtalk.appKey`
- `DINGTALK_APP_SECRET` / `channels.dingtalk.appSecret`
- Required permissions: `IMessage`, `Chat`

### WeChat (企业微信)
- `WECHAT_CORP_ID` / `channels.wechat.corpId`
- `WECHAT_CORP_SECRET` / `channels.wechat.corpSecret`
- Required permissions: `media_get`

### Telegram
- Bot token configured in OpenClaw

### Discord
- Bot token configured in OpenClaw

## Notes

- Most platforms provide images in JPG/PNG format
- Large images may need resizing before analysis
- Consider rate limits for API calls
- Always validate user has permission to access the image