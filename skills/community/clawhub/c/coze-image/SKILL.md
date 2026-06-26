---
name: coze-image
description: Generate images using Coze AI platform. Supports text-to-image generation with automatic Base64 encoding for inline preview. Use when you need to create images from text prompts.
metadata:
  {
    "openclaw":
      {
        "env":
          [
            { "name": "IMAGE_API_TOKEN", "description": "Coze API authentication token", "required": true },
            { "name": "IMAGE_API_URL", "description": "Coze stream_run endpoint", "default": "https://6fj9k4p9x3.coze.site/stream_run" },
            { "name": "IMAGE_API_PROJECT_ID", "description": "Coze project ID", "default": "7621854258107039796" },
            { "name": "IMAGE_API_SESSION_ID", "description": "Coze session ID", "default": "mT8SQeCGgTMZNBsJEiRuN" },
            { "name": "IMAGE_API_TIMEOUT", "description": "Request timeout in seconds", "default": "60" },
          ],
      },
    "clawhub":
      {
        "version": "1.0.0",
        "author": "OpenClaw Community",
        "license": "MIT",
        "tags": ["image", "generation", "coze", "ai", "text-to-image"],
        "repository": "https://github.com/openclaw/skills",
      },
  }
---

# Coze Image Generation Skill

Generate images from text prompts using the Coze AI platform. This skill handles the complete workflow: submitting prompts, parsing SSE responses, downloading images, and returning Base64-encoded data URIs for inline display.

## Usage

### Basic Usage

```python
from coze_image_skill import run

result = run({
    "text": "一只可爱的小猫，毛茸茸的，大眼睛，坐在窗台上",
    "api_token": "your_coze_api_token"
})

# Result contains:
# - image: data:image/jpeg;base64,... (inline Base64)
# - mime_type: image/jpeg
# - filename: generated-image.jpeg
# - source_url: original image URL
```

### With Custom Configuration

```python
result = run({
    "prompt": "a cute orange cat playing on grass, sunny day",
    "api_token": "your_token",
    "project_id": "your_project_id",
    "session_id": "your_session_id",
    "timeout": 90,
    "include_debug": True
})
```

## Environment Variables

Set these in your OpenClaw configuration or `.env` file:

| Variable | Description | Default |
|----------|-------------|---------|
| `IMAGE_API_TOKEN` | Coze API authentication token | Required |
| `IMAGE_API_URL` | Coze stream_run endpoint | `https://6fj9k4p9x3.coze.site/stream_run` |
| `IMAGE_API_PROJECT_ID` | Coze project ID | `7621854258107039796` |
| `IMAGE_API_SESSION_ID` | Coze session ID | `mT8SQeCGgTMZNBsJEiRuN` |
| `IMAGE_API_TIMEOUT` | Request timeout in seconds | `60` |

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `text` or `prompt` | string | Image generation prompt (required) |
| `api_token` | string | Coze API token (or use env var) |
| `project_id` | string | Coze project ID (or use env var) |
| `session_id` | string | Coze session ID (or use env var) |
| `timeout` | int | Request timeout in seconds |
| `include_debug` | bool | Include debug info in response |
| `strict` | bool | Raise exceptions instead of returning error object |

## Response Format

### Success

```json
{
  "image": "data:image/jpeg;base64,/9j/4AAQSkZJRg...",
  "mime_type": "image/jpeg",
  "filename": "generated-image.jpeg",
  "source_url": "https://..."
}
```

### Error

```json
{
  "error": "Error message describing what went wrong",
  "image": null,
  "mime_type": null,
  "filename": null,
  "source_url": null
}
```

## Features

- **SSE Streaming**: Handles Coze's Server-Sent Events response format
- **Auto Download**: Automatically downloads generated images and converts to Base64
- **Error Handling**: Graceful error handling with structured error responses
- **Flexible Auth**: Supports both inline token and environment variables
- **Debug Mode**: Optional debug output for troubleshooting

## Setup on ClawHub

1. Install the skill via ClawHub:
   ```bash
   openclaw skills install coze-image
   ```

2. Configure your API token:
   ```bash
   openclaw config set IMAGE_API_TOKEN your_token_here
   ```

3. Generate your first image:
   ```
   Generate a picture of a sunset over the ocean
   ```

## Troubleshooting

### "Image URL not found in SSE response"

This means the Coze project returned text instead of an image. Make sure:
- Your Coze bot has an image generation plugin enabled
- The workflow is configured to return images
- The prompt is appropriate for image generation

### Authentication Errors

- Verify your API token is valid and not expired
- Check that the token has permission to access the project
- Ensure environment variables are set correctly

### Timeout Errors

- Increase the timeout parameter (default 60s)
- Check your network connection
- The image generation may be taking longer than expected

## License

MIT License - See license file for details.

## Support

For issues or questions, please open an issue on the ClawHub repository.
