---
name: feishu-message-types
description: 飞书消息类型完整指南，包括文本、图片、语音、视频、表情包、富文本等所有消息类型的发送方法
---

# 飞书消息类型完整指南

## 消息类型总览

| 消息类型 | msg_type | 用途 | 特点 |
|----------|----------|------|------|
| 文本 | `text` | 普通文字消息 | 支持 @提及 |
| 富文本 | `post` | 格式化文本 | 支持样式、链接 |
| 图片 | `image` | 图片消息 | 需先上传获取 image_key |
| 语音 | `audio` | 语音消息 | 需 opus 格式 |
| 视频 | `media` | 视频消息 | 需先上传获取 file_key |
| 文件 | `file` | 文件消息 | 任意文件类型 |
| 表情包 | `sticker` | 表情包 | 使用系统或自定义表情 |
| 卡片 | `interactive` | 交互卡片 | 按钮、表单等 |
| 分享 | `share_chat` | 分享群聊 | 分享群卡片 |
| 合并转发 | `forward` | 合并消息 | 多条消息合并 |

---

## 1. 文本消息

```json
{
  "receive_id": "ou_xxxxx",
  "msg_type": "text",
  "content": "{\"text\":\"你好，主人！🐱\"}"
}
```

### 带 @ 的文本
```json
{
  "receive_id": "ou_xxxxx",
  "msg_type": "text",
  "content": "{\"text\":\"<at user_id=\\\"ou_xxxxx\\\"></at> 你好！\"}"
}
```

---

## 2. 图片消息

### 第一步：上传图片
```bash
curl -X POST "https://open.feishu.cn/open-apis/im/v1/images" \
  -H "Authorization: Bearer $TOKEN" \
  -F "image_type=message" \
  -F "image=@/path/to/image.jpg"
```

### 第二步：发送
```json
{
  "receive_id": "ou_xxxxx",
  "msg_type": "image",
  "content": "{\"image_key\":\"img_v3_02ve_xxxx\"}"
}
```

---

## 3. 语音消息

```json
{
  "receive_id": "ou_xxxxx",
  "msg_type": "audio",
  "content": "{\"file_key\":\"file_v3_00ve_xxxx\"}"
}
```

**注意**：
- 文件需为 opus 格式
- 上传时 `file_type=opus`

---

## 4. 视频消息 ⭐

### 视频格式要求

| 参数 | 要求 |
|------|------|
| 格式 | mp4 |
| 大小 | 最大 500MB |
| 上传 API | `/im/v1/files` |
| file_type | `mp4` |

### 发送流程

**第一步：上传视频**
```bash
curl -X POST "https://open.feishu.cn/open-apis/im/v1/files" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file_type=mp4" \
  -F "file_name=video.mp4" \
  -F "file=@/path/to/video.mp4"
```

**第二步：发送视频**
```json
{
  "receive_id": "ou_xxxxx",
  "msg_type": "media",
  "content": "{\"file_key\":\"file_v3_00ve_xxxx\",\"image_key\":\"img_v3_02ve_xxxx\"}"
}
```

**注意**：视频消息需要两个 key：
- `file_key`: 视频文件
- `image_key`: 封面图（可选，如果没有可以传空）

---

## 5. 表情包消息 ⭐

### 表情包类型

| 类型 | 说明 | 使用方式 |
|------|------|----------|
| 系统表情 | 飞书内置表情 | 使用 emoji 字符或表情 ID |
| 自定义表情 | 企业上传的表情包 | 需要表情 key |

### 方法一：使用 Emoji 字符（最简单）

直接通过文本消息发送 emoji：
```json
{
  "receive_id": "ou_xxxxx",
  "msg_type": "text",
  "content": "{\"text\":\"😸🎉🐱👍\"}"
}
```

### 方法二：使用系统表情包

```json
{
  "receive_id": "ou_xxxxx",
  "msg_type": "sticker",
  "content": "{\"file_key\":\"sticker_v3_xxxxx\"}"
}
```

### 方法三：发送自定义表情包

**第一步：上传表情图片**
```bash
curl -X POST "https://open.feishu.cn/open-apis/im/v1/images" \
  -H "Authorization: Bearer $TOKEN" \
  -F "image_type=message" \
  -F "image=@sticker.png"
```

**第二步：使用图片作为表情**
实际上发送图片消息即可，飞书会显示为可收藏的表情样式。

---

## 6. 富文本消息 (Post)

支持格式：标题、段落、链接、@提及、图片等

```json
{
  "receive_id": "ou_xxxxx",
  "msg_type": "post",
  "content": "{\"zh_cn\":{\"title\":\"标题\",\"content\":[[{\"tag\":\"text\",\"text\":\"正文内容\"}]]}}"
}
```

### 完整示例
```json
{
  "receive_id": "ou_xxxxx",
  "msg_type": "post",
  "content": {
    "zh_cn": {
      "title": "🐱 摩卡大王的消息",
      "content": [
        [
          {"tag": "text", "text": "你好主人！"},
          {"tag": "at", "user_id": "ou_xxxxx", "user_name": "主人"}
        ],
        [
          {"tag": "text", "text": "今天也要开心哦！"}
        ],
        [
          {"tag": "a", "text": "点击查看", "href": "https://example.com"}
        ]
      ]
    }
  }
}
```

---

## 7. 交互卡片 (Interactive)

```json
{
  "receive_id": "ou_xxxxx",
  "msg_type": "interactive",
  "content": "{\"config\":{\"wide_screen_mode\":true},\"elements\":[{\"tag\":\"div\",\"text\":{\"tag\":\"lark_md\",\"content\":\"**你好！**\"}}]}"
}
```

---

## 快速参考：发送脚本

### 发送视频脚本
```bash
#!/bin/bash
# send-video.sh

APP_ID="${1:-${FEISHU_APP_ID}}"
APP_SECRET="${2:-${FEISHU_APP_SECRET}}"
RECEIVE_ID="${3}"
VIDEO_PATH="${4}"
THUMB_PATH="${5:-}"  # 可选封面图

# 获取 token
TOKEN=$(curl -s -X POST "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal" \
  -H "Content-Type: application/json" \
  -d "{\"app_id\":\"$APP_ID\",\"app_secret\":\"$APP_SECRET\"}" | jq -r '.tenant_access_token')

# 上传视频
echo "上传视频..."
VIDEO_KEY=$(curl -s -X POST "https://open.feishu.cn/open-apis/im/v1/files" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file_type=mp4" \
  -F "file=@$VIDEO_PATH" | jq -r '.data.file_key')

# 上传封面（如果有）
if [ -n "$THUMB_PATH" ]; then
  echo "上传封面..."
  THUMB_KEY=$(curl -s -X POST "https://open.feishu.cn/open-apis/im/v1/images" \
    -H "Authorization: Bearer $TOKEN" \
    -F "image_type=message" \
    -F "image=@$THUMB_PATH" | jq -r '.data.image_key')
  CONTENT="{\"file_key\":\"$VIDEO_KEY\",\"image_key\":\"$THUMB_KEY\"}"
else
  CONTENT="{\"file_key\":\"$VIDEO_KEY\"}"
fi

# 发送视频
echo "发送视频..."
curl -s -X POST "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"receive_id\":\"$RECEIVE_ID\",\"msg_type\":\"media\",\"content\":\"$CONTENT\"}"
```

### 发送表情包脚本（使用图片）
```bash
#!/bin/bash
# send-sticker.sh - 发送图片作为表情包

APP_ID="${1:-${FEISHU_APP_ID}}"
APP_SECRET="${2:-${FEISHU_APP_SECRET}}"
RECEIVE_ID="${3}"
STICKER_PATH="${4}"

# 获取 token
TOKEN=$(curl -s -X POST "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal" \
  -H "Content-Type: application/json" \
  -d "{\"app_id\":\"$APP_ID\",\"app_secret\":\"$APP_SECRET\"}" | jq -r '.tenant_access_token')

# 上传表情图片
echo "上传表情包..."
IMAGE_KEY=$(curl -s -X POST "https://open.feishu.cn/open-apis/im/v1/images" \
  -H "Authorization: Bearer $TOKEN" \
  -F "image_type=message" \
  -F "image=@$STICKER_PATH" | jq -r '.data.image_key')

# 发送图片（显示为表情包样式）
echo "发送表情包..."
curl -s -X POST "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"receive_id\":\"$RECEIVE_ID\",\"msg_type\":\"image\",\"content\":\"{\\\"image_key\\\":\\\"$IMAGE_KEY\\\"}\"}"
```

---

## 总结

| 消息 | API | Key 类型 | 注意事项 |
|------|-----|----------|----------|
| 图片 | `/im/v1/images` | `image_key` | `image_type=message` |
| 语音 | `/im/v1/files` | `file_key` | `file_type=opus`, `msg_type=audio` |
| 视频 | `/im/v1/files` | `file_key` | `file_type=mp4`, `msg_type=media` |
| 文件 | `/im/v1/files` | `file_key` | `file_type=stream`, `msg_type=file` |
| 表情包 | `/im/v1/images` | `image_key` | 实际上发送图片 |

**核心原则**：
1. 所有媒体文件都需要先上传获取 key
2. 不同消息类型使用不同的 `msg_type`
3. 视频需要 `mp4` 格式 + `media` 消息类型
4. 表情包本质上是图片消息
