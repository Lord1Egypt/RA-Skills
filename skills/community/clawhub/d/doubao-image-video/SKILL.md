---
name: doubao-image-video
description: 豆包图片与视频生成原生技能。适用于用户提到豆包、文生图、图生图、文生视频、图生视频、查询视频生成任务、等待任务完成或下载最终视频时，直接调用火山引擎 Ark 接口，不依赖外部 MCP 服务。
author: 小蜜
version: 0.3.1
homepage: https://github.com/156554395/doubao-image-video-mcp
metadata:
  {
    "openclaw": {
      "requires": { "bins": ["python3"] },
      "config": {
        "env": {
          "DOUBAO_API_KEY": {
            "description": "Volcengine Ark API key for Doubao image/video generation",
            "required": true
          },
          "DOUBAO_IMAGE_ENDPOINT_ID": {
            "description": "Default image endpoint id from Volcengine Ark",
            "required": false
          },
          "DOUBAO_VIDEO_ENDPOINT_ID": {
            "description": "Default video endpoint id from Volcengine Ark",
            "required": false
          },
          "DOUBAO_DEFAULT_IMAGE_MODEL": {
            "description": "Optional default image model",
            "default": "doubao-seedream-4-5"
          },
          "DOUBAO_DEFAULT_VIDEO_MODEL": {
            "description": "Optional default video model",
            "default": "doubao-seedance-1.0-lite-t2v"
          }
        }
      }
    }
  }
---

# Doubao Native Media Skill

This is a native OpenClaw skill. Do not spin up the upstream MCP server unless the user explicitly asks for MCP compatibility.

## Use this skill for

- Doubao / 豆包 text-to-image
- image-to-image or multi-reference image generation
- Doubao text-to-video or image-to-video
- querying an async Doubao video task by `task_id`
- troubleshooting Volcengine Ark endpoint/model issues

## Commands

### Generate an image

```bash
python3 {baseDir}/scripts/doubao_media.py image \
  --prompt "A cinematic cyberpunk alley in rain" \
  --size 2560x1440
```

### Generate a video

```bash
python3 {baseDir}/scripts/doubao_media.py video \
  --prompt "A panda astronaut waves on the moon" \
  --video-duration 5 \
  --fps 24 \
  --resolution 1080p
```

### Query a video task

```bash
python3 {baseDir}/scripts/doubao_media.py task --task-id your-task-id
```

### Wait for a video task and optionally download the result

```bash
python3 {baseDir}/scripts/doubao_media.py wait \
  --task-id your-task-id \
  --timeout 600 \
  --interval 5 \
  --download-to ./doubao-result.mp4
```

## Input rules

- Always prefer `--endpoint-id` when the user has a provisioned Volcengine Ark endpoint.
- Fall back to model names only when endpoint ids are unavailable.
- For video generation, this skill mirrors the upstream behavior and appends `--dur`, `--fps`, `--rs`, and `--ratio` to the prompt when they are not already present.
- If the user supplies image URLs, pass them through exactly; do not download or re-host unless asked.

## Troubleshooting

- If neither `--endpoint-id` nor a default endpoint env var exists, the script falls back to the default model env var.
- If the API returns `InvalidEndpointOrModel.NotFound`, ask the user to verify the Volcengine Ark endpoint authorization first.
- Video generation is async. If generation succeeds, capture `task_id` and query it later with the `task` subcommand, or use `wait` for automatic polling.

## References

- Read `references/api-notes.md` when you need request shapes, defaults, or caveats.
