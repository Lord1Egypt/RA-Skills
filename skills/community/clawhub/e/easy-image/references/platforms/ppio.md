# PPIO Cloud

## Basic Info
- Website: https://ppio.com
- API Key: https://ppio.com/console
- Documentation: https://ppio.com/docs

## Configuration

### Environment Variables
```bash
export PPIO_API_KEY="your-api-key-here"
```

### Config File (~/.ppio/config.json)
```json
{
  "api_key": "your-api-key-here",
  "base_url": "https://api.ppio.com",
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
| Web Search | Yes | Via search_grounding parameter |

## API Reference

### Text to Image

#### Gemini 3.1 Flash Image (Default, with web search)
- **Endpoint**: `https://api.ppio.com/v3/gemini-3.1-flash-image-text-to-image`
- **Method**: POST
- **Headers**:
  - `Authorization: Bearer <API_KEY>`
  - `Content-Type: application/json`
- **Body**:
```json
{
  "prompt": "A cute cat sitting on a windowsill, sunlight through curtains",
  "width": 1024,
  "height": 1024,
  "aspect_ratio": "1:1",
  "search_grounding": {
    "enabled": true,
    "types": ["web"]
  }
}
```
- **Response**:
```json
{
  "images": [
    {
      "url": "https://...",
      "grounding_info": {
        "queries": [...],
        "sources": [...]
      }
    }
  ]
}
```

#### Enable web + image search
```json
{
  "prompt": "Generate a product image based on the latest Huawei Mate 70 design",
  "width": 1024,
  "height": 1024,
  "search_grounding": {
    "enabled": true,
    "types": ["web", "image"]
  }
}
```

#### Gemini 3 Pro Image (Highest quality)
- **Endpoint**: `https://api.ppio.com/v3/gemini-3-pro-image-text-to-image`
- **Features**: Highest quality, excellent for complex scenes

### Image to Image

#### Gemini 3.1 Flash Image Edit (with web search)
- **Endpoint**: `https://api.ppio.com/v3/gemini-3.1-flash-image-edit`
- **Body**:
```json
{
  "image_url": "https://...",
  "prompt": "Change the background to a beach sunset",
  "strength": 0.7,
  "search_grounding": {
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
| search_grounding | See below | Web search config |

### Grounding Parameters
| Parameter | Value | Description |
|-----------|-------|-------------|
| search_grounding.enabled | `true` | Enable web search |
| search_grounding.types | `["web"]` | Web search only |
| search_grounding.types | `["web", "image"]` | Web + image search |

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
| Seedream 4.0 | CNY 0.20/image | SOTA level |
| Seedream 5.0 Lite | CNY 0.245/image | Fast generation |
| FLUX Schnell | CNY 0.01/image | Ultra fast |
| FLUX Dev | CNY 0.04/image | Balanced |
| Qwen-Image-Edit | CNY 0.15/image | Semantic editing |

## Error Codes
| Code | Meaning | Recommended Action |
|------|---------|-------------------|
| 200 | Success | - |
| 400 | Invalid request | Check parameters |
| 401 | Unauthorized | Check API Key |
| 402 | Insufficient balance | Top up |
| 429 | Rate limited | Wait and retry |
| 500 | Server error | Try later |
