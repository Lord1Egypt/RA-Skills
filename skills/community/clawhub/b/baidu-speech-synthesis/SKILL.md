---
name: baidu-speech-synthesis
description: Baidu Intelligent Cloud Speech Synthesis (TTS), supporting multi-role dialogue audio generation, SSML/segment-merge dual modes, speech rate/pitch adjustment.
metadata: { "openclaw": { "emoji": "🔊", "requires": { "bins": ["python3", "ffmpeg"], "env": ["BAIDU_API_KEY", "BAIDU_SECRET_KEY"] }, "primaryEnv": "BAIDU_API_KEY" } }
---

# Baidu Intelligent Cloud Speech Synthesis Skill

## Triggers
Use this skill when the user mentions:
- "Convert this dialogue to audio using Baidu TTS"
- "Generate male-female dialogue, male voice using Duxiaoyao, female voice using Duxiaomei"
- "Batch process all dialogues in dialogue.txt"
- "Adjust speech rate to 7, pitch to 6"
- "View available voice list"
- "baidu tts", "dialogue to audio", "multi-speaker speech synthesis"
- "baidu speech synthesis", "multi-speaker dialogue", "Baidu TTS"

**Chinese triggers (for Chinese users):**
- "用百度TTS把这段对话转成音频"
- "生成男女对话，男声用度逍遥，女声用度小美"
- "批量处理 dialogue.txt 里的所有对话"
- "调整语速到7，音调到6"
- "查看可用的音色列表"

## Overview
This skill calls the Baidu Intelligent Cloud Speech Synthesis API, supporting multi-speaker dialogue synthesis (SSML mode or segment-merge fallback). It provides rich voice selection, speech rate/pitch/volume adjustment, and can automatically convert text dialogues into audio files with character-specific voices.

## Installation Dependencies
```bash
# Install Python dependencies
pip install requests

# Ensure ffmpeg is installed (required for audio merging)
# Ubuntu/Debian:
sudo apt install ffmpeg
# macOS:
brew install ffmpeg
# Windows: Download from https://ffmpeg.org/download.html

# Optional: If pydub is needed (alternative merging solution)
# pip install pydub
```

## Environment Variables Setup
Choose one of three authentication methods:

### Method 1: API Key + Secret Key (auto-token)
```bash
export BAIDU_API_KEY="Your API Key (non-bce-v3 format)"
export BAIDU_SECRET_KEY="Your Secret Key"
```

### Method 2: Direct access_token (starts with `1.`)
```bash
export BAIDU_API_KEY="YOUR_ACCESS_TOKEN"
# BAIDU_SECRET_KEY not required
```

### Method 3: IAM Key (starts with `bce-v3/`)
```bash
export BAIDU_API_KEY="YOUR_IAM_KEY_HERE"
# BAIDU_SECRET_KEY not required
# Note: Existing bce-v3/ALTAK-... keys may be dedicated to other services (e.g., search).
# If authentication fails, create a dedicated speech synthesis application to get API Key + Secret Key.
```

## Required Environment Variables
`BAIDU_API_KEY` must be set. Whether `BAIDU_SECRET_KEY` is needed depends on the authentication method:

### Method 1: API Key + Secret Key (auto-token)
```bash
BAIDU_API_KEY=Your API Key (non-bce-v3 format)
BAIDU_SECRET_KEY=Your Secret Key
```

### Method 2: Direct access_token (starts with `1.`)
```bash
BAIDU_API_KEY=YOUR_ACCESS_TOKEN
# BAIDU_SECRET_KEY not required
```

### Method 3: IAM Key (starts with `bce-v3/`)
```bash
BAIDU_API_KEY=YOUR_IAM_KEY_HERE
# BAIDU_SECRET_KEY not required
```

The skill scripts automatically detect the key format and choose the corresponding authentication method. If not set, the user will be prompted.

## Usage
### 1. Direct script invocation (command line)
```bash
# Single dialogue file synthesis
python ~/.openclaw/skills/baidu-speech-synthesis/scripts/baidu_tts.py \
    --input dialogue.txt \
    --output conversation.mp3

# Specify voice mapping (character name → voice code)
python scripts/baidu_tts.py \
    --input script.txt \
    --map 小明:1 小红:0 老师:106

# Batch process all .txt files in a directory
python scripts/baidu_tts.py \
    --dir ./dialogues \
    --format mp3

# Adjust parameters
python scripts/baidu_tts.py \
    --input text.txt \
    --spd 7 --pit 6 --vol 5 \
    --aue 3
```

### 2. Usage in OpenClaw sessions
When the user triggers the above phrases, the skill will:
1. Check environment variable configuration
2. Ask or automatically identify input text/file
3. Generate SSML according to default or specified voice assignment scheme
4. Call the Baidu API and return the audio file (can be played automatically or saved)

## File Structure
```
baidu-speech-synthesis/
├── SKILL.md                    # This file
├── scripts/
│   ├── baidu_tts.py            # Main API client (token acquisition, SSML requests, segment merging)
│   ├── dialogue_formatter.py   # Dialogue text → SSML conversion and voice mapping
│   └── audio_merger.py         # ffmpeg audio merging tool (segment merge solution)
└── references/
    ├── voice_list.md           # Voice code table, samples, recommended pairings
    ├── ssml_guide.md           # Baidu SSML tags, limitations, examples
    └── api_setup.md            # How to obtain keys, free quota (5 million chars/month), authentication details
```

## Technical Points
- **Intelligent Mode Selection**: Automatically detects multi-voice requirements, defaults to segment synthesis mode (Baidu API only supports single-voice SSML).
- **Segment Synthesis Solution**: Splits multi-role dialogues into single-voice segments → synthesizes separately → merges with ffmpeg (solves API limitations, compatible with Python 3.13).
- **SSML Single-Voice Support**: Supports single-voice SSML (`tex_type=3`) for complex speech expressions of individual characters.
- **Automatic Voice Assignment**: Default mapping "老王" → Duxiaoyao (3), "张经理" → Duxiaoyu (1), "小李" → Duyaya (4), customizable via `--map`.
- **Error Handling**: Friendly prompts for network timeouts, quota exhaustion, audio merge failures, etc.

## Notes
- **Free Quota**: Baidu Speech Synthesis provides **5 million characters/month** free quota (2026 latest policy), pay-as-you-go beyond that.
- **Authentication Methods**: Supports three authentication methods (API Key+Secret Key, access_token, IAM Key), automatically detected by skill.
- **SSML Limitations**: SSML text length limited to 1024 bytes (note Chinese character count), recommend each sentence not exceed 120 characters.
- **Dependencies**: Segment merge solution requires `ffmpeg` installation (skill will detect and prompt). No need to install pydub.
- **Voice Expressiveness**: Baidu's base voices are relatively flat; recommend enhancing dialogue expressiveness through text optimization (adding语气词, emotional descriptions).
- **Key Security**: Do not hardcode API keys in code; always use environment variables or `.env` files.
- **Error Handling**: Detailed guidance provided for authentication failures; refer to `references/api_setup.md` for help.

## Changelog
- **2026‑05‑09 (v1.2.6)**: Removed _backup_tests directory to fix ClawHub security scan flags.
- **2026‑03‑31 (v1.2.4)**: Removed test files from package, requested security rescan.
- **2026‑03‑31 (v1.2.3)**: Fixed bare `except:` statements in `audio_merger.py`; replaced with proper exception handling to improve debugging and error visibility.
- **2026‑03‑26 (v1.2.2)**: Added MIT LICENSE file; updated metadata to declare ffmpeg dependency; addressing ClawHub security warnings.
- **2026‑03‑26 (v1.2.1)**: Complete English translation of skill documentation; improved bilingual triggers for both English and Chinese users.
- **2026‑03‑26 (v1.2)**: Switched to ffmpeg instead of pydub, solving Python 3.13 compatibility issues; corrected Baidu API limitation description (only supports single-voice SSML); optimized documentation and default voice mapping.
- **2026‑03‑26 (v1.1)**: Enhanced authentication support, added IAM Key and direct access_token authentication, updated free quota information, improved error guidance.
- **2026‑03‑26 (v1.0)**: Initial release, supporting multi-speaker dialogue synthesis, SSML/segment-merge dual modes.