---
name: feishu-voice-tts
description: 将文本通过 MOSS-TTS 转换为语音，并发送到飞书群/个人。支持语音消息格式（带波形条）。
---

# 飞书语音 TTS 技能

当用户要求"给飞书发语音"、"在飞书里读这段话"或类似需求时，执行以下流程：

## 核心流程

1. **MOSS-TTS 生成 WAV** → 2. **ffmpeg 转 opus** → 3. **上传飞书** → 4. **发送语音消息**

## 前置要求

- 系统已安装 `ffmpeg`
- 已配置环境变量 `MOSS_API_KEY`（MOSS-TTS API Key）
- 飞书配置在 OpenClaw 安装时已自动完成

## 使用方法

### 命令行模式

```bash
# 基本用法
python scripts/feishu_tts.py --text "要发送的文本" --chat_id "飞书群ID"

# 指定音色
python scripts/feishu_tts.py --text "文本" --voice_id "音色ID" --chat_id "群ID"

# 发送给个人（需要 open_id）
python scripts/feishu_tts.py --text "文本" --receive_id "用户open_id" --receive_id_type "open_id"
```

### 参数说明

| 参数 | 必填 | 说明 |
|------|------|------|
| `--text` | ✅ | 要转语音的文本 |
| `--chat_id` | ❌ | 飞书群 ID（与 receive_id 二选一） |
| `--receive_id` | ❌ | 接收者 ID（open_id 或 chat_id） |
| `--receive_id_type` | ❌ | 接收者类型：`chat_id` 或 `open_id`，默认 `chat_id` |
| `--voice_id` | ❌ | MOSS 音色 ID，默认 `2001286865130360832`（周周） |
| `--output` | ❌ | 输出文件路径，默认 `feishu_voice.wav` |

## 示例

```bash
# 给飞书群发语音
python scripts/feishu_tts.py --text "你好，我是 AI 助手" --chat_id "oc_xxx"

# 给指定用户发语音
python scripts/feishu_tts.py --text "你好" --receive_id "ou_xxx" --receive_id_type "open_id"
```

## 飞书权限要求

确保飞书应用已开通以下权限：
- `im:message:send_as_bot` - 以机器人身份发送消息
- `drive:file:upload` - 上传文件（发送语音消息必需）
- `im:message.group:readonly` - 读取群组消息（获取历史记录必需）
- `im:chat:readonly` - 读取会话列表

> 注意：需要在飞书开放平台应用配置中添加 `drive:file:upload` 权限并发布。

## 获取消息历史

### 脚本：get_history.py

获取飞书群消息历史，按时间排序。

```bash
# 获取最近 24 小时的消息
python scripts/get_history.py --chat_id "oc_xxx"

# 获取最近 1 小时的消息
python scripts/get_history.py --chat_id "oc_xxx" --hours 1

# 获取所有消息
python scripts/get_history.py --chat_id "oc_xxx" --all

# 只显示 audio 类型的消息
python scripts/get_history.py --chat_id "oc_xxx" --type audio

# 显示最近 10 条
python scripts/get_history.py --chat_id "oc_xxx" --limit 10
```

### 参数说明

| 参数 | 必填 | 说明 |
|------|------|------|
| `--chat_id` | ✅ | 飞书群 ID |
| `--hours` | ❌ | 获取最近几小时的消息，默认 24 |
| `--all` | ❌ | 获取所有消息（不使用时间过滤） |
| `--limit` | ❌ | 显示最近多少条消息，默认 30 |
| `--type` | ❌ | 只显示指定类型的消息，如 audio, file, text, image |

### 环境变量

需要设置飞书应用认证：
```bash
FEISHU_APP_ID=你的应用ID
FEISHU_APP_SECRET=你的应用密钥
```
