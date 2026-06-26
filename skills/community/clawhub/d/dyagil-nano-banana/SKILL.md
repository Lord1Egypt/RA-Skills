---
name: dyagil-nano-banana
description: Generate or edit images using Google's "Nano Banana" image models (Gemini 2.5 / 3.x image previews). Use this when the user explicitly asks for Gemini / Nano Banana / Nano Banana Pro, wants iterative image edits with reference inputs, or wants a different (often cheaper) image stack than the built-in image generation tool.
version: 1.0.0
license: MIT
author: dyagil
---

# Nano Banana — Gemini Image Generation

A CLI skill for generating and editing images using Google's Gemini image models, marketed as "Nano Banana" and "Nano Banana Pro".

## When to Use

Use this skill when the user explicitly asks for:
- "Nano Banana" / "Nano Banana Pro"
- "Generate the image with Gemini"
- Image edits / composition using one or more **reference images**
- Iterative edits in conversation ("now make her smile", "swap the background")

For generic "make me an image" requests with no provider hint, prefer your platform's built-in image generation unless the user has set Nano Banana as the default.

## Model Map (Nano Banana names → Gemini model IDs)

| Nickname | Model ID | Notes |
|---|---|---|
| **Nano Banana Pro** ← default | `gemini-3-pro-image-preview` | Highest quality, slower, multi-image edits |
| Nano Banana 3.1 Flash | `gemini-3.1-flash-image-preview` | Faster, newer, good for iteration |
| Nano Banana (classic) | `gemini-2.5-flash-image` | Original, cheapest, still solid |

If unspecified, **default to Pro**.

## Auth

Store the Gemini API key at `~/.openclaw/credentials/google/gemini_api_key` (`chmod 600`).

Load it before invoking the CLI:
```bash
export GEMINI_API_KEY=$(cat ~/.openclaw/credentials/google/gemini_api_key)
```

⚠️ Never log or echo the key. Never paste it into chat. If rotated, replace the file contents.

Get a key at: https://aistudio.google.com/apikey

## CLI

Binary: `~/bin/nano-banana` (Node.js). Source lives at `<your-tools-dir>/nano-banana.js`.

### Generate from prompt

```bash
~/bin/nano-banana "a person eating a red apple, photorealistic, warm light"
# Writes: ~/.../nano-banana-output/YYYY-MM-DD_HHMMSS.png
# Prints the absolute path on success.
```

### Choose model / aspect / count

```bash
~/bin/nano-banana --model pro "logo for a modern insurance agency, olive green"
~/bin/nano-banana --model flash --aspect 16:9 "morning marathon in a coastal city"
~/bin/nano-banana --model classic --count 4 "red pepper on a wooden table"
~/bin/nano-banana --aspect 1:1 --out /tmp/x.png "..."
```

Flags:
- `--model pro|flash|classic|<full-id>` (default: `pro`)
- `--aspect 1:1|4:3|3:4|16:9|9:16|3:2|2:3` (best-effort prompt hint)
- `--count N` (1–4, default 1)
- `--out <path>` (only valid with `--count 1`)
- `--out-dir <path>` (default: `<tools-dir>/nano-banana-output/`)
- `--quiet` (print only resulting paths, one per line)

### Edit with reference images

```bash
~/bin/nano-banana --ref photo.jpg "put a red baseball cap on the person"
~/bin/nano-banana --ref a.png --ref b.png "merge the two images, library background"
```

## How Your Agent Should Use This

1. **Read the request and pick a model.** "Pro" → `pro`. "Fast" / "Flash" → `flash`. Otherwise → `pro`.
2. **Write the prompt in English.** Gemini image models work best in English even when the chat is in another language. Translate any non-English description into a clear, descriptive English prompt.
3. **Run the CLI** via `exec`. Capture the output path.
4. **Deliver the image** by adding `MEDIA:<path>` on its own line in the reply (or use your platform's attachment convention).
5. **Reply** with a short caption + which model was used.

### Example agent flow

User: "Draw a person eating a red apple."

```bash
~/bin/nano-banana --aspect 4:3 \
  "A realistic portrait of a person taking a bite from a bright red apple, natural daylight, soft shadows, sharp focus, casual modern clothing, slight motion blur on the hand, warm color grading"
# → /home/<user>/.../nano-banana-output/2026-05-11_141815.png
```

Reply:
> Here's the apple shot — Nano Banana Pro
> MEDIA:/home/<user>/.../nano-banana-output/2026-05-11_141815.png

## API Contract (what the CLI does)

Under the hood, the CLI POSTs to:

```
POST https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={KEY}
```

Body:
```json
{
  "contents": [{"role": "user", "parts": [{"text": "<prompt>"}]}],
  "generationConfig": {
    "responseModalities": ["IMAGE", "TEXT"],
    "candidateCount": <N>
  }
}
```

Response candidates contain `parts[].inlineData.{mimeType, data}` (base64). The CLI decodes and writes to disk.

For reference images, additional `parts` with `inlineData` are prepended before the text prompt.

## Errors & Gotchas

- **`PERMISSION_DENIED` / `API_KEY_INVALID`** → key rotated. Update the credentials file.
- **`RESOURCE_EXHAUSTED`** → free-tier quota hit. Wait, or switch to `flash` / `classic`.
- **`SAFETY` block** → response has `promptFeedback.blockReason` and no image. Rewrite the prompt and retry.
- **No image in response** → model returned only text. Usually means the prompt was ambiguous or refused. Add "generate an image of..." explicitly.
- **Aspect ratio is best-effort** — Gemini doesn't expose a strict `aspectRatio` field on image models, so the CLI appends a textual hint.

## File Layout

```
<your-skills-dir>/nano-banana/
  SKILL.md                              ← this file
<your-tools-dir>/
  nano-banana.js                        ← the CLI implementation
  nano-banana-output/                   ← generated images
~/bin/nano-banana                       ← symlink to nano-banana.js
~/.openclaw/credentials/google/
  gemini_api_key                        ← the secret (chmod 600)
```
