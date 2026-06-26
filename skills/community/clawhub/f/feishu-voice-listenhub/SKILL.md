---
name: feishu-voice-listenhub
description: Send voice messages on Feishu using ListenHub TTS (high-quality Chinese voices). Activate when user wants to send a Feishu voice message using ListenHub, or when comparing Chinese TTS providers. Supports 20+ Chinese voice characters including storytelling, ASMR, broadcast styles.
---

# Feishu Voice — ListenHub TTS

Send high-quality Chinese voice messages on Feishu using ListenHub's TTS engine.

## Prerequisites

- `ffmpeg` / `ffprobe`
- `curl`, `python3`
- ListenHub API key (get from https://listenhub.ai/settings/api-keys)
- Feishu app with `im:message:send_as_bot` and `im:file` permissions

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `LISTENHUB_API_KEY` | ✅ | ListenHub API key (`lh_sk_...`) |
| `FEISHU_APP_ID` | ✅ | Feishu app ID |
| `FEISHU_APP_SECRET` | ✅ | Feishu app secret |
| `LISTENHUB_SPEAKER_ID` | ❌ | Default speaker (default: `chat-girl-105-cn`) |
| `LISTENHUB_LANGUAGE` | ❌ | Language: `zh` or `en` (default: `zh`) |
| `LISTENHUB_TTS_MODE` | ❌ | Mode: `direct` or `smart` (default: `direct`) |

If `FEISHU_APP_ID` / `FEISHU_APP_SECRET` are not in env, extract from openclaw config:

```bash
export FEISHU_APP_ID=$(python3 -c "import json; print(json.load(open('$HOME/.openclaw/openclaw.json'))['channels']['feishu']['appId'])")
export FEISHU_APP_SECRET=$(python3 -c "import json; print(json.load(open('$HOME/.openclaw/openclaw.json'))['channels']['feishu']['appSecret'])")
```

## Sending Voice Messages

```bash
scripts/feishu-voice-send.sh <text> <receive_id> [receive_id_type] [speaker_id]
```

- `receive_id`: target user `open_id` or `chat_id`
- `receive_id_type`: `open_id` (default) or `chat_id`
- `speaker_id`: override default speaker for this message

## Listing Available Speakers

```bash
scripts/list-speakers.sh [language]
```

Examples:
```bash
scripts/list-speakers.sh zh    # Chinese voices only
scripts/list-speakers.sh en    # English voices only
scripts/list-speakers.sh       # All voices
```

## Popular Chinese Speakers

| Speaker ID | Name | Gender | Style |
|---|---|---|---|
| `chat-girl-105-cn` | 晓曼 | female | 日常对话 |
| `gaoqing3-bfb5c88a` | 高晴 | female | 标准女声 |
| `xiaoyun` | 若云 | female | 温柔女声 |
| `xinyi6` | 诗涵 | female | 温柔女声 |
| `ASMR-Female-CN` | 宛星 | female | ASMR 风格 |
| `suzhe-45bbbe54` | 苏哲 | male | 标准男声 |
| `CN-Man-Beijing-V2` | 原野 | male | 北京腔 |
| `pingshu-c7c18f5a` | 古今先生 | male | 评书风格 |

## TTS Modes

- `direct` — 原样朗读文本，不做修改（推荐日常用）
- `smart` — AI 优化文本后再朗读（适合粗稿）

## Important Notes

- ListenHub TTS 是异步的，脚本会自动轮询等待（最长 60 秒）
- 生成的音频自动转为 opus 格式发送到飞书
- 中文语音质量非常高，特别是对话和叙事场景
- `msg_type` 必须是 `"audio"`，OpenClaw 的 `asVoice` 不可用于飞书
