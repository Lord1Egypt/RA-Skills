# EchoFlow API Reference

EchoFlow API (https://api.echoflow.cn/) is an OpenAI-compatible API gateway that provides access to 580+ AI models including image generation models.

## Authentication

All requests require an API key in the Authorization header:

```
Authorization: Bearer YOUR_API_KEY
```

Get your API key from: https://api.echoflow.cn/

## Base URL

```
https://api.echoflow.cn/v1
```

## Image Generation Endpoint

### POST /images/generations

Generate images from text prompts.

**Request Body:**

```json
{
  "model": "gpt-image-1",
  "prompt": "a beautiful sunset over mountains",
  "size": "1024x1024",
  "n": 1,
  "response_format": "b64_json",
  "quality": "standard",
  "style": "vivid"
}
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `model` | string | Model: `gpt-image-1`, `dall-e-3`, `dall-e-2` |
| `prompt` | string | Image description |
| `size` | string | Image dimensions |
| `n` | integer | Number of images (usually 1) |
| `response_format` | string | `b64_json` or `url` |
| `quality` | string | `standard` or `hd` (DALL-E 3) |
| `style` | string | `vivid` or `natural` (DALL-E 3) |

**Response:**

```json
{
  "created": 1234567890,
  "data": [
    {
      "b64_json": "base64_encoded_image_data..."
    }
  ]
}
```

## Image Editing Endpoint

### POST /images/edits (DALL-E 2)

Edit an existing image.

**Request:** multipart/form-data

| Field | Type | Description |
|-------|------|-------------|
| `image` | file | Source image (PNG, max 4MB) |
| `prompt` | string | Edit instructions |
| `n` | integer | Number of results |
| `size` | string | Output size |
| `response_format` | string | `b64_json` or `url` |

## Chat Completions with Images (GPT-image-1)

GPT-image-1 supports image input via the chat completions API:

```json
{
  "model": "gpt-image-1",
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "image_url",
          "image_url": {
            "url": "data:image/png;base64,BASE64_DATA"
          }
        },
        {
          "type": "text",
          "text": "Edit instructions here"
        }
      ]
    }
  ]
}
```

## Error Handling

Errors are returned in OpenAI format:

```json
{
  "error": {
    "message": "Error description",
    "type": "invalid_request_error",
    "code": "invalid_api_key"
  }
}
```

## Rate Limits

EchoFlow handles rate limiting. If you receive a 429 error, wait and retry with exponential backoff.

## Pricing

Refer to EchoFlow dashboard for current pricing: https://api.echoflow.cn/
