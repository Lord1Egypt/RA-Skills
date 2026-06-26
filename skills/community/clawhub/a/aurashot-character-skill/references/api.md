# AuraShot Character Design API Reference

Base URL: `https://www.aurashot.art`

## Authentication

All endpoints require a Bearer token in the `Authorization` header:

```
Authorization: Bearer sk_live_YOUR_KEY
```

Get your API key at: https://www.aurashot.art/studio?tab=keys

## Environment Variables

- `AURASHOT_API_KEY`: preferred AuraShot API key
- `AURASHOT_STUDIO_KEY`: fallback key
- `AURASHOT_BASE_URL`: defaults to `https://www.aurashot.art`

## Endpoints

### POST /v1/uploads

Upload a local image and get a public URL for use in other endpoints.

**Content-Type:** `multipart/form-data`

| Field  | Required | Description          |
|--------|----------|----------------------|
| `file` | Yes      | Image file to upload |

**Response:**
```json
{ "url": "https://..." }
```

---

### POST /v1/character/id-photo

Generate a 4-in-1 character ID photo (front, left profile, right profile, white-background ID).

**Request Body:**
```json
{
  "images": {
    "face": "https://example.com/face.jpg"
  },
  "prompt": "Optional custom prompt for ID photo generation"
}
```

| Field         | Required | Description                                                                 |
|---------------|----------|-----------------------------------------------------------------------------|
| `images.face` | Yes      | Face photo URL (HTTPS)                                                      |
| `prompt`      | No       | Custom generation prompt. Defaults to standard real-person ID photo prompt. |

**Response:**
```json
{
  "requestId": "uuid",
  "jobId": "uuid",
  "taskType": "id-photo",
  "status": "success",
  "outputs": [{ "url": "https://..." }],
  "pipeline": { "provider": "qwen-image-edit", "status": "success" },
  "tokenUsage": { "inputTokens": 0, "outputTokens": 1234 },
  "createdAt": "2026-03-16T..."
}
```

---

### POST /v1/character/generate

Reference-driven character image generation. Upload a face photo and optionally clothes/scene references.

**Request Body:**
```json
{
  "prompt": "穿着白色连衣裙站在樱花树下",
  "images": {
    "face": "https://example.com/face.jpg",
    "clothes": "https://example.com/dress.jpg",
    "scene": "https://example.com/park.jpg"
  }
}
```

| Field            | Required | Description                          |
|------------------|----------|--------------------------------------|
| `prompt`         | Yes      | Natural language description         |
| `images.face`    | Yes      | Face reference photo URL             |
| `images.clothes` | No       | Clothing reference image URL         |
| `images.scene`   | No       | Scene/background reference image URL |

**Response:** Same shape as id-photo, with `taskType: "generate"`.

---

### POST /v1/character/edit

Edit an existing image using natural language. Optionally pass a face reference to maintain identity.

**Request Body:**
```json
{
  "prompt": "换个站姿，背景改成咖啡馆",
  "images": {
    "target": "https://example.com/current-photo.jpg",
    "face": "https://example.com/id-photo.jpg"
  }
}
```

| Field           | Required | Description                                    |
|-----------------|----------|------------------------------------------------|
| `prompt`        | Yes      | Natural language edit description              |
| `images.target` | Yes      | Image to edit URL                              |
| `images.face`   | No       | Face reference (ID photo) for identity lock    |

**Response:** Same shape as id-photo, with `taskType: "edit"`.

---

## Response Fields

| Field              | Description                                              |
|--------------------|----------------------------------------------------------|
| `requestId`        | Unique request identifier                                |
| `jobId`            | Job identifier                                           |
| `taskType`         | `id-photo`, `generate`, or `edit`                        |
| `status`           | `success` or `failed`                                    |
| `outputs`          | Array of `{ url }` objects with generated image URLs     |
| `pipeline.status`  | Generation pipeline status (provider: qwen-image-edit)   |
| `tokenUsage`       | Token consumption stats                                  |
| `createdAt`        | ISO 8601 timestamp                                       |

## Image Input Rules

- All image URLs must be publicly accessible HTTPS URLs
- SSRF protection: private IPs, non-standard ports, and localhost are rejected
- Supported formats: JPEG, PNG, WebP, GIF
- Local files: upload via `/v1/uploads` first (Agent Skill handles this automatically)

## Legacy Endpoints

The following endpoints are from the previous e-commerce photography version and are kept for backward compatibility:

- `POST /api/aesthetic/generate` — Virtual Try-On / Pose Change (legacy)
- `POST /api/aesthetic/query` — Poll job status (legacy)

New integrations should use the `/v1/character/*` endpoints above.
