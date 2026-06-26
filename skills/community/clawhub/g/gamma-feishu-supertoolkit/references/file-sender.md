# 📎 文件发送

支持发送图片、音频、视频、文档等到飞书个人或群聊。

## 功能特性

### 🖼️ 图片
- 直接预览显示（无需点击）
- 支持格式：`.jpg`, `.png`, `.gif`, `.webp`
- 大小限制：<10MB

### 🎵 音频卡片 ⭐
- 自动转换为 OPUS 格式
- 内嵌播放器（进度条 + 时间显示）
- 支持格式：`.mp3`, `.wav`, `.ogg`, `.m4a`
- 大小限制：<100MB
- 要求：飞书客户端 V7.49+

### 🎬 视频
- 文件卡片（点击播放）
- 大视频自动截取封面
- 支持格式：`.mp4`, `.mov`, `.avi`

### 📁 其他文件
- PDF、Word、Excel、压缩包等
- 大小限制：<100MB

## API 端点

### 发送文件
```
POST /messaging/send-file
```

**请求体：**
```json
{
  "file_path": "C:/path/to/file.mp3",
  "receive_id": "ou_xxx",
  "receive_id_type": "open_id",
  "msg_type": "auto"
}
```

**响应：**
```json
{
  "message_id": "xxxxx",
  "msg_type": "interactive",
  "file_type": "audio",
  "file_key": "xxxxx"
}
```

### 发送文本
```
POST /messaging/send-text
```

**请求体：**
```json
{
  "receive_id": "ou_xxx",
  "receive_id_type": "open_id",
  "text": "你好，这是 UTF-8 编码的文本消息"
}
```

### 发送图片（上传）
```
POST /messaging/send-image
Content-Type: multipart/form-data
```

**表单字段：**
- `receive_id`: 接收者 ID
- `receive_id_type`: ID 类型
- `file`: 图片文件

### 发送音频卡片（上传）
```
POST /messaging/send-audio-card
Content-Type: multipart/form-data
```

**表单字段：**
- `receive_id`: 接收者 ID
- `receive_id_type`: ID 类型
- `file`: 音频文件

## 接收者 ID 类型

| 类型 | 说明 | 示例 |
|------|------|------|
| `open_id` | 用户开放 ID（默认） | `ou_ac77807572d24fb3049094acbd93d5f2` |
| `user_id` | 用户 ID | `123456` |
| `chat_id` | 群聊 ID | `oc_xxxxxxxxxxxxx` |
| `email` | 邮箱地址 | `user@example.com` |

## UTF-8 编码支持

所有文本内容自动使用 UTF-8 编码，支持：
- ✅ 简体中文
- ✅ 繁体中文
- ✅ 哈萨克语（西里尔文/阿拉伯文）
- ✅ 其他多语言文本

## 示例

### Python
```python
import requests

# 发送音频卡片
response = requests.post(
    "http://127.0.0.1:8002/messaging/send-file",
    json={
        "file_path": "C:/Music/song.mp3",
        "receive_id": "ou_xxx",
        "receive_id_type": "open_id",
    },
)
print(response.json())
```

### cURL
```bash
# 发送文本
curl -X POST http://127.0.0.1:8002/messaging/send-text \
  -H "Content-Type: application/json" \
  -d '{"receive_id":"ou_xxx","text":"Сәлем, бұл хабарлама"}'
```
