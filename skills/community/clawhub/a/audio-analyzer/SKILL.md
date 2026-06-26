---
name: audio-analyzer
version: 1.1.1
displayName: "Smart Audio Analyzer — 录音转写·说话人识别·场景纪要"
description: >
  All-in-one audio analysis: transcribe, identify speakers by voiceprint,
  auto-detect scene (meeting/interview/training/talk), generate structured notes.
  The ONLY skill with persistent voice profile matching across sessions.
  录音分析全流程：转写+说话人声纹识别+场景自动判断+结构化纪要。
  唯一支持跨录音声纹档案匹配的 skill。支持 AssemblyAI / Whisper / Gemini 多引擎。
metadata:
  openclaw:
    emoji: "🎙️"
    tags:
      - audio
      - transcribe
      - voice
      - speaker-identification
      - meeting-notes
      - voiceprint
      - assemblyai
      - whisper
      - scene-detection
      - structured-notes
    triggers:
      file_types: [".m4a", ".mp3", ".wav", ".ogg", ".flac"]
      keywords: ["分析录音", "转写", "会议纪要", "录音分析", "听一下这个",
                 "transcribe", "meeting notes", "who said what", "analyze audio"]
    requires:
      npm: ["assemblyai", "dotenv", "openai"]
      env_any_of: ["ASSEMBLYAI_API_KEY", "GEMINI_API_KEY", "OPENAI_API_KEY"]
      optional_python: ["numpy", "librosa", "onnxruntime"]
      optional_system:
        - whisper (pip install openai-whisper, optional local ASR fallback)
        - ffmpeg (required for voiceprint extraction)
      optional_model:
        - ONNX speaker embedding model (WeSpeaker cnceleb_resnet34_LM.onnx)
        - Set WESPEAKER_MODEL env var to model path
        - Download: https://github.com/wenet-e2e/wespeaker/releases
      optional_env: ["WESPEAKER_MODEL", "ASR_ENGINE"]
    permissions:
      - shell_exec: whisper (optional local ASR), ffmpeg (audio segment extraction for voiceprint)
      - network: AssemblyAI API, OpenRouter API, Google Gemini API (for transcription and summarization)
      - filesystem: read audio files, write transcripts/summaries, read/write voice-profiles.md and voice-db.json
      - privacy: voiceprint.py extracts and stores speaker embeddings locally in references/voice-db.json for cross-session speaker identification. Voice embeddings are stored locally, never sent externally. Audio files are uploaded to cloud ASR services for transcription (use Whisper for offline). Users must explicitly confirm speaker identity before profiles are updated.
    install:
      - id: npm-install
        kind: shell
        command: "cd scripts && npm install"
        label: "安装 Node.js 依赖"
---

# Smart Audio Analyzer

> The only audio skill with persistent voice profiles. Beyond transcription — it knows WHO is speaking, detects the scene, and generates structured notes.

> 唯一带声纹档案的录音分析 skill。转写只是第一步——它还能认出谁在说话，自动判断场景，按模板出纪要。

## What Makes This Different

| Feature | This Skill | Others |
|---------|-----------|--------|
| Transcription | ✅ AssemblyAI (default) + Whisper + Gemini | ✅ Usually one engine |
| Speaker ID by voiceprint | ✅ Persistent profiles across sessions | ❌ None |
| Scene auto-detection | ✅ 5 built-in scenes + extensible | ❌ One-size-fits-all |
| Structured output | ✅ Scene-specific templates | ⚠️ Generic summary |
| Multi-language | ✅ Chinese + English | Varies |

## Quick Start

```bash
# 1. Install
cd skills/audio-analyzer/scripts && npm install

# 2. Configure (pick ONE — AssemblyAI recommended)
cp .env.example .env
# Edit .env: set ASSEMBLYAI_API_KEY

# 3. Run
node analyze.js /path/to/recording.m4a
```

**Zero-config alternative**: If no API key is set, it will attempt local Whisper or Gemini fallback.

## 安装

```bash
# 1. 放到 workspace/skills/ 下
cp -r audio-analyzer /path/to/.openclaw/workspace/skills/

# 2. 安装依赖
cd skills/audio-analyzer/scripts && npm install

# 3. 配置 ASR 引擎（选一个即可，推荐 AssemblyAI）
cp .env.example .env
# 编辑 .env，填入 ASSEMBLYAI_API_KEY

# 4. 多 agent 环境：每个 agent 的 workspace 都需要一份
```

## Bootstrap 片段

**将以下内容添加到你的 agent bootstrap.md：**

```markdown
## 音频文件处理
当收到音频文件（.m4a/.mp3/.wav/.ogg/.flac）时，**必须**按以下流程处理：
1. 运行 `cd <workspace>/skills/audio-analyzer/scripts && node analyze.js <音频文件绝对路径>` 进行转写+说话人分离
2. 读取转写结果，根据内容自动判断场景（或按用户指定）
3. 读取 skills/audio-analyzer/references/scenes/<场景>.md 加载模板
4. 读取 skills/audio-analyzer/references/voice-profiles.md 对照音色档案
5. 按模板生成结构化纪要
6. 与用户确认说话人身份，更新音色档案

**不要**尝试用 summarize、pdf、image 等工具处理音频文件。
```

## Core Pipeline

```
Audio File → Transcribe + Speaker Separation → Voice Profile Matching
→ Scene Detection → Load Template → Generate Notes → Update Profiles
```

### Step 1: Transcribe

```bash
cd scripts && node analyze.js <文件路径>
```

**ASR Engine Priority:**
1. **AssemblyAI** (default, best quality) — needs `ASSEMBLYAI_API_KEY`
2. **Gemini** — needs `GEMINI_API_KEY` or OpenRouter key
3. **Whisper** (local) — needs `whisper` installed locally

Output:
- `<filename>_transcript.txt` — timestamped dialogue with speaker labels
- `<filename>_raw.json` — raw JSON with speaker metadata

### Step 2: Speaker Identification

Cross-references `references/voice-profiles.md`:

1. Read all known voice profiles (speech patterns, content patterns)
2. Analyze each speaker against profiles
3. Match rules:
   - High confidence → auto-label with name
   - Partial match → label as "possibly XXX" with evidence
   - No match → label as "Unknown Speaker"
4. Ask user to confirm
5. Update profiles after confirmation

### Step 3: Scene Detection

Auto-detects based on transcript content:

| Scene | Typical Keywords | Template |
|-------|-----------------|----------|
| 🚣 Rowing Training | stroke rate, pace, catch, drive | `scenes/rowing.md` |
| 💼 Work Meeting | project, deadline, requirements, bug | `scenes/meeting.md` |
| 🎤 Interview | user pain points, use case, feedback | `scenes/interview.md` |
| 🎓 Talk/Lecture | welcome, today's topic, Q&A | `scenes/talk.md` |
| 📝 General | (fallback) | `scenes/general.md` |

Override manually: `node analyze.js file.m4a meeting`

### Step 4-5: Generate Structured Notes

Loads scene-specific template → generates structured output with key points, action items, and insights.

### Step 6: Update Voice Profiles

After user confirms speaker identities, updates `references/voice-profiles.md`:
- New person → add entry (role, speech patterns, content patterns)
- Known person → refine description
- Shared across all scenes and future recordings

## Extending Scenes

Add a new `.md` file in `references/scenes/`:

```
references/scenes/
├── rowing.md      # 🚣 Rowing Training
├── meeting.md     # 💼 Work Meeting
├── interview.md   # 🎤 Interview
├── talk.md        # 🎓 Talk/Lecture
└── general.md     # 📝 General (fallback)
```

## Requirements

- Node.js 18+
- At least ONE of: AssemblyAI key, Gemini key, or local Whisper
- `cd scripts && npm install`

## Error Handling

| Situation | Response |
|-----------|----------|
| API quota exceeded | "Transcription service unavailable, check API quota" |
| File > 100MB | Warn user: estimated 5-10 min processing |
| Empty transcript | "No speech detected in audio" |
| Network error | "Connection error, please retry" |
| No ASR engine available | List setup instructions for each engine |

## Advanced: Voiceprint Extraction (Optional)

The skill includes an optional `voiceprint.py` tool for **embedding-based speaker identification** using ONNX neural models. This is separate from the text-based voice profile matching in the core pipeline.

### What it does
- Extracts speaker audio segments using ffmpeg
- Computes 256-dim speaker embeddings via WeSpeaker ONNX model
- Stores embeddings locally in `references/voice-db.json`
- Matches new speakers against stored embeddings (cosine similarity)

### Setup (optional — core skill works without this)

```bash
# 1. Install Python dependencies
pip install numpy librosa onnxruntime

# 2. Install ffmpeg
apt install ffmpeg  # or: brew install ffmpeg

# 3. Download WeSpeaker model
mkdir -p ~/.openclaw/models/wespeaker
# Download cnceleb_resnet34_LM.onnx from:
# https://github.com/wenet-e2e/wespeaker/releases
# Set: export WESPEAKER_MODEL=~/.openclaw/models/wespeaker/cnceleb_resnet34_LM.onnx
```

### Usage

```bash
# Extract voiceprints from a transcribed recording
python3 voiceprint.py extract recording.m4a recording_raw.json

# Enroll a known speaker
python3 voiceprint.py enroll "JoJo" jojo_sample.m4a

# Identify speaker in new audio
python3 voiceprint.py identify unknown.m4a
```

### Privacy Notice
- All voice embeddings are stored **locally** in `references/voice-db.json`
- Voice embeddings are never sent externally
- Audio files ARE uploaded to cloud ASR (AssemblyAI/Gemini) for transcription. For fully offline operation, use local Whisper
- Speaker identity updates require **explicit user confirmation**
- To delete all voiceprint data: `rm references/voice-db.json`

## Voice Profiles (Text-Based)

See `references/voice-profiles.md`. Shared across all scenes — same person is recognized regardless of context. This is the lightweight alternative that works without the ONNX model.
