---
name: douyin-transcribe
description: Douyin video transcription suite. Extract audio from Douyin/TikTok China videos, transcribe with Whisper, and analyze content. Supports video links, local files, and image notes. Trigger when user sends a Douyin link and asks for transcription, summary, or analysis.
---

# Douyin Transcribe - Video Transcription Suite

A complete solution for transcribing Douyin (抖音/TikTok China) videos. Extracts audio, transcribes speech to text, and generates structured summaries.

## Version History

| Version | Changes |
|---------|---------|
| 2.0.0 | Modular architecture, improved workflow, browser DOM extraction |
| 1.0.0 | Initial release, basic transcription |

## Architecture

\\\
User Input (Douyin Link/File)
         │
         ▼
┌─────────────────────────────────────────┐
│           Workflow Orchestrator          │
├─────────────────────────────────────────┤
│  Step 1: Fetcher    → Get video file    │
│  Step 2: Transcriber → Extract & convert│
│  Step 3: Analyzer    → Structure output │
│  Step 4: Output      → Save results     │
└─────────────────────────────────────────┘
\\\

## Core Features

- **Video Fetching**: Browser-based DOM extraction for CDN URLs
- **Audio Extraction**: ffmpeg-powered audio conversion
- **Speech-to-Text**: Whisper ASR with multiple model options
- **Content Analysis**: Auto-structured transcripts with key points
- **Multi-format Support**: Video links, local files, image notes

## Prerequisites

| Tool | Purpose | Install |
|------|---------|---------|
| curl | Download files | Built-in (Windows: \curl.exe\) |
| ffmpeg | Audio extraction/merge | \winget install Gyan.FFmpeg\ |
| Whisper | Transcription | \pip install openai-whisper\ or Docker |
| Browser | Video extraction | OpenClaw profile required |

**Docker Whisper (Recommended):**
\\\ash
docker run -d -p 9000:9000 --name whisper-asr onerahmet/openai-whisper-asr-webservice:latest
\\\

## Workflow

### Step 0: Input Classification

| Input Type | Detection | Action |
|------------|-----------|--------|
| Video link (\/video/\) | URL pattern | Full workflow |
| Image note (\/note/\) | URL pattern | Snapshot only |
| Local video file | File path | Start from Step 2 |
| Text input | Plain text | Start from Step 3 |

### Step 1: Fetch Video

#### 1.1 Resolve Short URL

\\\ash
# Windows PowerShell
curl.exe -sL -o NUL -w "%{url_effective}" "https://v.douyin.com/xxx/"

# macOS/Linux
curl -sL -o /dev/null -w '%{url_effective}' "https://v.douyin.com/xxx/"
\\\

Output: \https://www.douyin.com/video/7616020798351871284\

#### 1.2 Open Video Page

\\\
browser(action='open', profile='openclaw', url='https://www.douyin.com/video/{VIDEO_ID}')
\\\

Wait 10-15 seconds for page to load completely.

#### 1.3 Extract Video URL (Browser DOM Method)

\\\javascript
browser(action='act', targetId='PAGE_ID', request={
  "kind": "evaluate", 
  "fn": "(() => {
    const entries = performance.getEntriesByType('resource');
    const videoEntries = entries.filter(e => {
      const name = e.name.toLowerCase();
      return name.includes('douyinvod') && 
             (name.includes('.mp4') || name.includes('video'));
    });
    if (videoEntries.length > 0) {
      const video = videoEntries[videoEntries.length - 1];
      return {
        url: video.name,
        type: video.name.includes('.mp4') ? 'mp4' : 'dash'
      };
    }
    return null;
  })()"
})
\\\

**Important Notes:**
- \ct\ action requires nested \equest\ object with \kind\ and \n\
- Wrong: \rowser(action='act', fn='...')\
- Correct: \rowser(action='act', request={"kind": "evaluate", "fn": "..."})\

#### 1.4 Download Video

\\\ash
curl.exe -L -H "Referer: https://www.douyin.com/" -o video.mp4 "<CDN_URL>"
\\\

**Referer header is required, otherwise 403.**

### Step 2: Transcribe Audio

#### 2.1 Extract Audio

\\\ash
# For MP4 videos
ffmpeg -i video.mp4 -ar 16000 -ac 1 -c:a pcm_s16le audio.wav -y

# For DASH videos (need merge)
ffmpeg -i video.mp4 -i audio.mp4 -c copy merged.mp4 -y
ffmpeg -i merged.mp4 -ar 16000 -ac 1 -c:a pcm_s16le audio.wav -y
\\\

Parameters:
- \-ar 16000\: 16kHz sample rate (Whisper requirement)
- \-ac 1\: Mono channel
- \-c:a pcm_s16le\: 16-bit PCM

#### 2.2 Transcribe with Docker Whisper

\\\ash
curl.exe -X POST "http://localhost:PORT/asr" -F "audio_file=@audio.wav"
\\\

#### 2.3 Alternative: Local Whisper

\\\ash
python -m whisper audio.wav --model small --language zh
\\\

**Model Selection:**

| Model | Size | 5-min Video (CPU) | Accuracy | Use Case |
|-------|------|-------------------|----------|----------|
| tiny | 75MB | ~30s | Fair | Quick preview |
| base | 142MB | ~1min | Good | Daily use |
| small | 466MB | ~3min | Better | **Recommended** |
| medium | 1.5GB | ~8min | Best | High accuracy |

### Step 3: Analyze Content

Agent processes transcript and generates:

1. **Fix transcription errors**
   - Correct homophones
   - Fix speaker names
   - Remove filler words

2. **Structure content**
   - Add paragraph breaks
   - Create sections

3. **Extract key points**
   - Main ideas
   - Important quotes

4. **Generate tags**
   - 3-5 topic tags

### Step 4: Save Output

#### Transcript Format

\\\markdown
# {Title}

**作者**: {Author}
**来源**: 抖音
**日期**: {Date}
**转录时间**: {Transcription Date}

---

## 摘要

{Summary}

---

## 正文

{Transcript content with paragraphs}

---

## 要点

- {Key point 1}
- {Key point 2}
- {Key point 3}

---

## 标签

#{tag1} #{tag2} #{tag3}
\\\

#### File Naming Convention

\\\
{VIDEO_ID}-抖音转录.md
\\\

## Troubleshooting

| Stage | Issue | Solution |
|-------|-------|----------|
| Step 1 | Short URL fails | Check link completeness, remove share text |
| Step 1 | JS returns null | Wait 15-20s and retry, increase timeout |
| Step 1 | Download 403 | URL expired, re-fetch from browser |
| Step 1 | DASH no audio | Merge with \fmpeg -i video -i audio -c copy\ |
| Step 2 | ffmpeg not installed | \winget install Gyan.FFmpeg\ |
| Step 2 | Whisper service down | \docker start whisper-asr\ |
| Step 2 | Transcription slow | 10-min video takes 15-20 min on CPU |
| Step 2 | Poor quality | Use larger model (medium) |

## Image Note Handling

Image notes (\/note/\) don't need transcription:

\\\
1. browser(action='open', profile='openclaw', url='IMAGE_NOTE_URL')
2. browser(action='snapshot')
3. Extract content from snapshot
4. Save to output directory
\\\

## Edge Cases

- **Article links** (\/article/\): Use browser snapshot, no transcription
- **Douyin AI summary**: Extract from page as supplement
- **Other platforms**: Use yt-dlp for YouTube/Bilibili
- **Live streams**: Not supported

## Related Modules

This skill can be extended with standalone modules:

| Module | Purpose |
|--------|---------|
| douyin-fetcher | Video fetching only |
| douyin-transcriber | Audio transcription only |
| douyin-analyzer | Content analysis only |
| douyin-orchestrator | Workflow coordination |

## License

MIT-0 License - Free to use, modify, and redistribute.