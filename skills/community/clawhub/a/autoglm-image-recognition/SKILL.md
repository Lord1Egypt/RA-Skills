---
name: autoglm-image-recognition
description: >
  Use the AutoGLM Image Recognition API to analyze and describe image content. Use this skill when the
  user needs image analysis, object or scene recognition, OCR-like text extraction, or a general image
  description.
  The token is fetched automatically from the local service at http://127.0.0.1:18432/get_token, so no
  manual environment variable setup is required.
  If the user provides a local image file, you must first run upload-mix.py to upload it and obtain a
  public URL before using this skill.
compatibility:
  requires:
    - Python 3, hashlib (built in)
---

# AutoGLM Image Recognition Skill

Use the AutoGLM Image Recognition API to analyze and describe an image.

---

## Prerequisite: Get a Public Image URL

This skill requires `image_url` to be a **publicly accessible URL**. Choose the correct path based on the source of the image:

| Image source | What to do |
|----------|----------|
| Existing public URL (`http://` or `https://`) | Use it directly with no extra processing |
| Local file (user upload or local path) | You must run `upload-mix.py` first, then pass the returned public URL |

> **Important:** If the user provides a local image, such as an uploaded file or a local disk path, do not pass the file path directly.
> Run **`upload-mix.py`** first to upload the file, obtain a public URL, and only then perform image recognition.

---

## Step 1 for a Local Image: Upload with `upload-mix.py`

If the image is a local file, upload it first:

```bash
python upload-mix.py "<local image path>"
```

**Example:**

```bash
python upload-mix.py "/home/user/photo.jpg"
```

**Response structure:**

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
        "filename": "photo.jpg",
        "oss_name": "auto_fly/xxx/photo.jpg",
        "oss_url": "https://autoglm-agent.aminer.cn/auto_fly/xxx/photo.jpg"
      }
    ]
  }
}
```

Extract `data.oss_info[0].oss_url` from the response. That value is the `image_url` needed for the recognition step.

---

## Step 2: Image Recognition API

| Item | Value |
|------|------|
| URL | `https://autoglm-api.autoglm.ai/agentdr/v1/assistant/skills/image-recognition` |
| Method | POST |
| Request body | See below |

**Request body:**

```json
{
  "prompt": "Describe the image",
  "image_url": "https://example.com/image.jpg"
}
```

| Field | Description | Required |
|------|------|--------|
| `image_url` | A **publicly accessible URL** for the image. For local images, upload first with `upload-mix.py` and use `data.oss_info[0].oss_url` | Yes |
| `prompt` | An instruction such as "Describe the image" or "Extract the text shown in the image" | Optional, default is `"Describe the image"` |

**Signed headers (generated dynamically for each request):**

- `X-Auth-Appid`: `100003`
- `X-Auth-TimeStamp`: current Unix timestamp in seconds
- `X-Auth-Sign`: MD5(`100003 + "&" + timestamp + "&" + 38d2391985e2369a5fb8227d8e6cd5e5`)

---

## Run the Script

Use `image-recognition.py` in the same directory:

```bash
# Pass only the image URL and use the default prompt
python image-recognition.py "https://example.com/image.jpg"

# Pass the image URL with a custom prompt
python image-recognition.py "https://example.com/image.jpg" "Extract the text shown in the image"
```

> **Note:** Image recognition may take longer than other calls. Wait for the response.
> If you need a timeout, change the request call in `image-recognition.py` to:
> ```python
> with urllib.request.urlopen(req, timeout=300) as resp:
> ```
> A timeout of **300 seconds** is recommended.

---

## Full Workflow

```
User provides a local image
       ↓
Run upload-mix.py to upload the image
  python upload-mix.py "<local image path>"
       ↓
Extract data.oss_info[0].oss_url as image_url
       ↓
Run image-recognition.py
  python image-recognition.py "<image_url>" ["<prompt>"]
       ↓
Present data.text to the user
```

**If the user already provides a public URL, skip the upload step:**

```
User provides a public image URL
       ↓
Run image-recognition.py
  python image-recognition.py "<image_url>" ["<prompt>"]
       ↓
Present data.text to the user
```

---

## Response Handling

### Response Structure

```json
{
  "code": 0,
  "msg": "SUCCESS",
  "time": 1773137796961,
  "trace": "298d5fe1efdd4da58ca46d1700d8054b",
  "data": {
    "text": "Detailed image recognition result...",
    "tokens": 5588
  }
}
```

### Output Requirements

**1. Present the recognition result directly**
Return the contents of `data.text` directly to the user and preserve the original formatting, including any Markdown emphasis.
