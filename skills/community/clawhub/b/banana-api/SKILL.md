---
name: banana-api
description: Generate and edit images using Nano Banana (Gemini-3-Pro-Image-Preview) API. Handles automatic base64 encoding/decoding, image compression, and Discord integration. Use when users want to generate AI images via the Nano Banana service, edit existing photos with AI, or need a streamlined workflow for Gemini image generation without manually handling base64.
---

# Banana API - Nano Banana Image Generation

Streamlined client for Nano Banana's Gemini-3-Pro-Image-Preview API. Automatically handles the annoying base64 workflow, image compression, and Discord sending.

## What This Skill Solves

**The Problem with Gemini API:**
- Input/output is **only base64** (no URLs)
- Large images = massive base64 strings (2MB+)
- Manual encoding/decoding is painful
- No built-in Discord integration

**This Skill Provides:**
- ✅ Automatic image compression (512px default)
- ✅ Transparent base64 encoding/decoding
- ✅ Smart filename generation
- ✅ Auto-send to Discord
- ✅ Both text-to-image and image-to-image editing

## Quick Start

### Text-to-Image
```bash
python3 scripts/banana_gen.py "a cute fluffy cat on a window sill"
```

### Image Editing
```bash
python3 scripts/banana_gen.py "transform into rock concert scene with leather jacket" \
  --image /path/to/photo.png
```

### With Discord Auto-Send
```bash
python3 scripts/banana_gen.py "cyberpunk cityscape at night" \
  --channel-id 1478746465328435412
```

## Configuration

### API Key (Choose One)

**Option 1: Config File (Recommended - Persistent)**
```bash
# Interactive setup (stores in ~/.openclaw/workspace/config/banana-api.json)
python3 scripts/banana_gen.py --setup

# Or manually create config file
echo '{"api_key": "sk-your-key-here"}' > ~/.openclaw/workspace/config/banana-api.json
```

**Option 2: Environment Variable**
```bash
export BANANA_API_KEY="sk-xxxxxxxx"
```

**Option 3: Command Line (One-time)**
```bash
python3 scripts/banana_gen.py "prompt" --api-key "sk-xxx"
```

### Output Location
Generated images are saved to:
```
~/.openclaw/workspace/photos/{description}-{timestamp}.png
```

### View Current Config
```bash
python3 scripts/banana_gen.py --show-config
```

## Usage Examples

### Basic Generation
```bash
# Simple prompt
python3 scripts/banana_gen.py "sunset over mountains"

# With aspect ratio hint
python3 scripts/banana_gen.py "portrait of a warrior" --ratio 2:3

# Custom filename tag
python3 scripts/banana_gen.py "cat playing piano" --name cat-piano
```

### Image Editing (Inpainting/Restyle)
```bash
# Change setting/outfit
python3 scripts/banana_gen.py "wearing a red dress at the beach" \
  --image ~/photos/portrait.png

# Change background
python3 scripts/banana_gen.py "standing in front of Tokyo skyline at night" \
  --image ~/photos/selfie.png \
  --name tokyo-night

# Artistic transformation
python3 scripts/banana_gen.py "oil painting style, renaissance portrait" \
  --image ~/photos/photo.jpg
```

### Discord Integration
```bash
# Auto-send to channel
python3 scripts/banana_gen.py "dragon breathing fire" \
  --channel-id 1478746465328435412

# Auto-send with custom name
python3 scripts/banana_gen.py "cute anime girl with blue hair" \
  --channel-id 1478746465328435412 \
  --name anime-girl

# Save locally only (no Discord)
python3 scripts/banana_gen.py "prompt" --no-send
```

### Advanced Options
```bash
# Custom output path
python3 scripts/banana_gen.py "prompt" --output ~/Desktop/my-image.png

# Different model (if available)
python3 scripts/banana_gen.py "prompt" --model gemini-2.5-flash-image

# Full example
python3 scripts/banana_gen.py "wizard casting spell in ancient library" \
  --image ~/photos/me.png \
  --ratio 2:3 \
  --name wizard-me \
  --channel-id 1478746465328435412
```

## Best Practices

### Image Editing Tips
1. **Compress input automatically**: Script resizes to 512px by default
2. **Be specific**: "wearing black leather jacket" > "cool outfit"
3. **Preserve identity**: Face features are usually maintained well
4. **Aspect ratio**: Add to prompt, but actual output depends on model

### Prompt Engineering
- **Style keywords**: "oil painting", "anime style", "photorealistic"
- **Lighting**: "dramatic lighting", "soft golden hour", "neon lights"
- **Quality**: "high quality", "detailed", "8k"

### File Naming
The script auto-generates filenames:
- Format: `banana-{description}-{timestamp}.png`
- Description is cleaned from prompt (first 30 chars)
- Use `--name` for custom suffix: `banana-{name}-{timestamp}.png`

## Technical Details

### Image Processing Pipeline
```
Input Image → Resize to 512px → JPEG compress (85%) → Base64 encode → API
                                              ↓
Output ← Base64 decode ← PNG save ← Response
```

### API Flow
```
1. Compress input image (if provided)
2. Build Gemini API request with base64 inlineData
3. POST to /v1beta/models/{model}:generateContent
4. Extract image from response.candidates[0].content.parts
5. Decode base64 and save to workspace/photos/
6. Send to Discord (if channel-id provided)
```

### Error Handling
- Input file not found → Clear error message
- API key missing → Prompt to set BANANA_API_KEY
- Image too large → Automatic compression
- API error → JSON error details printed
- Discord send fail → Warning but continues

## Limitations

- **Output always base64**: Cannot be changed (Gemini limitation)
- **No URL input**: Must download images locally first
- **Single image output**: Gemini returns one image per request
- **Response time**: 10-60 seconds depending on complexity

## When to Use This vs Other Tools

| Use Case | Recommended Tool |
|----------|-----------------|
| Quick Gemini image | **banana-api** ✅ |
| ComfyUI workflows | comfyui-gen |
| DALL-E / OpenAI | Use their direct API |
| Stable Diffusion | comfyui-gen |

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "PIL not available" | Install: `pip install Pillow` |
| "API key required" | Run `--setup` to save key, or set `BANANA_API_KEY` env var |
| "No image data found" | Model may have returned text only; try different prompt |
| Large output files | Normal for high-res images (500KB-2MB) |
| Discord send fails | Check channel ID and openclaw CLI access |

## Configuration Priority

API Key is loaded in this order (first found wins):
1. `--api-key` command line argument
2. `BANANA_API_KEY` environment variable  
3. `~/.openclaw/workspace/config/banana-api.json` config file
4. ❌ Error if none found

To persist the API key for future use:
```bash
python3 scripts/banana_gen.py --setup
```

## Script Reference

```bash
python3 scripts/banana_gen.py [PROMPT] [OPTIONS]

Options:
  --image, -i PATH       Input image for editing
  --ratio, -r RATIO      Aspect ratio hint (e.g., 2:3, 16:9)
  --model, -m MODEL      Model name (default: gemini-3-pro-image-preview)
  --output, -o PATH      Custom output path
  --name, -n NAME        Filename suffix/tag
  --channel-id, -c ID    Discord channel ID to auto-send
  --no-send              Skip Discord sending
  --api-key, -k KEY      API key (or set BANANA_API_KEY)
  --setup                Interactive setup to save API key
  --show-config          Display current configuration
```

## Integration with Workflows

### As Part of a Larger Pipeline
```bash
# Generate + send + reference
IMAGE=$(python3 scripts/banana_gen.py "cute cat" --name kitty | grep "OUTPUT_PATH:" | cut -d: -f2-)
echo "Generated: $IMAGE"
```

### From Another Skill
Call the script directly:
```python
import subprocess
result = subprocess.run([
    'python3', 'scripts/banana_gen.py',
    'prompt here',
    '--image', input_path,
    '--channel-id', channel_id
], capture_output=True, text=True)
```
