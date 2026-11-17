---
name: DaDaScribe advanced speech-to-text transcription and translations
description: Transcribe audio and video with the DaDaScribe AI service (YouTube URLs, direct links, or local files). Supports 100+ languages, speaker diarization with named speakers, translation to up to 5 languages, and returns .txt transcripts plus .srt subtitles. Use whenever the user asks to transcribe, caption, subtitle, or translate speech from YouTube, podcasts, meetings, interviews, videos, or audio/video files via DaDaScribe or the dadascribe API.
---

# DaDaScribe API Skill

Use the official DaDaScribe API (`https://api.dadascribe.com/v1`) for high-quality AI transcription.

**Base URL:** `https://api.dadascribe.com/v1`  
**API version:** 1.0.1  
**Official docs:** https://api.dadascribe.com/docs  
**OpenAPI:** https://api.dadascribe.com/openapi.json  
**Get API key:** https://www.dadascribe.com/account/api.php (keys start with `dds_`)

The official Python wrapper lives in this same repository (`dadascribe` package). Prefer the HTTP API below when the package is not installed; it works with any language that can make HTTP requests.

## Authentication

Every authenticated request requires:

```
Authorization: Bearer dds_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

Never hard-code the key. Load it from the environment variable `DADASCRIBE_API_KEY` (or ask the user for it). Output file download URLs do **not** require authentication.

## Core Workflow

1. Submit one or more sources → receive a batch `id`.
2. Poll `/status` until `status` is `"complete"` (or `"error"`).
3. Download the `.txt` / `.srt` files from the `urls` array **within 1 hour** (they expire for privacy).

### 1. Submit transcription – `POST /transcribe`

**JSON body** (preferred for URLs):

```json
{
  "source": "https://www.youtube.com/watch?v=VIDEO_ID",
  "source-language": "en",
  "destination-language": "es,it,fr",
  "diarization": "Host,Guest"
}
```

- `source` (required for JSON unless `s3_token` is used): single string **or** array of up to **10** items.  
  Accepted values: full YouTube URL, Shorts, `youtu.be`, 11-char video ID, or a direct HTTPS audio/video URL.
- `s3_token` (optional): token from `/v1/upload/complete` instead of `source` / `file`.
- Direct file URLs and uploads allow audio and video (max **10 GB**; PHP multipart `file` is still capped near 480M — use `/v1/upload/*` for larger files).
- `source-language` (required): ISO-style code (`en`, `es`, `fr`, `zh`, `ja`, …). 100+ supported.
- `destination-language` (optional): comma-separated list, **max 5**, must **not** include the source language.
- `diarization` (optional): comma-separated speaker names, **minimum 2**.

**Multipart** (for a single local file upload):

```
file=@/path/to/audio.mp3
data={"source-language":"en","destination-language":"es"};type=application/json
```

or individual form fields.

**Success response:**

```json
{
  "status": "ok",
  "id": "a1B2c3D4e5F6g7H8",
  "count": 1
}
```

**Limits:**
- Max 10 sources per request
- Max 10 hours per source
- Duplicates are automatically removed
- Rate limit: 60 requests/minute per API key

### 2. Poll status – `POST /status`

```json
{
  "id": "a1B2c3D4e5F6g7H8"
}
```

Possible responses:

| status       | meaning                          | extra fields                                      |
|--------------|----------------------------------|---------------------------------------------------|
| `queue`      | waiting in queue                 | `count`                                           |
| `processing` | actively transcribing            | `count`, `complete`, `queue`, `processing`        |
| `complete`   | ready                            | `count`, `urls` (array of download links)         |
| `error`      | failed                           | `message`                                         |

Rate limit: 120 requests/minute. Poll every 5–15 seconds.

### 3. Download results – `GET /output/{id}/{filename}`

No auth header needed. Example URLs returned in a complete response:

```
https://api.dadascribe.com/v1/output/a1B2c3D4e5F6g7H8/xxxx.txt
https://api.dadascribe.com/v1/output/a1B2c3D4e5F6g7H8/xxxx.srt
https://api.dadascribe.com/v1/output/a1B2c3D4e5F6g7H8/xxxx_es.srt
```

- `.txt` = plain transcript  
- `.srt` = timed subtitles  
- `_{lang}.srt` = translated subtitles  

Files disappear after **1 hour**. Rate limit: 600/min per IP.

## Python reference implementation (requests)

```python
import os
import time
import requests

API_KEY = os.environ["DADASCRIBE_API_KEY"]
BASE = "https://api.dadascribe.com/v1"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}

def transcribe(source, source_language="en", destination_language=None, diarization=None):
    payload = {"source": source, "source-language": source_language}
    if destination_language:
        payload["destination-language"] = destination_language
    if diarization:
        payload["diarization"] = diarization

    r = requests.post(f"{BASE}/transcribe", json=payload, headers=HEADERS, timeout=30)
    r.raise_for_status()
    data = r.json()
    if data.get("status") != "ok":
        raise RuntimeError(data)
    return data["id"]

def wait_until_complete(job_id, poll_interval=8):
    while True:
        r = requests.post(f"{BASE}/status", json={"id": job_id}, headers=HEADERS, timeout=15)
        r.raise_for_status()
        data = r.json()
        status = data.get("status")
        if status == "complete":
            return data["urls"]
        if status == "error":
            raise RuntimeError(data.get("message", "unknown error"))
        time.sleep(poll_interval)

def download(urls, out_dir="."):
    paths = []
    for url in urls:
        name = url.rsplit("/", 1)[-1]
        path = os.path.join(out_dir, name)
        with requests.get(url, stream=True, timeout=60) as r:
            r.raise_for_status()
            with open(path, "wb") as f:
                for chunk in r.iter_content(8192):
                    f.write(chunk)
        paths.append(path)
    return paths

# Example usage
job_id = transcribe(
    source="https://www.youtube.com/watch?v=dQw4w9wgccc",
    source_language="en",
    destination_language="es,it",
    diarization="Host,Guest",
)
urls = wait_until_complete(job_id)
files = download(urls)
print("Downloaded:", files)
```

## Using the official Python package (optional)

```bash
pip install -e .          # from this repo
# or
pip install git+https://github.com/PatzEdi/dadascribe-api-python.git
```

```python
from dadascribe import ScribeAPIWrapper
import os

w = ScribeAPIWrapper(os.environ["DADASCRIBE_API_KEY"])
result = w.transcribe(
    source="https://www.youtube.com/watch?v=...",
    source_language="en",
    destination_language="es,it",
)
```

CLI (after install):

```bash
dadascribe --source "https://youtube.com/watch?v=..."
dadascribe --status <job_id>
dadascribe --download <job_id>
```

## Error handling

| HTTP | Typical message              | Action                                      |
|------|------------------------------|---------------------------------------------|
| 400  | missing source / invalid …   | Fix request parameters                     |
| 401  | unauthorized                 | Check API key                               |
| 402  | no time left                 | User must top up account balance            |
| 429  | rate limit exceeded          | Back off using `X-RateLimit-Reset` header   |
| 403  | (on output)                  | File not ready or already expired           |

Always surface the `message` field from error JSON to the user.

## Best practices for agents

- Confirm the user has a valid API key and account balance before starting large jobs.
- Prefer YouTube / direct URLs over uploading large local files when possible.
- Respect rate limits; never spin in a tight poll loop.
- Download results immediately after `complete`.
- When returning results to the user, prefer the plain `.txt` for readability and the `.srt` for subtitles.
- For multi-language requests, list the generated `_{lang}.srt` files clearly.
- Never store or log the full API key.

This skill gives any agent complete, production-ready access to the DaDaScribe transcription service.
```