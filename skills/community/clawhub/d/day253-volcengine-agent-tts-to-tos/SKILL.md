---
name: volcengine-agent-tts-to-tos
description: Combined agent that synthesizes speech via Volcengine TTS, uploads the audio to TOS, and returns a presigned temporary URL. Use when users need a shareable audio link from text input.
---

Category: agent

# TTS → TOS → Presigned URL Agent

一步完成：文本 → 语音合成 → 上传对象存储 → 生成临时访问链接。

## Workflow

```
┌──────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  输入文本  │ ──▶ │  TTS 语音合成  │ ──▶ │  上传到 TOS   │ ──▶ │ 生成预签名 URL │
└──────────┘     └──────────────┘     └──────────────┘     └──────────────┘
                   audio bytes           tos://bucket/key       https://...
```

1. 调用火山引擎 TTS HTTP API 合成音频（mp3/wav）
2. 将音频上传到指定 TOS 桶
3. 生成带有效期的预签名 URL
4. 输出完整结果（本地路径 + TOS 路径 + 临时链接）

## Prerequisites

- `pip install requests tos`
- TTS 环境变量：`VOLCENGINE_TTS_APP_ID`, `VOLCENGINE_TTS_TOKEN`, `VOLCENGINE_TTS_CLUSTER`
- TOS 环境变量：`VOLCENGINE_ACCESS_KEY`, `VOLCENGINE_SECRET_KEY`, `VOLCENGINE_TOS_ENDPOINT`, `VOLCENGINE_TOS_REGION`

## Quick start

```bash
# 基本用法：文本 + 目标桶
python agents/tts-to-tos/scripts/tts_to_tos.py \
  --text "你好，这是一段测试语音" \
  --bucket my-bucket

# 完整参数
python agents/tts-to-tos/scripts/tts_to_tos.py \
  --text "欢迎使用火山引擎语音合成服务" \
  --voice-type BV700_streaming \
  --encoding mp3 \
  --bucket my-bucket \
  --key-prefix audio/tts/ \
  --expires 7200 \
  --print-json
```

## Parameters

| 参数 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| `--text` | ✓ | | 要合成的文本 |
| `--bucket` | ✓ | | TOS 目标桶名 |
| `--voice-type` | | `BV700_streaming` | 音色 |
| `--encoding` | | `mp3` | 音频格式 mp3/wav/pcm |
| `--speed-ratio` | | `1.0` | 语速 [0.2, 3] |
| `--volume-ratio` | | `1.0` | 音量 [0.1, 3] |
| `--pitch-ratio` | | `1.0` | 音高 [0.1, 3] |
| `--language` | | | 语言，如 `cn` |
| `--key-prefix` | | `tts/` | TOS 对象键前缀 |
| `--expires` | | `3600` | 预签名 URL 有效期（秒） |
| `--keep-local` | | `false` | 保留本地临时音频文件 |
| `--print-json` | | `false` | 输出 JSON 格式结果 |

## Output

```json
{
  "text": "你好，这是一段测试语音",
  "voice_type": "BV700_streaming",
  "duration_ms": "2150",
  "tos_bucket": "my-bucket",
  "tos_key": "tts/20260308-143025-a1b2c3d4.mp3",
  "presigned_url": "https://my-bucket.tos-cn-beijing.volces.com/tts/...",
  "expires_seconds": 3600,
  "audio_size": 34560
}
```

## Safety

- 不执行任何删除操作
- 本地临时文件默认自动清理（除非 `--keep-local`）
- 预签名 URL 有效期可控，默认 1 小时

## References

- TTS skill: `skills/ai/audio/volcengine-ai-audio-tts/SKILL.md`
- TOS skill: `skills/storage/tos/volcengine-storage-tos/SKILL.md`
