---
name: apiko-media
description: Generate or edit images and generate videos through the APIKO API (Nano Banana, GPT Image, Seedream, Wan 3.0, Seedance). Use when the user asks to create an image, edit or combine photos, make a video from text, an image or reference clips, or call APIKO image/video models from code. Handles async submit, polling, local reference uploads, cost checks and saving the result.
metadata:
  author: APIKO
  version: "1.0"
  openclaw:
    requires:
      env:
        - APIKO_API_KEY
      bins:
        - python3
    primaryEnv: APIKO_API_KEY
    envVars:
      - name: APIKO_BASE_URL
        required: false
        description: Override the API host. Defaults to https://api.apiko.app and must be HTTPS.
---

# APIKO image and video generation

Create images and videos with models served by APIKO (https://apiko.app/) through one API key. Jobs run asynchronously: they take from about 20 seconds to over 10 minutes, so this skill submits the job, polls it, and saves the file. The bundled script `scripts/apiko_media.py` does all of that with the Python standard library only.

## Step 1: Understand the request

1. **Pick the job type**: text to image, image edit (one or more reference photos), text or image to video, or video from reference images and clips.
2. **Use the user's own words as the prompt.** Do not rewrite or summarize their description. If something important is missing (subject, style, aspect ratio, text to render, length of the video), ask first, then append the answer to their original prompt.
3. **Pick the model** from the table below, or let the user choose. Model details, fields and billing rules are in [references/models.md](references/models.md).

| Need | Model id |
|---|---|
| Edit or combine photos | `nano-banana-2.1` (default), `nano-banana-pro` |
| Text to image, posters, text rendering | `gpt-image-2.5-sunburst` (default), `gpt-image-2.5-flare`, `gpt-image-2` |
| Text or image to video | `wan3.0-text-to-video`, `wan3.0-image-to-video`, `seedance-2.5`, `seedance-2.0-fast` |
| Video from reference images and clips | `wan3.0-reference-video`, `wan3.0-prime-reference-video` |

4. **Work out the parameters**: resolution tier for images (`1k`/`2k`/`4k` on Nano Banana, `size` ratio on GPT Image), and for videos `duration` (seconds), `resolution` (`480p`/`720p`/`1080p`) and `aspect_ratio`.

## Step 2: Check cost, then run

1. **Check the key**: the script reads `APIKO_API_KEY` from the environment. If it is not set, ask the user to create a key at https://apiko.app/ and `export APIKO_API_KEY=...` themselves. Never ask them to paste the key into the chat, and never print it or write it into a file.
2. **Check the price** on the model page (https://apiko.app/models/<model-id>). Images are priced per image by tier; videos per second of output by resolution. For anything above a few cents (4K images, 1080p or long videos, Wan reference clips), tell the user the estimate and wait for a yes.
3. **Tell the user how long to wait** before starting: about 1 minute for a 1K/2K image, up to 5 minutes for 4K, and 2–15 minutes for a video depending on resolution and length.
4. **Run the script** (path relative to this skill's folder):

```bash
# Text to image
python3 scripts/apiko_media.py image --model gpt-image-2.5-sunburst \
  --prompt "<user prompt>" --size 16:9 -o poster.png

# Edit or combine photos (local files are uploaded automatically; https URLs are passed through)
python3 scripts/apiko_media.py image --model nano-banana-2.1 \
  --prompt "<user prompt>" --image ./product.jpg --resolution 2k -o product-studio.png

# Video from a reference image and a reference clip
python3 scripts/apiko_media.py video --model wan3.0-reference-video \
  --prompt "Image 1 walks along the beach in the style of Video 1" \
  --ref-image ./character.png --ref-video https://example.com/style-3s.mp4 \
  --duration 5 --resolution 720p --aspect-ratio adaptive -o beach.mp4
```

Progress goes to stderr. On success the script prints one JSON line with `task_id`, `file` and `url`.

If the script is not available, use plain HTTP: `POST https://api.apiko.app/v1/images/generations`, `/v1/images/edits` or `/v1/videos` with `"async": true` for images, then poll `GET https://api.apiko.app/v1/tasks/{id}` every 5–10 seconds until `status` is `completed` or `failed`, and download `data[0].url`. Send the header `Authorization: Bearer $APIKO_API_KEY`.

## Step 3: Report the result

- **Success**: give the user the saved file path. Result links expire after 24 hours, so the saved file is what they keep.
- **Still running when the script times out**: do not submit again (that bills a second time). Resume with `python3 scripts/apiko_media.py status <task_id> -o <file>`.
- **Task failed**: failed tasks are refunded in full. Show the `fail_reason`. Unreachable reference URLs and content refusals are the usual causes; fix the input before retrying.
- **Errors before submission**:
  - `HTTP 400`: a field is invalid (prompt too long, unsupported size, too many seconds of reference video). Nothing was billed; fix the request.
  - `HTTP 401` / invalid key: the key is wrong or deleted. Ask the user to check it in the APIKO console.
  - `HTTP 503` with `model_not_found`: the model id is wrong. Check https://apiko.app/models for the exact id.
  - Anything else: show the error message; it ends with a request id that APIKO support can look up.

## Rules

- Keep the key in the environment. Do not echo it, log request headers, or commit it.
- Reference images must be public HTTPS URLs or local JPEG/PNG/WebP files up to 10 MB (the script uploads local files; uploads are free and kept for 72 hours). Reference videos must be public HTTPS URLs.
- Uploaded references and result links are reachable by anyone who has the URL. Do not upload private or sensitive images without the user's consent.
- One submission per job. Polling is free; resubmitting is not.

## More

- Fields, limits and billing per model: [references/models.md](references/models.md)
- Full API reference: https://apiko.app/docs
- Prefer tool calls over a script? The APIKO MCP server (`npx -y apiko-mcp`, https://apiko.app/mcp) offers the same pricing, generation and task tracking as tools.
