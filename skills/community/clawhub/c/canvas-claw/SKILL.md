---
name: canvas-claw
description: Generate images and videos through AI-video-agent. Supports image create, image remix, video create, and video animate.
metadata:
  {
    "openclaw":
      {
        "emoji": "🎬",
        "requires":
          {
            "bins": ["python3"],
            "env":
              [
                "AI_VIDEO_AGENT_BASE_URL",
                "AI_VIDEO_AGENT_TOKEN",
                "AI_VIDEO_AGENT_SITE_ID",
              ],
          },
        "primaryEnv": "AI_VIDEO_AGENT_TOKEN",
      },
  }
---

# Canvas Claw

Canvas Claw is an OpenClaw skill package that sends generation tasks to AI-video-agent.

## Core Capabilities

- 图片生成：`python3 {baseDir}/scripts/generate_image.py --prompt "cinematic portrait"`
- 参考图生成：`python3 {baseDir}/scripts/generate_image.py --prompt "same character, winter coat" --reference-image "/tmp/char.png"`
- 文本生成视频：`python3 {baseDir}/scripts/generate_video.py --prompt "a rainy city street at night"`
- 图片生成视频：`python3 {baseDir}/scripts/generate_video.py --prompt "the character turns and smiles" --first-frame "/tmp/frame.png"`

## Model Discovery

- 图片模型：`python3 {baseDir}/scripts/image_models.py`
- 视频模型：`python3 {baseDir}/scripts/video_models.py`

## Login Helper

- `python3 {baseDir}/scripts/login.py --base-url "http://localhost:8000" --site-id 10000 --username "demo" --password "secret"`
