# Fitness Recipes AI

AI-powered TikTok video generator for fitness content. Creates viral recipe videos from a database, generates AI images via fal.ai, adds voiceover with ElevenLabs, renders video with Shotstack, and posts to TikTok.

## What It Does

- Maintains a recipe database (or fetches from source)
- Generates AI food images using fal.ai
- Creates voiceover scripts and generates audio with ElevenLabs
- Renders complete videos using Shotstack API
- Posts to TikTok via Postiz (optional) or exports for manual upload

## Setup

### Prerequisites

1. **fal.ai API Key** - Get at https://fal.ai
2. **ElevenLabs API Key** - Get at https://elevenlabs.io
3. **Shotstack API Key** - Get at https://shotstack.io
4. **Postiz API Key** (optional) - For auto-posting to TikTok

### Environment Variables

```bash
export FAL_API_KEY="your_fal_key"
export ELEVENLABS_API_KEY="your_elevenlabs_key"
export SHOTSTACK_API_KEY="your_shotstack_key"
export POSTIZ_API_KEY="your_postiz_key"  # optional
```

### Installation

```bash
pip install requests
```

## Usage

### Generate a single video

```bash
python generate_videos.py --recipe "Chicken Breast Recipe" --output my_video.mp4
```

### Run daily batch

```bash
python daily_batch.py --count 10
```

### Custom pipeline

```python
from run_pipeline import Pipeline

pipeline = Pipeline()
video_path = pipeline.run(recipe_name="Keto Salmon", style="fitness")
```

## Configuration

Edit `config.py` or set environment variables:

- `DEFAULT_VOICE` - ElevenLabs voice ID
- `VIDEO_QUALITY` - 1080p or 720p
- `OUTPUT_DIR` - Where videos are saved

## Cost Per Video

| Component | Cost |
|-----------|------|
| fal.ai image | ~$0.01 |
| ElevenLabs voice | ~$0.02 |
| Shotstack render | ~$0.10 |
| **Total** | **~$0.13** |

## Example Output

Videos are saved to `output/` directory with format:
`{recipe_name}_{timestamp}.mp4`

## Files

- `generate_videos.py` - Main video generator
- `run_pipeline.py` - Full pipeline orchestrator
- `fal_client.py` - Image generation
- `elevenlabs_client.py` - Voice generation
- `shotstack_client.py` - Video rendering
- `daily_batch.py` - Batch processor
