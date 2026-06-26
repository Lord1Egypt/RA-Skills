# Animate Old Photos — API Reference

Base URL: `https://animateoldphotos.org`

All endpoints (except authentication) require a Bearer token obtained from the auth endpoint.

---

## Authentication

### POST /api/extension/auth

Exchange an API key (license key) for a short-lived access token.

**Request**

```
POST /api/extension/auth
Content-Type: application/json

{
  "licenseKey": "your-api-key"
}
```

**Response (success)**

```json
{
  "accessToken": "eyJhbGciOi...",
  "expiresIn": 43200,
  "creditBalance": 42,
  "userId": "user_abc123",
  "keyId": "key_xyz789"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `accessToken` | string | JWT Bearer token for subsequent requests |
| `expiresIn` | number | Token lifetime in seconds (~12 hours) |
| `creditBalance` | number | Current credit balance |
| `userId` | string | User identifier |
| `keyId` | string | API key identifier |

**Errors**

| error_code | error_msg | Meaning |
|------------|-----------|---------|
| `4010` | Invalid license key | The API key does not exist |
| `4011` | License key expired | The API key has expired |

---

## Upload — Get Token

### POST /api/extension/upload-token

Get a presigned URL for uploading an image to cloud storage (Cloudflare R2).

**Request**

```
POST /api/extension/upload-token
Authorization: Bearer <accessToken>
Content-Type: application/json

{
  "fileName": "photo.jpg",
  "contentType": "image/jpeg",
  "fileSize": 2048576
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `fileName` | string | yes | Original file name |
| `contentType` | string | yes | MIME type: `image/jpeg` or `image/png` |
| `fileSize` | number | yes | File size in bytes |

**Response (success)**

```json
{
  "uploadUrl": "https://....r2.cloudflarestorage.com/...?X-Amz-Signature=...",
  "key": "uploads/abc123/photo.jpg",
  "publicUrl": "https://pub-xxx.r2.dev/uploads/abc123/photo.jpg",
  "expiresIn": 3600
}
```

| Field | Type | Description |
|-------|------|-------------|
| `uploadUrl` | string | Presigned PUT URL (expires in `expiresIn` seconds) |
| `key` | string | Storage key for the uploaded file |
| `publicUrl` | string | Public URL of the file after upload |
| `expiresIn` | number | Seconds until the presigned URL expires |

---

## Upload — PUT to R2

### PUT \<uploadUrl\>

Upload the image binary to the presigned URL returned by the previous step.

**Request**

```
PUT <uploadUrl>
Content-Type: image/jpeg

<binary image data>
```

No Authorization header is needed — the presigned URL contains embedded credentials.

**Response**: HTTP 200 on success, no body.

---

## Upload — Finalize

### POST /api/extension/upload-finalize

Confirm the upload completed. The server validates the object, prepares it for the AI pipeline, and returns an encrypted payload required for task submission.

**Request**

```
POST /api/extension/upload-finalize
Authorization: Bearer <accessToken>
Content-Type: multipart/form-data

key=uploads/abc123/photo.jpg
publicUrl=https://pub-xxx.r2.dev/uploads/abc123/photo.jpg
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `key` | string | yes | Storage key from upload-token response |
| `publicUrl` | string | yes | Public URL from upload-token response |

**Response (success)**

```json
{
  "url": "https://...",
  "message": "encrypted-payload-string",
  "dnt": "source-identifier"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `url` | string | Image URL to use for the animation task |
| `message` | string | Encrypted payload — pass as the `Ss` header in the animate request |
| `dnt` | string | Source routing identifier — pass through to animate request |

**Important**: The `message` value is a server-side encrypted signature. It cannot be fabricated. You must complete the full upload flow to obtain it.

---

## Animate — Submit Task

### POST /api/extension/animate

Submit a photo-to-video animation task. Costs **3 credits**.

**Request**

```
POST /api/extension/animate
Authorization: Bearer <accessToken>
Ss: <message from finalize>
Content-Type: multipart/form-data

prompt=grandmother smiling and waving
input_image_url=https://...
dnt=source-identifier
type=m2v_img2video
duration=5
public=false
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `prompt` | string | no | Motion description. If empty, AI auto-generates motion. |
| `input_image_url` | string | yes | Image URL from the finalize response |
| `dnt` | string | yes | Source identifier from the finalize response |
| `type` | string | yes | Must be `m2v_img2video` |
| `duration` | string | yes | Video duration in seconds. Use `"5"`. |
| `public` | string | no | `"false"` to keep the result private |

**Headers**

| Header | Required | Description |
|--------|----------|-------------|
| `Authorization` | yes | `Bearer <accessToken>` |
| `Ss` | yes | The `message` value from the finalize response |

**Response (success)**

```json
{
  "taskId": "encrypted-task-id",
  "dnt": "source-identifier",
  "did": "device-identifier"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `taskId` | string | Task identifier for polling |
| `dnt` | string | Source identifier (may differ from input) |
| `did` | string | Device identifier for polling |

**Errors**

| error_code | Meaning |
|------------|---------|
| `999990` | Insufficient credits |
| `10009` | Insufficient credits |
| `999998` | Access token invalid/expired |

---

## Animate — Poll Status

### GET /api/extension/animate

Poll the status of a submitted animation task.

**Request**

```
GET /api/extension/animate?taskId=<taskId>&dnt=<dnt>&did=<did>&type=m2v_img2video
Authorization: Bearer <accessToken>
```

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `taskId` | string | yes | From the submit response |
| `dnt` | string | yes | From the submit response |
| `did` | string | yes | From the submit response |
| `type` | string | yes | Must be `m2v_img2video` |

**Response (in progress)**

```json
{
  "status": 50
}
```

**Response (completed)**

```json
{
  "status": 99,
  "resource": "https://pub-xxx.r2.dev/videos/abc123/output.mp4"
}
```

**Response (failed)**

```json
{
  "message": "Task failed: content policy violation"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `status` | number | Progress indicator. `>= 99` means done. |
| `resource` | string | Video URL. Present only when `status >= 99`. |
| `message` | string | Error message. Present only on failure. |

**Polling strategy**: Poll every **30 seconds**. Typical task completes in 2–5 minutes. Set a maximum timeout of 10 minutes.

---

## Error Codes — Complete Table

| error_code | Meaning | Resolution |
|------------|---------|------------|
| `4010` | Invalid license key | Get a valid key at [Profile > API Key](https://animateoldphotos.org/profile/interface-key) |
| `4011` | License key expired | Renew at [Profile > API Key](https://animateoldphotos.org/profile/interface-key) |
| `999998` | Access token invalid | Re-authenticate by calling POST /api/extension/auth |
| `999990` | Insufficient credits | Purchase credits at [Buy Credits](https://animateoldphotos.org/stripe) |
| `10009` | Insufficient credits | Purchase credits at [Buy Credits](https://animateoldphotos.org/stripe) |

Network errors (timeouts, DNS failures) should be retried up to 3 times with exponential backoff (2s → 4s → 8s).

---

## Image Constraints

| Constraint | Value |
|------------|-------|
| Supported formats | JPEG (`image/jpeg`), PNG (`image/png`) |
| Maximum file size | 10 MB (10,485,760 bytes) |
| Minimum dimensions | 300 × 300 px |

---

## Token Lifecycle

- Tokens are valid for approximately **12 hours** (`expiresIn: 43200` seconds).
- To refresh, call `POST /api/extension/auth` again with the same API key.
- Recommended: refresh if the token will expire within the next **60 seconds**.
- If a request returns `error_code: 999998`, the token has expired — re-authenticate and retry.

---

## Links

- Official Website: <https://animateoldphotos.org/>
- Get API Key: <https://animateoldphotos.org/profile/interface-key>
- Buy Credits: <https://animateoldphotos.org/stripe>
- View Pricing Plans: <https://animateoldphotos.org/stripe>
