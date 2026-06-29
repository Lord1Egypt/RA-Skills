---
name: autoglm-file-upload
description: >
  Use the AutoGLM Upload Mix API to upload local files such as images and documents, then obtain a file URL
  or resource ID for downstream API calls.
  The token is fetched automatically from the local service at http://127.0.0.1:18432/get_token, so no
  manual environment variable setup is required.
compatibility:
  requires:
    - Python 3, hashlib, mimetypes, uuid (all built in)
---

# AutoGLM File Upload Skill

Upload a local file to the AutoGLM server and return file resource information that can be used by other APIs.

---

## Token Retrieval

When the script starts, it automatically sends an HTTP GET request to the local service to retrieve a token:

| Item | Value |
|------|------|
| URL | `http://127.0.0.1:18432/get_token` |
| Method | GET |
| Response | `Bearer xxx` (used directly as the `Authorization` header) |

> If the returned token does not include the `Bearer` prefix, the script adds it automatically.

---

## Upload Mix API

| Item | Value |
|------|------|
| URL | `https://autoglm-api.autoglm.ai/agentdr/v1/assistant/upload-mix` |
| Method | POST |
| Request body | `multipart/form-data`, with the field name `files` |

**Signed headers (generated dynamically for each request):**

- `X-Auth-Appid`: `100003`
- `X-Auth-TimeStamp`: current Unix timestamp in seconds
- `X-Auth-Sign`: MD5(`100003 + "&" + timestamp + "&" + 38d2391985e2369a5fb8227d8e6cd5e5`)

---

## Run the Script

Use `upload-mix.py` in the same directory:

```bash
python upload-mix.py "<local file path>"
```

**Examples:**

```bash
# Upload an image
python upload-mix.py "/path/to/image.jpg"

# Upload a document
python upload-mix.py "/path/to/document.pdf"
```

The script automatically detects the file's MIME type and includes it in the request.

---

## Response Handling

### Response Structure

```json
{
  "code": 0,
  "msg": "SUCCESS",
  "time": 1773199477734,
  "trace": "78dd001f3ec04c37b6a1d58b5db70fce",
  "data": {
    "message": "",
    "oss_info": [
      {
        "filename": "SKILL.md",
        "oss_name": "auto_fly/8a4e6ab6-c2ab-4e88-b4af-fb62db9379af/SKILL.md",
        "oss_url": "https://autoglm-agent.aminer.cn/auto_fly/8a4e6ab6-c2ab-4e88-b4af-fb62db9379af/SKILL.md"
      }
    ]
  }
}
```

### Output Requirements

**1. Extract the file URL**
Use `data.oss_info[0].oss_url` as the uploaded file URL. It can be passed directly to downstream APIs such as the `image_url` parameter in `image-recognition`.

**2. Typical follow-up flow**
```
upload_mix (upload a local file) -> get the URL -> image_recognition (analyze the image)
```
