---
name: edge-tts-cantonese
description: Generate Cantonese TTS audio using Edge TTS for WhatsApp and Telegram voice replies. Trigger: voice reply requests.
---

# Edge TTS Cantonese Voice Skill

Use Microsoft Edge TTS to generate natural Cantonese voice audio for WhatsApp and Telegram.

## Voice Parameters
- **Voice:** `zh-HK-HiuMaanNeural`
- **Rate:** varies by tone
- **Pitch:** varies by tone

## Tones

| Tone | Rate | Pitch | Use Case |
|------|------|-------|----------|
| `normal` | +18% | +8Hz | General/neutral |
| `slow` | +0% | +8Hz | Calm/sad |
| `fast` | +24% | +8Hz | Happy/excited |
| `angry` | +36% | +12Hz | Impatient/angry |

## WhatsApp Script

```bash
# 只生成 OGG（適合 WhatsApp voice note）
/home/gabriel/.openclaw/workspace/scripts/edge-tts-voice-ogg.sh "你今日好嗎？" normal

# Slow/sad tone
/home/gabriel/.openclaw/workspace/scripts/edge-tts-voice-ogg.sh "我好傷心..." slow

# Fast/happy tone
/home/gabriel/.openclaw/workspace/scripts/edge-tts-voice-ogg.sh "好開心呀！" fast

# Angry/impatient tone
/home/gabriel/.openclaw/workspace/scripts/edge-tts-voice-ogg.sh "你到底聽唔聽我講？" angry
```

腳本輸出 OGG 路徑，然後可用 WhatsApp 發送命令（例如你現有腳本）傳送。

## Trigger Phrases
- "語音回應"
- "讀俾我聽"
- "用廣東話讀"
- "voice reply"

## Output
- OGG/Opus format ready for WhatsApp / Telegram

## Telegram Send Script
```bash
/home/gabriel/.openclaw/workspace/scripts/edge-tts-telegram.sh <chat_id> "你段文字" normal
```
Example:
```bash
/home/gabriel/.openclaw/workspace/scripts/edge-tts-telegram.sh 8474074290 "主人，我係小蝦。" fast
```
