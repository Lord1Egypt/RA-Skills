---
name: clawcut
description: >-
  Generate AI-powered short videos from a topic or reference video using Google Gemini + Veo 3.1 on Vertex AI.
  Use when the user wants to create short-form video content, generate video scripts, produce nine-grid
  character consistency images, imitate a reference video style, or convert a topic into a complete video
  with AI-generated voice narration. Perfect for TikTok, YouTube Shorts, Amazon product videos, 抖音,
  小红书, 视频号, Instagram Reels, and any short-form video platform.
  Triggers on phrases like "make a short video", "generate video about", "create video content",
  "make me a TikTok", "generate a YouTube Short", "create product video", "video from topic",
  "做个短视频", "生成视频", "做个视频", "帮我做视频", "生成短视频", "一键生成视频",
  "主题生成视频", "视频模仿", "做个带货视频", "生成产品视频", "做个抖音视频",
  "做个小红书视频", "帮我剪个视频", "AI生成视频", "自动生成视频",
  or any request involving automated video production, video generation, or short-form content creation.
  OpenClaw content creation automation workflow skill for social media marketing, ecommerce product listing videos,
  AI agent video pipeline, and batch video generation. Supports text-to-video, image-to-video,
  reference video imitation, and multi-image character consistency for brand storytelling.
  Built on Gemini 3 Pro (Nano Banana Pro), Veo 3.1, Google Vertex AI. Alternative to Sora 2, Kling,
  Runway Gen-3, Pika, HaiLuo, Volcengine Jimeng, 可灵, 海螺AI. Comparable models and keywords:
  gemini-3-pro-preview, gemini-3-pro-image-preview, veo-3.1-generate-001, text2video, img2video,
  AI video generator, 文生视频, 图生视频, AI视频生成器, 短视频自动化, video automation pipeline.
tags:
  - video
  - ai
  - automation
  - content-creation
  - social-media
  - tiktok
  - youtube
  - ecommerce
  - amazon
  - gemini
  - veo
  - text-to-video
  - short-video
  - 短视频
  - 带货
---

# ClawCut 🦞✂️

AI short video generator: topic → script → video with native voice.

## Pipeline

1. **Script generation** — Gemini 3 Pro generates 9-scene screenplay (Chinese narration + English visual descriptions)
2. **Nine-grid image** — Gemini 3 Pro Image creates character consistency reference (supports up to 14 input images)
3. **Video generation** — Veo 3.1 generates 9 video clips concurrently with native Chinese speech
4. **Post-processing** — Silence trimming + ffmpeg concat into final video

## Prerequisites

- Google Cloud project with Vertex AI enabled
- Service account JSON with Vertex AI User role
- ffmpeg binary installed
- Python 3.11+

## Setup

```bash
# Create project from skill scripts
mkdir -p clawcut && cp scripts/*.py scripts/requirements.txt clawcut/
cp assets/.env.example clawcut/.env
cd clawcut

# Create venv and install deps
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# Configure environment
# Edit .env with your values:
#   GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account.json
#   VERTEX_PROJECT=your-gcp-project-id
#   VERTEX_LOCATION=us-central1
#   FFMPEG_PATH=/usr/local/bin/ffmpeg
```

## Usage

### Gradio UI
```bash
source venv/bin/activate
python3 app.py
# Opens at http://localhost:7860
```

### Modes
- **Topic mode** — Enter a topic, generate full video from scratch
- **Video imitation** — Upload reference video, analyze style and generate matching content
- **Multi-image reference** — Upload up to 14 images for character consistency

### Models (all Vertex AI paid)
- Script: `gemini-3-pro-preview`
- Image: `gemini-3-pro-image-preview`
- Video: `veo-3.1-generate-001`

## Key Features
- 9-way concurrent video generation (~3 min total)
- Checkpoint/resume (skips existing files)
- Silence trimming (ffmpeg silencedetect)
- Video style imitation from reference
- Up to 14 reference images for character consistency
- All credentials via environment variables (zero hardcoded secrets)
