---
name: ali-minimax-toolkit
description: MiniMax multimodal generation via API. Use when user wants voice, music, image, image-to-image, or video generation with MiniMax. Supports TTS, music, image (t2i + i2i), and video (t2v, i2v, sef, ref). Cross-platform Python scripts.
---

# MiniMax Multimodal Toolkit

Generate voice, music, image, and video content via MiniMax APIs. **Pure Python** — works on Windows, Mac, and Linux without any third-party dependencies.

## Prerequisites

- `MINIMAX_API_KEY` environment variable (starts with `sk-`)
- `MINIMAX_API_HOST` environment variable (optional, default: `https://api.minimaxi.com`)
- Python 3.6+
- For video duration detection: `ffprobe` (optional)

## Quick Start

```bash
# Load the Python module
import sys; sys.path.insert(0, "{skillDir}/scripts"); import minimax_api
```

Or use CLI directly:
```bash
python "{skillDir}/scripts/minimax_api.py" tts "Hello world" -o minimax-output/hello.mp3
python "{skillDir}/scripts/minimax_api.py" image "A cute cat" -o minimax-output/cat.png
```

## Output Convention

All generated files MUST be saved to `minimax-output/` under the agent's working directory.

## TTS (Text-to-Speech)

Endpoint: `POST /v1/t2a_v2` — returns hex audio, decoded and saved as file.

**Models:** `speech-2.8-hd` (recommended, best quality), `speech-2.8-turbo` (faster), `speech-02-hd`, `speech-02-turbo`

```python
# Basic TTS
minimax_api.generate_tts("Hello world", output="minimax-output/hello.mp3")

# Chinese with specific voice
minimax_api.generate_tts("红叶最多情，一舞寄相思", voice_id="female-shaonv", output="minimax-output/greeting.mp3")

# With emotion
minimax_api.generate_tts("I'm so happy today!", voice_id="male-qn-qingse", emotion="happy", output="minimax-output/happy.mp3")
```

**Common voice IDs:** `female-shaonv`, `male-qn-qingse`, `male-qn-jingying`, `presenter_male`, `presenter_female`
**Emotions:** `happy`, `sad`, `angry`, `fearful`, `disgusted`, `surprised`, `calm`, `fluent`, `whisper` (empty = auto)

## Music Generation

Endpoint: `POST /v1/music_generation` — lyrics required, returns audio URL. **Takes 30-300 seconds.**

```python
# Instrumental (BGM)
minimax_api.generate_music("soft piano, ambient, peaceful", instrumental=True, output="minimax-output/bgm.mp3")

# Song with lyrics
minimax_api.generate_music(
    "indie folk, melancholic",
    lyrics="[verse]\nWalking alone\n[chorus]\nFeeling free",
    output="minimax-output/song.mp3"
)
```

## Image Generation (Text-to-Image)

Endpoint: `POST /v1/image_generation` — returns image URLs (immediate).

```python
# Basic
minimax_api.generate_image("A cute cat on a windowsill, photorealistic", output="minimax-output/cat.png")

# With aspect ratio
minimax_api.generate_image("Mountain landscape, golden hour", aspect_ratio="16:9", output="minimax-output/landscape.png")

# Multiple images
minimax_api.generate_image("Abstract geometric art, vibrant", count=3, output="minimax-output/art.png")

# With prompt optimizer
minimax_api.generate_image("A man on Venice Beach, 90s documentary", prompt_optimizer=True, output="minimax-output/beach.png")
```

**Aspect ratios:** `1:1` (default), `16:9`, `4:3`, `3:2`, `2:3`, `3:4`, `9:16`, `21:9`

## Image-to-Image Generation

Endpoint: `POST /v1/image_generation` with `image_file` — generate new images from a reference.

```python
# From local file
minimax_api.image_to_image("A girl in a library", "minimax-output/face.jpg", output="minimax-output/library.png")

# From URL
minimax_api.image_to_image("Oil painting style", "https://example.com/photo.jpg", output="minimax-output/painting.png")
```

## Video Generation

Endpoint: `POST /v1/video_generation` (async) + `GET /v1/query/video_generation` — polling required.

```python
# Text-to-video
minimax_api.generate_video(
    "A golden retriever puppy runs toward camera, tracking shot, golden hour",
    output="minimax-output/puppy.mp4"
)

# Image-to-video (prompt focuses on MOTION only)
minimax_api.generate_video(
    "Petals sway in breeze, soft light shifts",
    mode="i2v", first_frame="minimax-output/flower.png",
    output="minimax-output/flower_video.mp4"
)

# Subject reference (face consistency)
minimax_api.generate_video(
    "A woman walks through a garden, tracking shot",
    mode="ref", subject_image="minimax-output/face.jpg",
    output="minimax-output/garden.mp4"
)
```

**Models:** `MiniMax-Hailuo-2.3` (default), `MiniMax-Hailuo-2.3-Fast` (i2v), `MiniMax-Hailuo-02` (1080P, 10s)
**Modes:** `t2v`, `i2v`, `sef` (start-end frame), `ref` (subject reference)

### Video Prompt Tips
Main subject + Scene + Movement + Camera motion + Aesthetic. For i2v: describe motion only, don't repeat what's in the image.

## Generate & Send to Feishu

Use `generate_and_send.py` to generate content and prepare for Feishu delivery via the `feishu-media` skill:

```bash
# Generate TTS and send
python "{skillDir}/scripts/generate_and_send.py" tts "Hello" --voice female-shaonv --feishu-chat <chat_id>

# Generate image and send
python "{skillDir}/scripts/generate_and_send.py" image "A sunset" --ratio 16:9 --feishu-chat <chat_id>

# Set FEISHU_CHAT_ID env var to avoid passing --feishu-chat every time
export FEISHU_CHAT_ID=oc_xxxxx
```

After generation, the script outputs file paths and feishu-media send instructions. Use the `feishu-media` skill to actually deliver the content.

## Legacy PowerShell Script

The original `scripts/minimax-api.ps1` is preserved for backward compatibility but is **deprecated**. Use the Python scripts instead.

## Error Handling

| Error Code | Meaning | Solution |
|-----------|---------|----------|
| 2061 | Plan doesn't support model | Try `speech-02-turbo` for TTS |
| 1008 | Insufficient balance | Top up MiniMax account |
| 2013 | Invalid params | Check required fields |

## References

See `references/` folder for detailed API docs, voice catalogs, and prompt guides.
