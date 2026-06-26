---
name: feishu-send-message
description: |
  飞书消息发送工具。支持发送图片和文件。

  **依赖**：读取 ~/.openclaw/openclaw.json 中的飞书应用凭据 (appId, appSecret)

  **当以下情况时使用此 Skill**:
  (1) 需要发送图片给飞书用户或群聊
  (2) 需要发送文件给飞书用户或群聊
  (3) 用户说"发图片"、"发文件"
---

# 飞书消息发送

## 依赖说明

本 skill 需要读取飞书应用凭据来进行 API 认证：

- **凭据位置**: `~/.openclaw/openclaw.json`
- **读取字段**: `appId`, `appSecret`
- **用途**: 调用飞书开放 API 接口进行图片/文件上传和消息发送

## 快速开始

```bash
# 发送图片
feishu_send_message --msg-type image --file-path /path/to/image.jpg --receive-id ou_xxx --receive-id-type open_id

# 发送文件
feishu_send_message --msg-type file --file-path /path/to/file.pdf --receive-id ou_xxx --receive-id-type open_id
```

## 参数说明

| 参数 | 说明 | 必填 | 适用类型 |
|------|------|------|----------|
| --msg-type | 消息类型：`image` 或 `file` | 是 | 全部 |
| --file-path | 文件路径（图片或文件） | 是 | 全部 |
| --receive-id | 接收者 ID（用户 open_id 或群 chat_id） | 是 | 全部 |
| --receive-id-type | 接收者类型：`open_id`（用户）或 `chat_id`（群聊） | 否，默认 open_id | 全部 |

## 使用示例

### 发图片给用户

```bash
feishu_send_message \
  --msg-type image \
  --file-path /tmp/photo.jpg \
  --receive-id ou_xxxxxxxxxxxxxxxxxx \
  --receive-id-type open_id
```

### 发文件到群聊

```bash
feishu_send_message \
  --msg-type file \
  --file-path /tmp/document.pdf \
  --receive-id oc_xxx \
  --receive-id-type chat_id
```

## 消息类型说明

| 类型 | 说明 | 限制 |
|------|------|------|
| image | 图片消息 | 大小不超过 10MB，分辨率不超过 12000×12000 |
| file | 文件消息 | 大小不超过 100MB |

## 支持的文件格式

- **图片**：JPG、JPEG、PNG、WEBP、GIF、BMP、ICO、TIFF、HEIC
- **文件**：根据扩展名自动判断（pdf、doc、xls、ppt、mp4、opus 等），未知类型使用 stream

## 实现原理

1. 从 ~/.openclaw/openclaw.json 读取 appId 和 appSecret
2. 调用飞书 auth API 获取 tenant_access_token
3. 根据消息类型：
   - image: 调用 im/images API 上传图片，获取 image_key
   - file: 调用 im/files API 上传文件，获取 file_key（自动根据扩展名判断 file_type）
4. 调用 im/messages API 发送消息，content 为字符串格式的 JSON

## 依赖

- curl
- sips（macOS 自带，用于图片压缩）
- stat