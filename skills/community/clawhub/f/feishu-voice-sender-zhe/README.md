# Feishu Voice Sender

飞书语音发送器 — 通过飞书 OpenAPI 发送音频文件，以语音消息形式展示（可直接点击播放）。

Send audio files to Feishu as inline voice messages (click to play).

## 安装 | Installation

```bash
# 通过 clawhub 安装（推荐）
clawhub install feishu-voice-sender --workdir ~/.agents

# 或手动克隆到 skills 目录
git clone https://github.com/ZheYanyan/feishu-voice-skill.git ~/.agents/skills/feishu-voice-sender
```

## 使用方法 | Usage

```bash
# 基本用法
python3 ~/.agents/skills/feishu-voice-sender/scripts/feishu_voice_sender.py \
  --file /path/to/audio.mp3

# 指定接收者
python3 ~/.agents/skills/feishu-voice-sender/scripts/feishu_voice_sender.py \
  --file /path/to/audio.mp3 \
  --receive-id ou_xxxxxxxxxx

# 设置环境变量后自动获取接收者
export OPENCLAW_CHAT_ID=ou_xxxxxxxxxx
python3 ~/.agents/skills/feishu-voice-sender/scripts/feishu_voice_sender.py \
  --file /path/to/audio.mp3
```

## 前置要求 | Prerequisites

- Python 3
- curl
- OpenClaw 飞书渠道配置（`~/.openclaw/openclaw.json` 中包含 `channels.feishu.appId` 和 `appSecret`）

## 工作原理 | How It Works

1. 从 OpenClaw 配置读取飞书 `appId` 和 `appSecret`
2. 获取 `tenant_access_token`
3. 上传音频文件（`file_type=opus`）
4. 发送语音消息（`msg_type=audio`）

## 注意事项 | Notes

- 音频文件会被上传到飞书服务器并以语音消息形式发送
- 接收者可以直接在聊天中点击播放，无需下载
- 支持 mp3、m4a、wav 等常见音频格式

## License

MIT
