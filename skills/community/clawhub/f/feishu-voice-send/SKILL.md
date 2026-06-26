---
name: feishu-voice-send
description: Feishu native voice message skill (no ffmpeg needed). Supports multi-language TTS/STT (Chinese, English, etc.) via MiniMax and Edge TTS, with Whisper for receiving.
version: 1.0.3
metadata:
  openclaw:
    requires:
      bins: ["node"]
      python: ["av", "openai-whisper", "soundfile"]
    install:
      - id: edge-tts
        kind: node
        package: edge-tts
        label: Edge TTS (Node.js)
      - id: pyav
        kind: pip
        package: av
        label: PyAV
      - id: whisper
        kind: pip
        package: openai-whisper
        label: Whisper
      - id: soundfile
        kind: pip
        package: soundfile
        label: soundfile
---

# Feishu Voice Send

Send audio as native Feishu voice messages. Supports multi-language TTS (Chinese, English, etc.) and STT via Whisper.

## Features

- 🎙️ **Receive Voice**: receive .ogg voice messages, transcribe to text
- 🔊 **Send Voice**: prefer MiniMax TTS, auto-fallback to Edge TTS when quota is insufficient
- ✅ **Native Format**: sent voice appears as voice bubble in Feishu (not a file)
- 🌍 **Multi-language**: Chinese, English, etc. via MiniMax and Edge TTS

## TTS Engine Selection Logic

```
Send voice request
    ↓
Check MiniMax speech-hd quota (current_interval_total_count - usage_count)
    ↓
Quota > 0 → MiniMax TTS (speech-2.8-hd) ✅
Quota ≤ 0 → Edge TTS (zh-CN-XiaoxiaoNeural) ✅
```

**Quota check**: run `mmx quota show --output json` and look for `speech_generation` category remaining count.

## Architecture

```
User voice → .ogg received → Whisper STT → understand → reply content
                                                              ↓
User ← Feishu voice bubble ← Ogg/Opus convert ← MP3 TTS ← text
                                   ↑                ↑
                           PyAV convert      MiniMax / Edge
```

## Implementation

### Sending Voice (text → Ogg/Opus)

Main entry: `send_feishu_voice_unified.py`

```python
import subprocess, av, os, re, sys, json, tempfile

EDGE_TTS_SCRIPT = "/home/node/.openclaw/plugin-skills/edge-tts/scripts/tts-converter.js"

def check_minimax_quota() -> int:
    result = subprocess.run(['mmx', 'quota', 'show', '--output', 'json'], capture_output=True, text=True)
    data = json.loads(result.stdout)
    for cat in data.get('category_remains', []):
        if cat.get('category') == 'speech_generation':
            return cat.get('current_interval_total_count', 0) - cat.get('current_interval_usage_count', 0)
    return 0

def generate_minimax_tts(text: str) -> str:
    tmp = tempfile.mktemp(suffix='.mp3')
    subprocess.run(['mmx', 'speech', 'synthesize', '--text', text, '--out', tmp], check=True)
    return tmp

def generate_edge_tts(text: str) -> str:
    text_clean = re.sub(r'\b(TTS|语音|文字转语音|text-to-speech)\b', '', text, flags=re.IGNORECASE).strip()
    result = subprocess.run(['node', EDGE_TTS_SCRIPT, text_clean, '--voice', 'zh-CN-XiaoxiaoNeural'], capture_output=True, text=True, check=True)
    return re.search(r'Audio saved to: (.+)', result.stdout).group(1).strip()

def send_voice(text: str) -> str:
    quota = check_minimax_quota()
    mp3_path = generate_minimax_tts(text) if quota > 0 else generate_edge_tts(text)
    return convert_to_ogg(mp3_path)
```

### Format Conversion (MP3 → Ogg/Opus)

Use PyAV to convert TTS MP3 to Feishu native format:
- Container: Ogg
- Codec: libopus
- Sample rate: 16000Hz
- Channels: mono

## Dependencies

| Dependency | Purpose | Install |
|------------|---------|---------|
| `mmx` CLI | MiniMax TTS | Installed, API Key in `~/.mmx/config.json` |
| `edge-tts` (node) | Edge TTS fallback | Installed at `/home/node/.openclaw/plugin-skills/edge-tts/` |
| `PyAV` | Audio format conversion | `pip install av` |
| `Whisper` | Speech recognition | `pip install openai-whisper` |
| `soundfile` | Audio file reading | `pip install soundfile` |
| `openclaw message tool` | Feishu message sending | Built into OpenClaw |

## Files

| File | Description |
|------|-------------|
| `send_feishu_voice_unified.py` | Unified TTS sender (recommended) |
| `send_feishu_voice.py` | Legacy Edge TTS only version |

## Limitations

- Does not support ElevenLabs or other cloud TTS (needs API Key)
- Long audio (>30s) should be segmented
- Feishu Ogg requirements: Ogg container + Opus codec + 16kHz + mono

## Changelog

- 2026-05-28: Added unified version — MiniMax TTS first, auto-fallback to Edge TTS on quota exhaustion
- 2026-05-17: Initial version