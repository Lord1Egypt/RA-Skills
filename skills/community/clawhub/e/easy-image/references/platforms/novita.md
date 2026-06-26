# Novita AI

## Basic Info
- Website: https://novita.ai
- API Key: https://novita.ai/settings/key-management
- Documentation: https://docs.novita.ai

## Configuration

### Environment Variables
```bash
export NOVITA_API_KEY="your-api-key-here"
```

### Config File (~/.novita/config.json)
```json
{
  "api_key": "your-api-key-here",
  "base_url": "https://api.novita.ai",
  "default_model": "gemini-3.1-flash-image",
  "timeout": 300,
  "enable_grounding": true
}
```

## Capabilities
| Capability | Supported | Recommended Model |
|------------|-----------|-------------------|
| Text to Image | Yes | Gemini 3.1 Flash Image |
| Image to Image | Yes | Gemini 3.1 Flash Image |
| Web Search | Yes | Via grounding parameter |

## API Reference

### Text to Image

#### Gemini 3.1 Flash Image (Default, with web search)
- **Endpoint**: `https://api.novita.ai/v3/gemini-3.1-flash-image-text-to-image`
- **Method**: POST
- **Headers**:
  - `Authorization: Bearer <API_KEY>`
  - `Content-Type: application/json`
- **Body**:
```json
{
  "prompt": "A cute cat sitting on a windowsill, morning sunlight",
  "width": 1024,
  "height": 1024,
  "aspect_ratio": "1:1",
  "grounding": {
    "enabled": true,
    "search_types": ["web"]
  }
}
```
- **Response**:
```json
{
  "images": [
    {
      "url": "https://...",
      "grounding_sources": [...]
    }
  ]
}
```

#### Enable web + image search
```json
{
  "prompt": "Generate an image based on the latest MacBook Pro design",
  "width": 1024,
  "height": 1024,
  "grounding": {
    "enabled": true,
    "search_types": ["web", "image"]
  }
}
```

#### Gemini 3 Pro Image (Highest quality)
- **Endpoint**: `https://api.novita.ai/v3/gemini-3-pro-image-text-to-image`
- **Features**: Highest quality, excellent for complex scenes

### Image to Image

#### Gemini 3.1 Flash Image Edit (with web search)
- **Endpoint**: `https://api.novita.ai/v3/gemini-3.1-flash-image-edit`
- **Body**:
```json
{
  "image_url": "https://...",
  "prompt": "Change the background to a beach sunset",
  "strength": 0.7,
  "grounding": {
    "enabled": true
  }
}
```

### Parameters
| Parameter | Values | Description |
|-----------|--------|-------------|
| width | 512-4096 | Image width |
| height | 512-4096 | Image height |
| aspect_ratio | 1:1, 3:4, 4:3, 9:16, 16:9 | Image aspect ratio |
| strength | 0.0-1.0 | Edit intensity |
| grounding | See below | Web search config |

### Grounding Parameters
| Parameter | Value | Description |
|-----------|-------|-------------|
| grounding.enabled | `true` | Enable web search |
| grounding.search_types | `["web"]` | Web search only |
| grounding.search_types | `["web", "image"]` | Web + image search |

## Recommended Models

| Model | Endpoint | Use Case | Notes |
|-------|----------|----------|-------|
| **Gemini 3.1 Flash Image** | `/v3/gemini-3.1-flash-image-text-to-image` | Text to Image | Default recommended |
| **Gemini 3 Pro Image** | `/v3/gemini-3-pro-image-text-to-image` | Text to Image | Highest quality |
| **Gemini 3.1 Flash Edit** | `/v3/gemini-3.1-flash-image-edit` | Image to Image | Default recommended |
| **Gemini 3 Pro Edit** | `/v3/gemini-3-pro-image-edit` | Image to Image | High quality editing |

## Other Supported Image Models

| Model | Price | Description |
|-------|-------|-------------|
| FLUX Schnell | $0.0015/image | Ultra fast |
| FLUX Dev | $0.006/image | Balanced |
| FLUX Pro | $0.03/image | High quality |
| Seedream 5.0 Lite | $0.035/image | ByteDance |
| SDXL 1.0 | $0.002/image | Classic Stable Diffusion |

## Error Codes
| Code | Meaning | Recommended Action |
|------|---------|-------------------|
| 200 | Success | - |
| 400 | Invalid request | Check parameters |
| 401 | Unauthorized | Check API Key |
| 402 | Insufficient balance | Top up |
| 429 | Rate limited | Wait and retry |
| 500 | Server error | Try later |
