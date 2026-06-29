# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Python CLI client for the ChatArt Pro API — generates AI images, videos, and animations via cloud APIs. All async tasks auto-poll to completion before returning.

## Commands

```bash
# Authentication
python auth.py login        # OAuth device flow — opens browser, saves to ~/.ChatArt/credentials.json
python auth.py status       # Check current login state
python auth.py logout       # Remove credentials

# AI Image (text-to-image and image editing)
python ai_image.py run --type text2image --model "Nano Banana" --prompt "..." --aspect-ratio "16:9"
python ai_image.py run --type image_edit --model "Nano Banana" --prompt "..." --input-images photo.jpg --aspect-ratio "16:9"
python ai_image.py list-models --type text2image
python ai_image.py estimate-cost --type text2image --model "Nano Banana" --resolution "2K" --count 2

# Video Generation (i2v, t2v, extend, anim)
python video_gen.py run --type i2v --model "Seedance 2.0" --first-frame photo.png --prompt "..."
python video_gen.py run --type t2v --model "Seedance 2.0" --prompt "..." --aspect-ratio "16:9" --duration 5
python video_gen.py run --type extend --model "LitAI 5" --input-video video.mp4 --prompt "..."
python video_gen.py run --type anim --model "LitAI 5" --input-image photo.png --prompt "..." --style "anime"
python video_gen.py list-models --type t2v
python video_gen.py estimate-cost --model "Seedance 2.0" --resolution 720 --duration 5 --count 1

# Character Replace in Videos
python video_mimic.py run --type Full_Scene --model "Kling V3.0" --input-image char.jpg --input-video video.mp4
python video_mimic.py run --type Body_Only --model "Wan 2.2" --input-image char.jpg --input-video video.mp4

# Account Management
python user.py credit       # Query credit balance
python user.py logs --type video --page 1 --size 20  # Query usage history
```

## Architecture

```
scripts/
├── auth.py            # OAuth 2.0 device flow login + credential file management
├── ai_image.py        # Text-to-image and image editing (text2image, image_edit)
├── video_gen.py       # Video generation (i2v, t2v, extend, anim, a2ls)
├── video_mimic.py     # Character replacement in videos (Full_Scene, Body_Only)
├── user.py            # Credit balance and usage history queries
└── shared/
    ├── config.py      # Credential loading (env vars → ~/.ChatArt/credentials.json)
    ├── client.py      # ChatArtClient: authenticated HTTP client, task polling, URL shortening
    ├── upload.py       # Local file → Alibaba Cloud OSS upload
    └── media_util.py  # MediaInfo wrapper for duration/resolution extraction
```

## Authentication

Credentials are loaded in this priority order:
1. Environment variables `CHATART_UID` + `CHATART_API_KEY`
2. `~/.ChatArt/credentials.json` (created by `auth.py login`)
3. Exit with error prompting login

Credentials contain: `uid`, `api_key`, `email`, `name`, `team_id`, `charge_type`, `remain_credit`.

## Agent Workflow Rules

Each module enforces this pattern — never deviate:
- **`run`** — submits task and polls until done (default, always use first)
- **`submit`** — submit only, print taskId (for parallel batch jobs)
- **`query`** — poll an existing taskId (only if `run` timed out)
- Never return a pending taskId to the user without polling it to completion

## API Endpoints

- **Base URL**: `https://chatartpro-api.ifonelab.net`
- **OAuth**: `https://litvideo-api.litmedia.ai`
- Image endpoints: `/web/art/create`, `/web/art/get-draw-task`
- Video endpoints: `/web/video/generate-video`, `/web/video/get-video-task`
- Credit: `/web/member/user-diamond`
- History: `/web/art/history`, `/web/video/history`

## Dependencies

```
requests>=2.28.0
python-dotenv>=1.0.0
alibabacloud-oss-v2==1.2.4
pymediainfo==7.0.1
```
