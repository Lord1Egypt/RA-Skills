# Feishu Voice Skill - API 参考文档

## Feishu API 端点

### 1. 获取 Tenant Access Token

```bash
POST https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal

请求体:
{
  "app_id": "cli_xxx",
  "app_secret": "xxx"
}

响应:
{
  "code": 0,
  "tenant_access_token": "t-xxx",
  "expire": 7200
}
```

### 2. 上传音频文件

```bash
POST https://open.feishu.cn/open-apis/im/v1/files

Headers:
  Authorization: Bearer <tenant_access_token>
  Content-Type: multipart/form-data

参数:
  type: audio
  file: @/path/to/voice.opus
  file_type: opus  # 关键参数！

响应:
{
  "code": 0,
  "data": {
    "file_key": "file_v3_xxx"
  }
}
```

### 3. 发送语音消息

```bash
POST https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id

Headers:
  Authorization: Bearer <tenant_access_token>
  Content-Type: application/json

请求体:
{
  "receive_id": "oc_xxx",
  "msg_type": "audio",
  "content": "{\"file_key\":\"file_v3_xxx\",\"duration\":5000}"
}

注意：content 必须是 JSON 字符串（双重转义）

响应:
{
  "code": 0,
  "data": {
    "message_id": "om_xxx",
    "msg_type": "audio"
  }
}
```

## NoizAI TTS API

### 生成语音

```bash
POST https://api.noiz.ai/tts

Headers:
  Authorization: <NOIZ_API_KEY>
  Content-Type: application/json

请求体:
{
  "text": "你好世界",
  "speed": 1.0,
  "emotion": "neutral"
}

响应:
音频文件（MP3 格式）
```

## 错误码

| Code | 说明 | 解决方案 |
|------|------|----------|
| 0 | 成功 | - |
| 234001 | 无效请求参数 | 检查 file_type=opus |
| 9499 | 无效参数类型 | 检查 content 格式 |
| 99991663 | Token 无效 | 重新获取 Token |
| 99992402 | 字段验证失败 | 检查 receive_id_type |

## 最佳实践

1. **音频格式**：必须使用 OPUS，采样率 24kHz，比特率 32kbps
2. **时长限制**：单条语音最长 60 秒
3. **文件大小**：不超过 20MB
4. **Token 缓存**：Tenant Access Token 有效期 2 小时，可以缓存复用
5. **错误重试**：网络错误可以重试 2-3 次
