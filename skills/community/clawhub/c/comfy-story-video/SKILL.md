---
name: comfy-story-video
description: Generate children's story videos using ComfyUI. Use when: (1) Creating illustrated children's stories, (2) Generating story images with AI, (3) Converting text stories to video with TTS narration, (4) Building children's educational content. Requires ComfyUI running on http://127.0.0.1:8188.
---

# Comfy Story Video

Generate children's story videos with AI-generated illustrations and voice narration.

## Quick Start

```bash
cd /Users/yiyi/.openclaw/workspace/comfy-story-video
python3 scripts/generate_story_video.py --theme "友谊" --scenes 5
```

## Requirements

1. **ComfyUI running** on `http://127.0.0.1:8188`
2. **Python dependencies**: `pip install websocket-client requests`
3. **FFmpeg** for audio conversion

## Usage

### Generate a Story Video

```bash
# Default theme (友谊/friendship)
python3 scripts/generate_story_video.py

# Custom theme
python3 scripts/generate_story_video.py --theme "勇气"

# Custom number of scenes
python3 scripts/generate_story_video.py --theme "环保" --scenes 6
```

### Output Files

Generated in `output/` directory:
- `story_{theme}_{timestamp}.json` - Story text
- `scene_01.png` ~ `scene_NN.png` - AI illustrations
- `scene_01.mp3` ~ `scene_NN.mp3` - Voice narration
- `story_{theme}_{timestamp}.mp4` - Final video

## Customization

### Change ComfyUI Model

Edit `assets/basic_workflow.json`, replace `ckpt_name` in `CheckpointLoaderSimple` node.

### Modify Characters/Settings

Edit `scripts/generate_story_video.py`:
- `characters` - List of animal characters
- `settings` - Story backgrounds
- `themes` - Story themes

### Change Voice

Modify the `-v` parameter in `generate_tts()` function:
```bash
say -v '?' | grep zh  # List available Chinese voices
```

## Workflow

1. Generate story text (configurable characters, setting, theme)
2. Convert each scene to ComfyUI prompt
3. Send to ComfyUI for image generation
4. Generate TTS narration for each scene
5. Combine into video (WIP)

## Troubleshooting

- **ComfyUI not responding**: Check if ComfyUI is running at `http://127.0.0.1:8188`
- **Model not found**: Update `ckpt_name` in workflow to match available models
- **Image generation fails**: Check ComfyUI console for error messages
