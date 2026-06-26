---
name: bilibili-ai-subtitle
description: "Download Bilibili AI-generated subtitles (auto-subtitles) for videos. Use when you need to quickly get subtitles from Bilibili videos that have AI-generated captions. Supports 9 languages: Chinese, English, Japanese, Spanish, Arabic, Portuguese, Korean, German, French. Language priority can be customized."
---

# Bilibili AI Subtitle Downloader v2.0

Download AI-generated subtitles from Bilibili videos quickly.

## What This Skill Does

This skill downloads **AI-generated subtitles** (自动生成的字幕) from Bilibili videos. These are subtitles automatically created by Bilibili's AI system, not manually uploaded by creators.

**Key improvements from v1.x:**
- ✅ Customizable language priority (e.g., prefer English over Chinese)
- ✅ Better filename format: `Title_Author_Date_Duration_BVid.txt`
- ✅ Three-part document structure (Info, Summary, Full Text)
- ✅ Improved UTF-8 filename handling
- ✅ Better WSL Chromium/Windows Edge Cookie support

## Supported AI Languages

Bilibili uses `ai-` prefix for AI-generated subtitles:

| Code | Language | 语言 |
|------|----------|------|
| `ai-zh` | Chinese | 中文 |
| `ai-en` | English | 英文 |
| `ai-ja` | Japanese | 日文 |
| `ai-es` | Spanish | 西班牙文 |
| `ai-ar` | Arabic | 阿拉伯文 |
| `ai-pt` | Portuguese | 葡萄牙文 |
| `ai-ko` | Korean | 韩文 |
| `ai-de` | German | 德文 |
| `ai-fr` | French | 法文 |

## Usage

### Basic Usage
```bash
./scripts/bilibili_ai_subtitle.sh "https://www.bilibili.com/video/BVxxxxx/"
```

### Specify Language Priority
```bash
# Prefer English, fallback to Chinese
./scripts/bilibili_ai_subtitle.sh -l en,zh "BVxxxxx"

# Prefer Japanese
./scripts/bilibili_ai_subtitle.sh --lang ja "BVxxxxx"

# Multiple languages in order of preference
./scripts/bilibili_ai_subtitle.sh -l en,zh,ja,es "BVxxxxx"
```

## Output

**File name format:** `VideoTitle_Author_Date_Duration_BVid.txt`

**File structure:**
```
第一部分：视频信息
├── 视频标题
├── B站链接
├── 作者
├── 发布时间
├── 视频时长
├── 原视频语言
└── 转录来源

第二部分：视频摘要
└── 自动生成的内容摘要

第三部分：完整原文
└── 完整字幕文本
```

## Setup

### Browser Cookie (Recommended)

For accessing member-only videos, log in to Bilibili in:
- **WSL Chromium** (preferred): `chromium-browser &`
- **Windows Edge**: Log in normally

The script will automatically detect and use available cookies.

## Requirements

- `yt-dlp` installed
- Optional: Browser with Bilibili login (for member-only videos)

## Notes

- AI subtitles are generated automatically by Bilibili's system
- Accuracy varies (typically 85-95% for clear speech)
- Not all videos have AI subtitles available
- Some videos may require membership to access AI subtitles

## Comparison with bilibili-transcript

| Feature | bilibili-ai-subtitle | bilibili-transcript |
|---------|---------------------|---------------------|
| **Purpose** | Download AI subtitles only | Full transcription workflow |
| **Speed** | ⚡ Fast (instant download) | Varies (subtitles → Whisper) |
| **Subtitle sources** | AI only | CC → AI → Whisper |
| **Use case** | Quick subtitle grab | Complete transcription |
| **Dependencies** | yt-dlp only | yt-dlp + optional Whisper |

**Recommendation:** Use `bilibili-ai-subtitle` for quick AI subtitle download, use `bilibili-transcript` when you need complete transcription (including voice transcription for videos without subtitles).
