# OpenRouter

## Basic Info
- Website: https://openrouter.ai
- API Key: https://openrouter.ai/settings/keys
- Documentation: https://openrouter.ai/docs

## Configuration

### Environment Variables
```bash
export OPENROUTER_API_KEY="your-api-key-here"
```

### Config File (~/.openrouter/config.json)
```json
{
  "api_key": "your-api-key-here",
  "base_url": "https://openrouter.ai/api/v1",
  "default_model": "google/gemini-3.1-flash-image-preview",
  "timeout": 300,
  "enable_grounding": true
}
```

## Capabilities
| Capability | Supported | Recommended Model |
|------------|-----------|-------------------|
| Text to Image | Yes | Gemini 3.1 Flash Image |
| Image to Image | Yes | Gemini 3.1 Flash Image |
| Web Search | Yes | Via plugins or provider parameter |

## API Reference

### Text to Image

#### Gemini 3.1 Flash Image (Default, with web search)
- **Endpoint**: `https://openrouter.ai/api/v1/chat/completions`
- **Method**: POST
- **Headers**:
  - `Authorization: Bearer <API_KEY>`
  - `Content-Type: application/json`
- **Body**:
```json
{
  "model": "google/gemini-3.1-flash-image-preview",
  "messages": [
    {
      "role": "user",
      "content": "Generate an image of a cute cat sitting on a windowsill, morning sunlight"
    }
  ],
  "modalities": ["image", "text"],
  "plugins": [
    {
      "id": "web",
      "config": {
        "engine": "native"
      }
    }
  ]
}
```

#### Using provider parameter for web search
```json
{
  "model": "google/gemini-3.1-flash-image-preview",
  "messages": [
    {
      "role": "user",
      "content": "Generate an image based on the latest Tesla Model S design"
    }
  ],
  "modalities": ["image", "text"],
  "provider": {
    "google": {
      "tools": [
        {
          "google_search": {}
        }
      ]
    }
  }
}
```

- **Response**:
```json
{
  "choices": [
    {
      "message": {
        "content": [
          {
            "type": "image_url",
            "image_url": {
              "url": "data:image/png;base64,..."
            }
          }
        ]
      }
    }
  ]
}
```

#### Gemini 3 Pro Image (Highest quality)
```json
{
  "model": "google/gemini-3-pro-image",
  "messages": [
    {
      "role": "user",
      "content": "A professional portrait photo with studio lighting"
    }
  ],
  "modalities": ["image", "text"],
  "plugins": [
    {
      "id": "web",
      "config": {
        "engine": "native"
      }
    }
  ]
}
```

### Image to Image

#### Gemini Image Edit (with web search)
```json
{
  "model": "google/gemini-3.1-flash-image-preview",
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "image_url",
          "image_url": {
            "url": "https://example.com/image.jpg"
          }
        },
        {
          "type": "text",
          "text": "Change the background to a beach sunset"
        }
      ]
    }
  ],
  "modalities": ["image", "text"],
  "plugins": [
    {
      "id": "web",
      "config": {
        "engine": "native"
      }
    }
  ]
}
```

### Grounding Parameters
| Parameter | Value | Description |
|-----------|-------|-------------|
| plugins | `[{"id": "web", "config": {"engine": "native"}}]` | Use native search |
| provider.google.tools | `[{"google_search": {}}]` | Pass-through Google parameter |
| modalities | `["image", "text"]` | Must specify |

## Recommended Models

| Model | Model ID | Use Case | Notes |
|-------|----------|----------|-------|
| **Gemini 3.1 Flash Image** | `google/gemini-3.1-flash-image-preview` | Text to Image / Image to Image | Default recommended |
| **Gemini 3 Pro Image** | `google/gemini-3-pro-image` | Text to Image / Image to Image | Highest quality |

## Other Supported Image Models

| Model | Model ID | Description |
|-------|----------|-------------|
| Gemini 2.5 Flash Image | `google/gemini-2.5-flash-image-preview` | Previous generation |
| Seedream 4.5 | `bytedance/seedream-4.5` | ByteDance |
| Riverflow V2 Pro | `sourceful/riverflow-v2-pro` | Good text rendering |
| GPT-5 Image | `openai/gpt-5-image` | OpenAI |

## Error Codes
| Code | Meaning | Recommended Action |
|------|---------|-------------------|
| 200 | Success | - |
| 400 | Invalid request | Check modalities parameter |
| 401 | Unauthorized | Check API Key |
| 402 | Insufficient balance | Top up |
| 429 | Rate limited | Wait and retry |
| 502 | Upstream error | Try later |
