# CastReader — URL to Audio

[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-blue)](https://clawhub.ai/vinxu/castreader)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Linux%20%7C%20Windows-lightgrey)]()

**Paste a URL, get an MP3.** The only OpenClaw skill that extracts article text from any web page and converts it to natural speech. No API key required. Free.

```
User: read this https://paulgraham.com/greatwork.html

Bot:  📖 How to Do Great Work — paulgraham.com
      🌐 English · 📝 85 paragraphs · 📊 12,400 chars

      Reply: 1️⃣ Full article  2️⃣ Summary only

User: 1

Bot:  🎙️ Generating... → 🔊 full.mp3
```

## Install

```bash
clawhub install castreader
```

Requires Node.js 18+.

## What makes it different

Every other TTS skill takes plain text. CastReader is the **only one that handles URLs** — it includes a battle-tested extraction engine with dedicated parsers for 15+ platforms:

| Works on | How |
|----------|-----|
| Notion, Google Docs, Medium, Substack | Dedicated DOM parsers |
| ChatGPT, Claude, Gemini, DeepSeek, Kimi | AI response extraction |
| WeChat Reading (微信读书) | Canvas text via fetch interception |
| Kindle Cloud Reader | OCR + glyph decoding |
| arXiv, Wikipedia | Academic/reference extractors |
| Feishu, Yuque, DingTalk, Fanqie Novel | Chinese platform extractors |
| **Any other website** | Readability + Boilerpipe + JusText fusion algorithm |

## Comparison

| | CastReader | kokoro-tts | openai-tts | mac-tts |
|---|:-:|:-:|:-:|:-:|
| URL → audio | **Yes** | No | No | No |
| Web extraction (15+ sites) | **Yes** | No | No | No |
| Plain text → speech | Yes | Yes | Yes | Yes |
| API key required | **No** | No | Yes | No |
| Languages | 40+ | 40+ | 50+ | System |
| Cost | **Free** | Free | Paid | Free |

## Usage

### URL → audio (one command)

```bash
node scripts/read-url.js "https://example.com/article" all
```

Output:
```json
{
  "title": "Article Title",
  "audioFile": "/tmp/castreader-abc123/full.mp3",
  "fileSizeBytes": 2450000
}
```

### Extract text only (no audio)

```bash
node scripts/read-url.js "https://example.com/article" 0
```

### Text file → audio

```bash
node scripts/generate-text.js /tmp/my-text.txt en
```

### Synced books (WeChat Reading / Kindle)

```bash
node scripts/sync-books.js --list                          # list books
node scripts/sync-books.js --book "<id>" --chapter 3 --audio  # chapter → MP3
```

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `CASTREADER_VOICE` | `af_heart` | Voice selection ([Kokoro voices](https://huggingface.co/hexgrad/Kokoro-82M)) |
| `CASTREADER_SPEED` | `1.5` | Speech speed |
| `CASTREADER_API_URL` | `https://api.castreader.ai` | TTS API endpoint |

## Links

- [CastReader Website](https://castreader.ai)
- [Chrome Extension](https://chromewebstore.google.com/detail/castreader-tts-reader/foammmkhpbeladledijkdljlechlclpb)
- [Edge Add-on](https://microsoftedge.microsoft.com/addons/detail/niidajfbelfcgnkmnpcmdlioclhljaaj)
- [ClawHub Page](https://clawhub.ai/vinxu/castreader)

## License

MIT
