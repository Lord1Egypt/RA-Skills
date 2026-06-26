---
name: coze-tts
description: Text-to-Speech (TTS) using Coze API. Convert text to natural-sounding speech audio files. Supports multiple voices and output formats (mp3, ogg_opus, wav, pcm).
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["jq"], "env": ["COZE_API_KEY"] },
      },
  }
---

# Coze Text-to-Speech (TTS)

Convert text to natural-sounding speech using Coze API.

## Setup

**1. Get your API Key:**
Get a key from [Coze Platform](https://www.coze.cn/)

**2. Set it in your environment:**
```bash
export COZE_API_KEY="your-key-here"
```

## Supported Output Formats

- **MP3** - Default format, widely compatible
- **OGG_OPUS** - Optimized for streaming and messaging
- **WAV** - Uncompressed audio
- **PCM** - Raw audio data

## Usage

### Basic TTS

Convert text to speech with default settings:

```bash
bash scripts/text_to_speech.sh "你好，这是测试语音"
```

### Save to Specific File

```bash
bash scripts/text_to_speech.sh "你好世界" -o output.mp3
```

### Use Different Voice

```bash
bash scripts/text_to_speech.sh "你好" -v 2
```

### Change Output Format

```bash
bash scripts/text_to_speech.sh "你好" -f ogg_opus
```

### Full Options

```bash
bash scripts/text_to_speech.sh "要转换的文本" -o output.mp3 -v 1 -f mp3
```

**Parameters:**
- `text` (required): Text to convert to speech
- `-o, --output` (optional): Output file path (default: auto-generated)
- `-v, --voice` (optional): Voice ID (default: 1)
- `-f, --format` (optional): Output format - mp3/ogg_opus/wav/pcm (default: mp3)

## Output

The script saves the audio file and outputs:
- File path
- File size
- Audio duration (if ffprobe is available)

Example output:
```
✓ Audio saved: coze_tts_20260324_235030_a1b2c3d4.mp3
  Size: 25.3 KB
  Duration: ~3 seconds
```

## Workflow Examples

### Generate Notification Audio

```bash
bash scripts/text_to_speech.sh "您有一条新消息" -o notification.mp3
```

### Create Voice Greeting

```bash
bash scripts/text_to_speech.sh "欢迎使用 Coze 语音服务" -v 2 -o greeting.mp3
```

### Generate OGG for Messaging

```bash
bash scripts/text_to_speech.sh "你好" -f ogg_opus -o message.ogg
```

### Batch Generate

```bash
for text in "你好" "谢谢" "再见"; do
    bash scripts/text_to_speech.sh "$text" -o "${text}.mp3"
done
```

## Integration with Other Skills

Combine with `coze-asr` for voice conversation:

```bash
# 1. User speaks -> ASR converts to text
bash coze-asr/scripts/speech_to_text.sh input.ogg

# 2. Process text with AI...

# 3. AI response -> TTS converts to speech
bash coze-tts/scripts/text_to_speech.sh "AI的回复" -o response.mp3
```

## Troubleshooting

**Authentication Error:**
- Check COZE_API_KEY is set correctly
- Verify API key has TTS permissions

**Invalid Voice ID:**
- Voice ID should be a number (int64 format)
- Try voice_id: 1 as default

**File Not Created:**
- Check write permissions in output directory
- Ensure sufficient disk space

## Limitations

- Text length limits apply (check Coze documentation)
- Rate limits may apply based on your plan
- Some voices may not support all output formats

## API Reference

- **Endpoint:** `POST https://api.coze.cn/v1/audio/speech`
- **Authentication:** Bearer token (COZE_API_KEY)
- **Content-Type:** application/json

## Required Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `COZE_API_KEY` | Coze API authentication key | Yes |

## Required Tools

| Tool | Purpose | Required |
|------|---------|----------|
| `jq` | JSON processing | Yes |
| `ffprobe` | Audio duration detection | Optional |

## License

MIT
