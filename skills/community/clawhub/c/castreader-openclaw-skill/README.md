# CastReader — Read Any Web Page Aloud | OpenClaw Skill

[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-blue)](https://clawhub.com/castreader)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Linux%20%7C%20Windows-lightgrey)]()

**Turn any URL into audio.** CastReader extracts article text from web pages — including sites where other tools fail — and converts it to natural-sounding speech with Kokoro TTS. No API key required.

## Why CastReader?

Every other TTS skill on ClawHub (kokoro-tts, openai-tts, mac-tts, etc.) does the same thing: takes **plain text** and speaks it. But when a user says *"read this article for me"* and pastes a URL, plain-text TTS skills can't help — they have no way to extract the content.

CastReader is the **only skill that handles the full pipeline**: URL in, audio out. It includes a battle-tested extraction engine with dedicated parsers for 15+ platforms, so it works on pages that break generic readability tools.

## Supported Platforms

| Platform | Challenge | CastReader's Approach |
|----------|-----------|----------------------|
| **Kindle Cloud Reader** | Scrambled custom fonts, no readable text in DOM | OCR + glyph mapping to decode font subsets |
| **WeRead (微信读书)** | Text rendered on Canvas, not in DOM | Intercepts fetch API to capture chapter data |
| **Notion** | Complex nested block-based DOM | Dedicated block parser |
| **Google Docs** | Custom rendering engine, no standard HTML | Specialized extractor for Docs DOM |
| **Medium** | Paywall markup, lazy loading | Clean article extraction |
| **Substack** | Newsletter formatting | Structured content parser |
| **arXiv** | LaTeX-rendered papers | Academic content extraction |
| **Wikipedia** | Complex infoboxes, references, citations | Content-focused extraction |
| **ChatGPT / Claude / Gemini** | Dynamic SPA, markdown rendering | AI response extraction with language detection |
| **Douban (豆包) / DeepSeek / Kimi** | Chinese AI platforms | Platform-specific extractors |
| **Feishu (飞书) / Yuque (语雀) / DingTalk** | Chinese productivity tools | Dedicated extractors |
| **Fanqie Novel (番茄小说)** | Novel reader with anti-scraping | Canvas text extraction |
| **Any other website** | Generic articles, blogs, docs | Visible-Text-Block algorithm (Readability + Boilerpipe + JusText fusion) |

## Installation

```bash
clawhub install castreader
```

**Requirements:** Node.js 18+

## Usage

### Extract text from a URL

```bash
node scripts/read-url.js https://en.wikipedia.org/wiki/Text-to-speech 0
```

Returns structured JSON with article info and all paragraph texts (no audio generated):

```json
{
  "title": "Text-to-speech - Wikipedia",
  "language": "en",
  "totalParagraphs": 42,
  "totalCharacters": 18500,
  "paragraphs": ["Speech synthesis is the artificial production of human speech...", "..."]
}
```

### Generate full article audio

```bash
node scripts/read-url.js https://en.wikipedia.org/wiki/Text-to-speech all
```

Extracts content + generates a single MP3 file for the entire article:

```json
{
  "title": "Text-to-speech - Wikipedia",
  "language": "en",
  "totalParagraphs": 42,
  "totalCharacters": 18500,
  "audioFile": "/tmp/castreader-abc123/full.mp3",
  "fileSizeBytes": 2450000
}
```

### Generate summary audio

```bash
echo "Your summary text here..." > /tmp/summary.txt
node scripts/generate-text.js /tmp/summary.txt en
```

Generates audio from any text file:

```json
{
  "audioFile": "/tmp/summary.mp3",
  "fileSizeBytes": 284588
}
```

### Read aloud in the browser (with highlighting)

```bash
node scripts/read-aloud.js https://notion.so/my-page
```

Opens the URL in your browser and triggers CastReader to read with real-time paragraph-level highlighting. Requires the [CastReader Chrome extension](https://chromewebstore.google.com/detail/castreader-tts-reader/foammmkhpbeladledijkdljlechlclpb) installed.

## Messaging Platform Flow (Telegram/Slack/Discord)

When a user sends a URL, CastReader follows a two-step flow:

```
User: https://example.com/article

Bot: 📖 Article Title
     🌐 English · 📝 12 paragraphs · 📊 2,450 chars

     📋 Summary:
     This article explores how AI is transforming industries...

     Reply a number to choose:
     1️⃣ Listen to full article (~2,450 chars, ~12 sec to generate)
     2️⃣ Listen to summary only (~150 chars, ~1 sec to generate)

User: 1

Bot: 🎙️ Generating full audio (~2,450 chars, ~12 seconds)...
Bot: [🔊 full.mp3]
Bot: ✅ Done!
```

**Environment variables:**

| Variable | Default | Description |
|----------|---------|-------------|
| `CASTREADER_VOICE` | `af_heart` | TTS voice selection |
| `CASTREADER_SPEED` | `1.5` | Playback speed |
| `CASTREADER_API_URL` | `http://api.castreader.ai:8123` | API endpoint |

## Comparison with Other TTS Skills

| Feature | CastReader | kokoro-tts | openai-tts | mac-tts |
|---------|-----------|------------|------------|---------|
| URL to audio | Yes | No | No | No |
| Web content extraction | Yes (15+ platforms) | No | No | No |
| Canvas/font-scrambled sites | Yes | No | No | No |
| Full article or summary | Yes | N/A | N/A | N/A |
| Plain text to speech | Yes | Yes | Yes | Yes |
| Paragraph highlighting | Yes | No | No | No |
| API key required | No | No | Yes | No |
| Languages | 40+ | 40+ | 50+ | System voices |
| Cost | Free | Free | Paid | Free |

## How It Works

1. **Extract** — The extraction engine analyzes the page DOM using a 3-tier pipeline:
   - Tier 1: Platform-specific extractors (Kindle, WeRead, Notion, etc.)
   - Tier 2: Learned CSS selector rules from automated evaluation
   - Tier 3: Visible-Text-Block algorithm — a fusion of Readability.js, Boilerpipe, JusText, and CETD techniques
2. **Generate** — Extracted text is sent to the Kokoro TTS API, which returns natural speech with word-level timestamps
3. **Deliver** — Full article audio as a single MP3, or summary-only audio for quick listening

## Links

- **Website:** [castreader.ai](https://castreader.ai)
- **OpenClaw page:** [castreader.ai/openclaw](https://castreader.ai/openclaw)
- **Chrome Web Store:** [CastReader Extension](https://chromewebstore.google.com/detail/castreader-tts-reader/foammmkhpbeladledijkdljlechlclpb)
- **Edge Add-ons:** [CastReader for Edge](https://microsoftedge.microsoft.com/addons/detail/niidajfbelfcgnkmnpcmdlioclhljaaj)
- **ClawHub:** [clawhub.com/castreader](https://clawhub.com/castreader)

## License

MIT
