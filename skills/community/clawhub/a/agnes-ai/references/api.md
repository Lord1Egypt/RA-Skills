# Agnes AI API Reference

## Base URL

```
https://apihub.agnes-ai.com/v1
```

## Authentication

All requests require an `Authorization: Bearer <api_key>` header.

## Models

| Model ID                 | Type  | Description                                              |
| ------------------------ | ----- | -------------------------------------------------------- |
| `agnes-image-2.1-flash` | Image | Text-to-image, high information density, best quality   |
| `agnes-image-2.0-flash` | Image | Image-to-image, multi-image composition, fast editing   |
| `agnes-video-v2.0`     | Video | Video generation model                                 |

## Endpoints

### Image Generation — Text-to-Image (agnes-image-2.1-flash)

```
POST /v1/images/generations
```

**Request Body:**

```json
{
  "model": "agnes-image-2.1-flash",
  "prompt": "A luminous floating city above a misty canyon at sunrise, cinematic realism",
  "size": "1024x768"
}
```

**Response:**

```json
{
  "created": 1774432125,
  "data": [
    {
      "url": "https://cdn.agnes-ai.com/output/abc123.png"
    }
  ],
  "usage": {
    "generated_images": 1
  }
}
```

---

### Image Generation — Image-to-Image (agnes-image-2.0-flash)

```
POST /v1/images/generations
```

**Request Body:**

```json
{
  "model": "agnes-image-2.0-flash",
  "tags": ["img2img"],
  "prompt": "Transform this image into a cinematic cyberpunk style while preserving the main subject and composition",
  "size": "1024x768",
  "extra_body": {
    "image": ["https://example.com/input-image.png"],
    "response_format": "url"
  }
}
```

**Multi-image composition (agnes-image-2.0-flash):**

```json
{
  "model": "agnes-image-2.0-flash",
  "tags": ["img2img"],
  "prompt": "Combine the two characters into an intense fantasy battle scene, dynamic lighting, detailed background, cinematic composition",
  "size": "1024x768",
  "extra_body": {
    "image": [
      "https://example.com/character-1.png",
      "https://example.com/character-2.png"
    ],
    "response_format": "url"
  }
}
```

**Response:**

```json
{
  "created": 1774432125,
  "data": [
    {
      "url": "https://cdn.agnes-ai.com/output/abc123.png"
    }
  ],
  "usage": {
    "generated_images": 1
  }
}
```

---

### Video Generation (Create)

```
POST /v1/video/generations
```

**Request Body:**

```json
{
  "model": "agnes-video-v2.0",
  "prompt": "A drone flying over a city skyline",
  "duration": 5
}
```

**Response:**

```json
{
  "id": "task_abc123",
  "status": "processing"
}
```

---

### Video Generation (Poll)

```
GET /v1/video/generations/{task_id}
```

**Response (completed):**

```json
{
  "id": "task_abc123",
  "status": "completed",
  "url": "https://cdn.agnes-ai.com/output/abc123.mp4"
}
```

**Response (processing):**

```json
{
  "id": "task_abc123",
  "status": "processing"
}
```

**Response (failed):**

```json
{
  "id": "task_abc123",
  "status": "failed",
  "error": "Generation failed: content policy violation"
}
```

---

## Supported Image Sizes

| Size        | Orientation |
| ----------- | ----------- |
| `1024x1024` | Square (default) |
| `1792x1024` | Landscape |
| `1024x1792` | Portrait |
| `1024x768`  | Wide (custom) |
| `768x1024`  | Tall (custom) |

## Recommended Prompt Structure

```
[Subject] + [Scene / Environment] + [Style] + [Lighting] + [Composition] + [Quality Requirements]
```

### Text-to-Image Example

```
A futuristic city marketplace filled with flying vehicles, holographic signs, dense crowds, neon lighting, cinematic realism, ultra-detailed, high-information-density composition
```

### Image-to-Image Example

```
Transform the scene into a rain-soaked cyberpunk night with neon reflections while preserving the original composition and main subject layout.
```

### Multi-Image Composition Example

```
Place the person from the first image beside the robot from the second image in a cinematic sci-fi battle scene
```
