# Google AI (Gemini API)

## Basic Info
- Website: https://ai.google.dev
- API Key: https://aistudio.google.com/app/apikey
- Documentation: https://ai.google.dev/gemini-api/docs
- AI Studio: https://aistudio.google.com

## Configuration

### Environment Variables
```bash
export GOOGLE_API_KEY="your-api-key-here"
```

### Config File (~/.google/config.json)
```json
{
  "api_key": "your-api-key-here",
  "base_url": "https://generativelanguage.googleapis.com/v1beta",
  "default_model": "gemini-3.1-flash-image-preview",
  "timeout": 300,
  "enable_grounding": true
}
```

## Capabilities
| Capability | Supported | Recommended Model |
|------------|-----------|-------------------|
| Text to Image | Yes | Gemini 3.1 Flash Image |
| Image to Image | Yes | Gemini 3.1 Flash Image |
| Web Search | Yes | Gemini 3.1 Flash Image (enabled by default) |

## API Reference

### Text to Image

#### Gemini 3.1 Flash Image (Default, with web search)
- **Endpoint**: `https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-image-preview:generateContent`
- **Method**: POST
- **URL Params**: `?key=<API_KEY>`
- **Body**:
```json
{
  "contents": [
    {
      "parts": [
        {
          "text": "Generate an image of a cute cat sitting on a windowsill, morning sunlight"
        }
      ]
    }
  ],
  "generationConfig": {
    "responseModalities": ["TEXT", "IMAGE"],
    "temperature": 1.0
  },
  "tools": [
    {
      "google_search": {}
    }
  ]
}
```

#### Enable Image Search + Web Search
```json
{
  "contents": [
    {
      "parts": [
        {
          "text": "Generate an image based on the latest iPhone design"
        }
      ]
    }
  ],
  "generationConfig": {
    "responseModalities": ["TEXT", "IMAGE"],
    "temperature": 1.0
  },
  "tools": [
    {
      "googleSearch": {
        "searchTypes": {
          "webSearch": {},
          "imageSearch": {}
        }
      }
    }
  ]
}
```

- **Response**:
```json
{
  "candidates": [
    {
      "content": {
        "parts": [
          {
            "inlineData": {
              "mimeType": "image/png",
              "data": "base64_encoded_image..."
            }
          }
        ]
      },
      "groundingMetadata": {
        "searchEntryPoint": {...},
        "groundingChunks": [...]
      }
    }
  ]
}
```

#### Gemini 3 Pro Image (Highest quality)
- **Endpoint**: `https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image:generateContent`
- **Features**: Highest quality, excellent for complex scenes
- **Note**: Same grounding parameters

### Image to Image

#### Gemini Multi-turn Edit (with web search)
```json
{
  "contents": [
    {
      "role": "user",
      "parts": [
        {
          "inlineData": {
            "mimeType": "image/jpeg",
            "data": "base64_encoded_image..."
          }
        },
        {
          "text": "Change the background to a beach sunset"
        }
      ]
    }
  ],
  "generationConfig": {
    "responseModalities": ["TEXT", "IMAGE"],
    "temperature": 1.0
  },
  "tools": [
    {
      "google_search": {}
    }
  ]
}
```

### Grounding Parameters
| Parameter | Value | Description |
|-----------|-------|-------------|
| tools | `[{"google_search": {}}]` | Enable Google Search |
| searchTypes.webSearch | `{}` | Web search |
| searchTypes.imageSearch | `{}` | Image search (3.1 Flash only) |
| temperature | `1.0` | Recommended for best results |

### Grounding Pricing
- **Gemini 3 series**: $14 / 1000 search queries
- **Gemini 2.5 and earlier**: $35 / 1000 prompts
- Empty search queries are not charged

## Recommended Models

| Model | Model ID | Use Case | Notes |
|-------|----------|----------|-------|
| **Gemini 3.1 Flash Image** | `gemini-3.1-flash-image-preview` | Text to Image / Image to Image | Default recommended, supports image search |
| **Gemini 3 Pro Image** | `gemini-3-pro-image` | Text to Image / Image to Image | Highest quality |

## Other Supported Image Models

| Model | Model ID | Price | Description |
|-------|----------|-------|-------------|
| Gemini 2.5 Flash Image | `gemini-2.5-flash-image-preview` | Free 500/day | Previous generation |
| Imagen 4 Fast | `imagen-4-fast` | $0.02/image | Fast generation |
| Imagen 4 Standard | `imagen-4` | $0.04/image | Standard quality |
| Imagen 4 Ultra | `imagen-4-ultra` | $0.06/image | Highest quality |

## Error Codes
| Code | Meaning | Recommended Action |
|------|---------|-------------------|
| 200 | Success | - |
| 400 | Invalid request | Check parameter format |
| 401 | Invalid API Key | Get new API Key |
| 429 | Quota exceeded | Wait for reset or upgrade |
| SAFETY | Safety filter | Modify prompt |
