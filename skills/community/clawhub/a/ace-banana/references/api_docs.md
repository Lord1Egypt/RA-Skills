# Nano Banana Images API Documentation

## Overview
This API supports image generation and editing.

- **Base URL**: `https://api.acedata.cloud`
- **Endpoint**: `POST /nano-banana/images`
- **Authentication**: `Bearer {token}` in `Authorization` header.

## Request Parameters
- `action`: `generate` or `edit`
- `model`: `nano-banana`, `nano-banana-2` (default for this skill), `nano-banana-pro`
- `prompt`: Text description of the image.
- `count`: Number of images to generate.
- `image_urls`: Array of image URLs or Base64 strings (required for `edit`).

## Example Response
```json
{
 "success": true,
 "task_id": "...",
 "data": [
  {
   "prompt": "...",
   "image_url": "..."
  }
 ]
}
```

## Note on Errors
- **403 Forbidden**: Usually means the API Key is invalid, has no quota, or the specific service (Nano Banana) hasn't been enabled for this key.
