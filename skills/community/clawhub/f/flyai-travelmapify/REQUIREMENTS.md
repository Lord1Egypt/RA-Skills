# Requirements

The `flyai-travelmapify` skill requires the following dependencies to function properly:

## Required Skills
- **[amap-maps](https://github.com/openclaw/openclaw/tree/main/skills/amap-maps)** - Provides Amap LBS services for geocoding, POI search, and location services

## API Keys
- **Amap API**: Built-in default API key included (`88628414733cf2ccb7ce2f94cfd680ef`)
- **No user API key required** - the skill works out of the box with the default key

## AI Vision Requirements
- **Image-capable AI model**: Your OpenClaw agent should have access to an image analysis model for processing travel planning images
- **Supported image formats**: JPG, PNG, GIF, WebP
- **Recommended image quality**: Clear, readable text with good contrast for optimal POI extraction

## Installation
Both skills should be installed in your OpenClaw workspace under the `skills/` directory:

```
~/.openclaw/workspace/
├── skills/
│   ├── flyai-travelmapify/
│   └── amap-maps/
```

## Verification
To verify both skills are properly installed, check that these directories exist:
- `~/.openclaw/workspace/skills/flyai-travelmapify/`
- `~/.openclaw/workspace/skills/amap-maps/`

The `flyai-travelmapify` skill will automatically detect and use the `amap-maps` skill via relative path resolution.