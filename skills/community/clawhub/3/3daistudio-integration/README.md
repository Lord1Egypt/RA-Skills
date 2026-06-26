# 3D AI Studio Skill

A skill for converting images and text prompts to 3D models using the 3D AI Studio API.

## Owner

Whale Professor (@WhaleProfessor on Telegram)

## Homepage

https://www.3daistudio.com

## Setup

1. Get an API key from https://www.3daistudio.com/Platform/API
2. Set the environment variable:
   ```bash
   export THREE_D_AI_STUDIO_API_KEY="your-api-key"
   ```
3. Run the skill:
   ```bash
   python 3daistudio.py balance
   ```

## Supported Models

- **TRELLIS.2** - Image to 3D (fastest, cheapest)
- **Hunyuan Rapid** - Text or image to 3D (balanced)
- **Hunyuan Pro** - Text or image to 3D (highest quality)

## Quick Start

```bash
# Check balance
python 3daistudio.py balance

# Image to 3D with TRELLIS.2
python 3daistudio.py trellis --image photo.png -o model.glb

# Text to 3D with Hunyuan Pro
python 3daistudio.py pro --prompt "a cute blue hedgehog" -o hedgehog.glb
```

## License

MIT
