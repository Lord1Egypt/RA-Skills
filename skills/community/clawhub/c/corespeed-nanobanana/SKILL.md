---
name: corespeed-nanobanana
description: Generate and edit images using Google Gemini models via Corespeed AI Gateway. Supports text-to-image generation, image editing, multi-image input, and text rendering in images using gemini-2.5-flash-image. Also supports text generation and image analysis with gemini-2.5-flash, gemini-2.5-pro, and gemini-2.5-flash-lite. Use when a user asks to create images, edit photos, analyze images, or generate text with Gemini models.
metadata:
  {
    "openclaw":
      {
        "emoji": "🍌",
        "requires": { "bins": ["uv"], "env": ["CS_AI_GATEWAY_BASE_URL", "CS_AI_GATEWAY_API_TOKEN"] },
        "install":
          [
            {
              "id": "uv-pip",
              "kind": "shell",
              "command": "pip install uv || pip3 install uv",
              "bins": ["uv"],
              "label": "Install uv via pip (https://github.com/astral-sh/uv)",
            },
          ],
      },
  }
---

# Corespeed NanoBanana — Gemini Image & Text Generation

Auth: Set `CS_AI_GATEWAY_BASE_URL` and `CS_AI_GATEWAY_API_TOKEN` environment variables.

## Workflow

1. Pick a model from the table below (default: `gemini-2.5-flash-image` for image generation)
2. Run the script with your prompt

## Usage

```bash
uv run {baseDir}/scripts/gemini.py --prompt "your prompt" -f output.ext [-i input.ext] [--model MODEL]
```

- `--prompt`, `-p` — Text prompt (required)
- `--filename`, `-f` — Output filename (required)
- `--input`, `-i` — Input image file(s), repeat for multiple
- `--model`, `-m` — Model name (default: `gemini-2.5-flash-image`)
- `--modalities` — Response type: `auto`, `image`, `text`, `image+text` (default: `auto`)
- `--json` — Output structured JSON (recommended for agent consumption)

Output format is determined by file extension: `.png`/`.jpg` → image generation, `.txt`/`.md` → text output.

## Image Generation

```bash
# Text-to-image
uv run {baseDir}/scripts/gemini.py -p "a watercolor fox in autumn forest" -f fox.png

# Image editing
uv run {baseDir}/scripts/gemini.py -p "Remove background, add beach sunset" -f edited.png -i photo.jpg

# Multi-image compositing
uv run {baseDir}/scripts/gemini.py -p "Blend these two scenes together" -f blend.png -i scene1.png -i scene2.png
```

## Image Analysis

```bash
# Describe an image
uv run {baseDir}/scripts/gemini.py -p "Describe this image" -f desc.txt -i photo.jpg --model gemini-2.5-flash

# Compare images
uv run {baseDir}/scripts/gemini.py -p "What are the differences?" -f diff.txt -i before.jpg -i after.jpg --model gemini-2.5-flash
```

## Text Generation

```bash
# Use the most capable model for complex tasks
uv run {baseDir}/scripts/gemini.py -p "Write a haiku about coding" -f haiku.txt --model gemini-2.5-pro
```

## Models

| Model | Type | Best For |
|-------|------|----------|
| gemini-2.5-flash-image | Image + Text | Image generation & editing (default) |
| gemini-2.5-flash | Text | Fast analysis, vision, general tasks |
| gemini-2.5-pro | Text | Complex reasoning, highest quality |
| gemini-2.5-flash-lite | Text | Fastest, simple tasks |

## Notes

- **No manual Python setup required.** The script uses [PEP 723 inline metadata](https://peps.python.org/pep-0723/). `uv run` automatically creates an isolated virtual environment and installs the `google-genai` dependency on first run.
- Image output is returned inline as base64 from the Gemini API — no separate download step.
- Use timestamps in filenames: `yyyy-mm-dd-hh-mm-ss-name.ext`.
- Script prints `MEDIA:` line for OpenClaw to auto-attach generated images.
- Do not read generated media back; report the saved path only.
- Only `gemini-2.5-flash-image` can generate images. Other models are text-only.
- Use `--json` for structured output: `{"ok": true, "files": [...], "text": "...", "model": "...", "tokens": {...}}`

## Support

Built by [Corespeed](https://corespeed.io). If you need help or run into issues:

- 💬 Discord: [discord.gg/mAfhakVRnJ](https://discord.gg/mAfhakVRnJ)
- 🐦 X/Twitter: [@CoreSpeed_io](https://x.com/CoreSpeed_io)
- 🐙 GitHub: [github.com/corespeed-io/skills](https://github.com/corespeed-io/skills/issues)
