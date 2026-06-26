# WaveSpeed AI

## Basic Info
- Website: https://wavespeed.ai
- API Key: https://wavespeed.ai/console
- Documentation: https://wavespeed.ai/docs

## Configuration

### Environment Variables
```bash
export WAVESPEED_API_KEY="your-api-key-here"
```

### Config File (~/.wavespeed/config.json)
```json
{
  "api_key": "your-api-key-here",
  "base_url": "https://api.wavespeed.ai",
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
| Web Search | Yes | Via web_search parameter |

## API Reference

### Text to Image

#### Gemini 3.1 Flash Image (Default, with web search)
- **Endpoint**: `https://api.wavespeed.ai/v1/images/generations`
- **Method**: POST
- **Headers**:
  - `Authorization: Bearer <API_KEY>`
  - `Content-Type: application/json`
- **Body**:
```json
{
  "model": "gemini-3.1-flash-image",
  "prompt": "A cute cat sitting on a windowsill, morning sunlight",
  "size": "1024x1024",
  "n": 1,
  "web_search": {
    "enabled": true,
    "types": ["web"]
  }
}
```
- **Response**:
```json
{
  "data": [
    {
      "url": "https://...",
      "revised_prompt": "...",
      "search_results": [...]
    }
  ]
}
```

#### Enable web + image search
```json
{
  "model": "gemini-3.1-flash-image",
  "prompt": "Generate an image based on the latest Nike Air Jordan design",
  "size": "1024x1024",
  "web_search": {
    "enabled": true,
    "types": ["web", "image"]
  }
}
```

#### Gemini 3 Pro Image (Highest quality)
```json
{
  "model": "gemini-3-pro-image",
  "prompt": "A professional portrait photo with studio lighting",
  "size": "1024x1024",
  "web_search": {
    "enabled": true
  }
}
```

### Image to Image

#### Gemini 3.1 Flash Image Edit (with web search)
- **Endpoint**: `https://api.wavespeed.ai/v1/images/edits`
- **Body**:
```json
{
  "model": "gemini-3.1-flash-image",
  "image_url": "https://...",
  "prompt": "Change the background to a beach sunset",
  "strength": 0.7,
  "web_search": {
    "enabled": true
  }
}
```

### Parameters
| Parameter | Values | Description |
|-----------|--------|-------------|
| size | 512x512, 1024x1024, 2048x2048 | Output dimensions |
| n | 1-4 | Number of images |
| strength | 0.0-1.0 | Edit intensity |
| web_search | See below | Web search config |

### Grounding Parameters
| Parameter | Value | Description |
|-----------|-------|-------------|
| web_search.enabled | `true` | Enable web search |
| web_search.types | `["web"]` | Web search only |
| web_search.types | `["web", "image"]` | Web + image search |

## Recommended Models

| Model | Model ID | Use Case | Notes |
|-------|----------|----------|-------|
| **Gemini 3.1 Flash Image** | `gemini-3.1-flash-image` | Text to Image / Image to Image | Default recommended |
| **Gemini 3 Pro Image** | `gemini-3-pro-image` | Text to Image / Image to Image | Highest quality |

## Other Supported Image Models

| Model | Model ID | Price | Description |
|-------|----------|-------|-------------|
| FLUX Schnell | `flux-1-schnell` | $0.002/image | Ultra fast |
| FLUX Dev | `flux-1-dev` | $0.01/image | Balanced |
| FLUX Pro | `flux-1-pro` | $0.05/image | High quality |
| FLUX Ultra | `flux-1-ultra` | $0.06/image | Ultra high resolution |
| SDXL 1.0 | `sdxl-1.0` | $0.003/image | Classic Stable Diffusion |

## Error Codes
| Code | Meaning | Recommended Action |
|------|---------|-------------------|
| 200 | Success | - |
| 400 | Invalid request | Check parameters |
| 401 | Unauthorized | Check API Key |
| 402 | Insufficient balance | Top up |
| 429 | Rate limited | Wait and retry |
| 500 | Server error | Try later |
