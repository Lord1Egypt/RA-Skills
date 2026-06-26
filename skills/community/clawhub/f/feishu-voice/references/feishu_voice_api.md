# 飞书语音消息 API 参考

## 接口信息

### 获取访问令牌
- **接口**: `POST /auth/v3/tenant_access_token/internal`
- **用途**: 获取飞书 API 访问令牌

### 上传文件
- **接口**: `POST /im/v1/files`
- **用途**: 上传语音文件到飞书服务器

**关键参数**:
- `file_type=opus` - 文件类型必须是 opus
- `duration` - 音频时长（毫秒，整数）

### 发送消息
- **接口**: `POST /im/v1/messages?receive_id_type=open_id`
- **用途**: 发送语音消息

**消息格式**:
```json
{
  "receive_id": "ou_xxx",
  "msg_type": "audio",
  "content": "{\"file_key\": \"xxx\", \"duration\": 6000}"
}
```

## 音频格式要求

| 参数 | 要求 |
|------|------|
| 格式 | opus (OGG 容器) |
| 编码 | libopus |
| 比特率 | 24k |
| 采样率 | 24000 Hz |
| 声道 | 单声道 |

## 环境变量说明

### 必需变量

| 变量名 | 说明 |
|--------|------|
| FEISHU_APP_ID | 飞书应用 ID |
| FEISHU_APP_SECRET | 飞书应用密钥 |
| COZE_API_KEY | Coze API 密钥 |

### 可选变量

| 变量名 | 说明 |
|--------|------|
| FEISHU_RECEIVER | 默认接收者 Open ID |
| FEISHU_APP_ID_B | 应用 B 的 ID（多应用场景） |
| FEISHU_APP_SECRET_B | 应用 B 的密钥 |
| FEISHU_RECEIVER_B | 应用 B 的接收者 |
| OPENCLAW_WORKSPACE | OpenClaw 工作区目录路径 |

## TTS 脚本路径解析

脚本会按以下顺序尝试找到 coze-tts：

1. **相对路径**: `../coze-tts/scripts/text_to_speech.sh`（相对于当前技能目录）
2. **环境变量**: `$OPENCLAW_WORKSPACE/skills/coze-tts/scripts/text_to_speech.sh`
3. **常见路径**: 尝试 `$HOME/.openclaw/workspace`、`$HOME/openclaw/workspace`、`/opt/openclaw/workspace`

## 官方文档

https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/message/create
