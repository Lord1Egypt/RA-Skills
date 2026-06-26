# Jiekou AI

## Basic Info
- Website: https://jiekou.ai
- API Key: https://jiekou.ai/settings/key-management
- Documentation: https://jiekou.ai/docs

## Configuration

### Environment Variables
```bash
export JIEKOU_API_KEY="your-api-key-here"
```

### Config File (~/.jiekou/config.json)
```json
{
  "api_key": "your-api-key-here",
  "base_url": "https://api.jiekou.ai",
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
| Web Search | Yes | Via tools parameter |

## API Reference

### Text to Image

#### Gemini 3.1 Flash Image (Default, with web search)
- **Endpoint**: `https://api.jiekou.ai/v3/gemini-3.1-flash-image-text-to-image`
- **Method**: POST
- **Headers**:
  - `Authorization: Bearer <API_KEY>`
  - `Content-Type: application/json`
- **Body**:
```json
{
  "prompt": "A cute cat sitting on a windowsill, sunlight through curtains",
  "size": "1K",
  "aspect_ratio": "1:1",
  "output_format": "image/png",
  "tools": [
    {
      "google_search": {}
    }
  ]
}
```
- **Response**:
```json
{
  "image_urls": ["https://..."],
  "grounding_metadata": {
    "search_queries": [...],
    "sources": [...]
  }
}
```

#### Enable web + image search
```json
{
  "prompt": "Generate a product image based on the latest iPhone 16 design",
  "size": "1K",
  "aspect_ratio": "1:1",
  "tools": [
    {
      "google_search": {
        "search_types": ["web", "image"]
      }
    }
  ]
}
```

#### Gemini 3 Pro Image (Highest quality)
- **Endpoint**: `https://api.jiekou.ai/v3/gemini-3-pro-image-text-to-image`
- **Features**: Highest quality, excellent for complex scenes

### Image to Image

#### Gemini 3.1 Flash Image Edit (with web search)
- **Endpoint**: `https://api.jiekou.ai/v3/gemini-3.1-flash-image-edit`
- **Body**:
```json
{
  "image_url": "https://...",
  "prompt": "Change the background to a beach sunset",
  "edit_strength": 0.7,
  "tools": [
    {
      "google_search": {}
    }
  ]
}
```

### Parameters
| Parameter | Values | Description |
|-----------|--------|-------------|
| size | 1K, 2K, 4K | Output resolution |
| aspect_ratio | 1:1, 3:4, 4:3, 9:16, 16:9 | Image aspect ratio |
| output_format | image/png, image/jpeg, image/webp | Output format |
| edit_strength | 0.0-1.0 | Edit intensity |
| tools | See below | Enable web search |

### Grounding Parameters
| Parameter | Value | Description |
|-----------|-------|-------------|
| tools | `[{"google_search": {}}]` | Enable web search |
| search_types | `["web"]` | Web search only |
| search_types | `["web", "image"]` | Web + image search |

## Recommended Models

| Model | Endpoint | Use Case | Notes |
|-------|----------|----------|-------|
| **Gemini 3.1 Flash Image** | `/v3/gemini-3.1-flash-image-text-to-image` | Text to Image | Default recommended |
| **Gemini 3 Pro Image** | `/v3/gemini-3-pro-image-text-to-image` | Text to Image | Highest quality |
| **Gemini 3.1 Flash Edit** | `/v3/gemini-3.1-flash-image-edit` | Image to Image | Default recommended |
| **Gemini 3 Pro Edit** | `/v3/gemini-3-pro-image-edit` | Image to Image | High quality editing |

## Other Supported Image Models

| Model | Description |
|-------|-------------|
| Gemini 2.5 Flash Image | Previous generation, has free quota |
| Seedream 5.0 Lite | ByteDance, fast generation |
| FLUX Schnell | Ultra fast |
| FLUX Dev | Balanced quality and speed |

## Error Codes
| Code | Meaning | Recommended Action |
|------|---------|-------------------|
| 200 | Success | - |
| 400 | Invalid request | Check parameter format |
| 401 | Invalid API Key | Check API Key |
| 402 | Insufficient balance | Top up |
| 429 | Rate limited | Wait and retry |
| 500 | Server error | Try later |
