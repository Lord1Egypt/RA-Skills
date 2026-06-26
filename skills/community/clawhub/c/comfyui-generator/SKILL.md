# ComfyUI Generator Skill

## Overview
Integration between OpenClaw and ComfyUI for AI media generation.

## Features
- Text-to-image generation
- Image style transfer
- Batch processing
- Automated workflow management
- File monitoring and archiving

## Installation

### Prerequisites
1. ComfyUI installed at `C:\ComfyUI`
2. ComfyUI service running on `http://127.0.0.1:8188`
3. OpenClaw 2026.4.5+

### Setup
```bash
# Set environment variables
export COMFY_API_KEY="local_comfyui"
export COMFY_BASE_URL="http://127.0.0.1:8188"

# Copy workflow files
cp -r workflows/*.json "C:\ComfyUI\input\workflows\"
```

## Usage

### Generate Image
```bash
openclaw comfy generate --prompt "a beautiful landscape" --style cyberpunk
```

### Style Transfer
```bash
openclaw comfy style --image "path/to/image.jpg" --style "van gogh"
```

### Batch Processing
```bash
openclaw comfy batch --input prompts.txt --output output_dir --iterations 5
```

## Configuration

### Environment Variables
```bash
COMFY_API_KEY="local_comfyui"
COMFY_BASE_URL="http://127.0.0.1:8188"
COMFY_OUTPUT_DIR="C:\ComfyUI\output"
```

### Workflow Configuration
Place workflow JSON files in:
```
C:\ComfyUI\input\workflows\
```

## Examples

### Basic Image Generation
```python
from comfy_client import ComfyUIClient

client = ComfyUIClient()
result = client.generate_image(
    prompt="a futuristic city at night",
    workflow="image_generation.json"
)
```

### Style Transfer
```python
result = client.style_transfer(
    image_path="input.jpg",
    style="cyberpunk",
    workflow="style_transfer.json"
)
```

## Troubleshooting

### Service Not Running
```bash
# Check if ComfyUI is running
curl http://127.0.0.1:8188

# Start ComfyUI
python "C:\ComfyUI\main.py" --listen 127.0.0.1 --port 8188
```

### API Connection Issues
1. Verify firewall allows port 8188
2. Check ComfyUI logs in `C:\ComfyUI\logs\`
3. Ensure API key is set correctly

### Generation Quality
- Use detailed prompts
- Adjust workflow parameters
- Try different models

## Files

### Core Scripts
- `scripts/comfy_client.py` - API client
- `scripts/prompt_generator.py` - Prompt optimization
- `scripts/file_monitor.py` - Output monitoring

### Workflow Files
- `workflows/image_generation.json` - Basic image generation
- `workflows/style_transfer.json` - Style transfer
- `workflows/upscale.json` - Image upscaling

### Configuration
- `config/settings.yaml` - Skill configuration
- `config/prompt_templates.json` - Prompt templates

## License
MIT License

## Support
For issues and questions, please check:
1. ComfyUI documentation
2. OpenClaw documentation
3. Skill logs in `C:\Users\LEI\.openclaw\logs\`