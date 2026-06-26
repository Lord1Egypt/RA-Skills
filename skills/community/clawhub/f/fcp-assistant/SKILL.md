---
name: fcp-assistant
description: "Auto video production, TTS voiceover, media management, batch export | AI 自动成片、TTS 配音、素材管理、批量导出. Triggers: FCP, Final Cut, make video, auto video, voiceover, import media, export"
author: Steve & Steven
metadata:
  openclaw:
    emoji: 🎬
    requires:
      bins: [osascript, ffmpeg, ffprobe, curl, jq]
---

# Final Cut Pro Assistant

A fully automated video production pipeline — from script to final cut. Also your everyday FCP editing assistant.

---

## 🔥 Core Feature: AI Auto Video Production

**One pipeline. Script in, video out.**

### Full Workflow

```
Script 📝 → Fetch Media 🔍 → TTS Voiceover 🎤 → Auto Assemble 🎞️ → Publish 🚀
```

### Step 1: Fetch Video Assets

Auto-search and download free stock footage from Pexels by keywords.

```bash
bash scripts/media-collector.sh \
    --keywords "nature ocean sunset" \
    --count 5 --output ./my-project
```

- Multi-keyword search (searches each word separately, then merges)
- Orientation (landscape/portrait/square), quality (SD/HD/4K), duration filtering
- Saves metadata and license info automatically
- Set `PEXELS_API_KEY` for expanded search

### Step 2: Add Background Music

Drop your BGM files (mp3/wav/m4a) into the project's `music/` folder. The assembler auto-detects them.

```
my-project/
├── videos/     ← Stock footage (auto-filled by Step 1)
├── music/      ← Your BGM goes here
└── meta/       ← Metadata (auto-generated)
```

### Step 3: TTS Voiceover

Generate per-paragraph voiceover using Qwen TTS.

```bash
bash scripts/tts-voiceover.sh \
    --script "First paragraph
Second paragraph
Third paragraph" \
    --output ./my-project/voiceover
```

- Per-paragraph generation with automatic silence trimming
- Customizable voice via `--instruct` (e.g., "warm female voice, moderate pace")
- Also reads from file: `--script-file ./script.txt`
- Requires Qwen TTS WebUI running at `localhost:7860`

### Step 4: Auto Assemble

Combines footage, voiceover, subtitles, and BGM into a finished video.

```bash
bash scripts/auto-video-maker.sh \
    --project ./my-project \
    --script-file ./script.txt \
    --voiceover ./my-project/voiceover \
    --style vlog \
    --output final.mp4
```

**Smart Features:**
- 📝 Script split by paragraph, each mapped to a video clip
- 🎤 Clip duration auto-syncs to voiceover timing when available
- 📝 Burn-in subtitles with PingFang SC font (position/size adjustable)
- 🎵 Smart audio mixing — voiceover + BGM (BGM auto-ducked to 15%)
- 🎬 Fade transitions between clips
- 📐 Uniform resolution (default 1920x1080, supports portrait 1080x1920)

**Style Presets:**

| Style | Pacing | Font Size | Transition | Best For |
|-------|--------|-----------|------------|----------|
| `default` | Medium | 42 | 0.5s | General |
| `vlog` | Upbeat | 38 | 0.3s | Daily vlogs |
| `cinematic` | Slow | 48 | 1.0s | Scenic/story |
| `fast` | Rapid | 36 | 0.2s | Shorts/TikTok |

**More Options:**
```bash
--resolution 1080x1920    # Portrait mode
--no-subtitle             # No subtitles
--subtitle-pos center     # Center subtitles (default: bottom)
--font-size 50            # Custom font size
--music ./specific.mp3    # Specify BGM file
--transition none         # No transitions
```

---

## 📂 FCP Project Management

Automate everyday Final Cut Pro tasks.

```bash
osascript scripts/check-fcp.scpt          # Check FCP status
osascript scripts/list-projects.scpt       # List all projects
osascript scripts/open-project.scpt "Name" # Open a project
osascript scripts/import-temp-media.scpt   # Import temp media
osascript scripts/project-time-tracking.scpt  # Time tracking
```

---

## ✂️ Editing Assistance

```bash
bash scripts/scene-detect.sh video.mp4          # Scene detection
bash scripts/auto-rough-cut.sh video.mp4         # Auto rough cut (silence removal)
bash scripts/smart-tagger.sh ./media/            # AI smart tagging
bash scripts/auto-chapter-marker.sh video.mp4    # Auto chapter markers
```

---

## 🔊 Audio Processing

```bash
bash scripts/audio-normalizer.sh video.mp4       # Normalize to -23 LUFS
bash scripts/auto-voiceover.sh "text" out.wav    # Single-file voiceover
```

---

## 🌍 Subtitles

```bash
bash scripts/multi-lang-subtitles.sh video.mp4 en   # Multi-language (en/ja/ko/fr/de/es)
```

---

## 🖼️ Other Tools

```bash
bash scripts/auto-thumbnail.sh video.mp4 ./thumbs   # Keyframe thumbnails + contact sheet
osascript scripts/create-script.scpt "Title" "Content"  # Create script in Notes
osascript scripts/list-scripts.scpt                  # List scripts
```

---

## Requirements

- **Required**: macOS, ffmpeg (with drawtext/libass), osascript
- **TTS**: Qwen TTS WebUI (`localhost:7860`)
- **Media Search**: Internet (Pexels API, free)
- **Recommended**: `brew install homebrew-ffmpeg/ffmpeg/ffmpeg` (includes drawtext + libass)

---

*From script to screen — let AI make your videos! 🎬*

---
---

# 中文版

# Final Cut Pro 助手

从文案到成片的全自动视频生产线，同时也是你的 FCP 剪辑助手。

---

## 🔥 核心能力：AI 自动视频生产

**一条命令，从文案到成品视频。**

### 完整工作流

```
文案 📝 → 搜素材 🔍 → TTS 配音 🎤 → 自动成片 🎞️ → 发布 🚀
```

### Step 1: 搜集视频素材

从 Pexels 免费素材库自动搜索下载，按关键词匹配。

```bash
bash scripts/media-collector.sh \
    --keywords "nature ocean sunset" \
    --count 5 --output ./my-project
```

- 多关键词自动逐词搜索
- 支持方向（横屏/竖屏）、质量（SD/HD/4K）、时长范围筛选
- 自动保存素材元数据和版权信息
- 设置 `PEXELS_API_KEY` 解锁更多搜索能力

### Step 2: 准备背景音乐

把你找的 BGM 放到项目的 `music/` 目录即可，成片时自动检测。

```
my-project/
├── videos/     ← 素材（Step 1 自动填充）
├── music/      ← 你的 BGM 放这里（mp3/wav/m4a）
└── meta/       ← 元数据（自动生成）
```

### Step 3: TTS 配音

用 Qwen TTS 为每段文案生成配音。

```bash
bash scripts/tts-voiceover.sh \
    --script "第一段文案
第二段文案
第三段文案" \
    --output ./my-project/voiceover
```

- 逐段生成，自动修剪首尾静音
- 声音特征可自定义（`--instruct`）
- 也支持从文件读取：`--script-file ./script.txt`
- 需要 Qwen TTS WebUI 运行在 `localhost:7860`

### Step 4: 自动成片

把素材、配音、字幕、BGM 全部组装成完整视频。

```bash
bash scripts/auto-video-maker.sh \
    --project ./my-project \
    --script-file ./script.txt \
    --voiceover ./my-project/voiceover \
    --style vlog \
    --output final.mp4
```

**智能特性：**
- 📝 文案按段落拆分，每段对应一个视频片段
- 🎤 有配音时，片段时长自动匹配配音节奏
- 📝 PingFang SC 简体中文字幕烧入（位置/大小可调）
- 🎵 配音 + BGM 智能混合（BGM 自动降低到 15% 音量）
- 🎬 fade 转场效果
- 📐 统一分辨率（默认 1920x1080，支持竖屏 1080x1920）

**风格预设：**

| 风格 | 节奏 | 字号 | 转场 | 适合 |
|------|------|------|------|------|
| `default` | 中等 | 42 | 0.5s | 通用 |
| `vlog` | 轻快 | 38 | 0.3s | 日常 Vlog |
| `cinematic` | 缓慢 | 48 | 1.0s | 电影感 |
| `fast` | 快速 | 36 | 0.2s | 短视频/抖音 |

---

## 📂 FCP 项目管理

```bash
osascript scripts/check-fcp.scpt          # 检查 FCP 状态
osascript scripts/list-projects.scpt       # 列出所有项目
osascript scripts/open-project.scpt "名称"  # 打开项目
osascript scripts/import-temp-media.scpt   # 导入临时素材
osascript scripts/project-time-tracking.scpt  # 时间追踪
```

## ✂️ 剪辑辅助

```bash
bash scripts/scene-detect.sh video.mp4     # 场景分析
bash scripts/auto-rough-cut.sh video.mp4   # 自动粗剪
bash scripts/smart-tagger.sh ./media/      # 智能标签
bash scripts/auto-chapter-marker.sh video.mp4  # 自动章节标记
```

## 🔊 音频处理

```bash
bash scripts/audio-normalizer.sh video.mp4 # 音频标准化 (-23 LUFS)
bash scripts/auto-voiceover.sh "文本" out.wav  # 单文件配音
```

## 🌍 字幕

```bash
bash scripts/multi-lang-subtitles.sh video.mp4 en  # 多语言字幕
```

## 🖼️ 其他工具

```bash
bash scripts/auto-thumbnail.sh video.mp4 ./thumbs  # 自动缩略图
osascript scripts/create-script.scpt "标题" "内容"   # 创建文案
osascript scripts/list-scripts.scpt                 # 列出文案
```

---

## 依赖

- **必需**: macOS, ffmpeg (with drawtext/libass), osascript
- **TTS 配音**: Qwen TTS WebUI (`localhost:7860`)
- **素材搜索**: 网络连接（Pexels API，免费）
- **推荐**: `brew install homebrew-ffmpeg/ffmpeg/ffmpeg`

---

*从文案到成片，让 AI 帮你做视频！🎬*

*Made by Steve & Steven 🤝*
