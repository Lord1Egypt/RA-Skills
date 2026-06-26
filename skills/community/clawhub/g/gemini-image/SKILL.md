---
name: gemini-image
description: Generate or edit images using Gemini API with multiple reference image support. Use for image generation, style transfer, combining references, UI mockups, or any visual creation task.
homepage: https://ai.google.dev/gemini-api/docs/image-generation
metadata: {"clawdbot":{"emoji":"🎨","requires":{"bins":["uv"],"env":["GEMINI_API_KEY"]},"primaryEnv":"GEMINI_API_KEY","install":[{"id":"uv-brew","kind":"brew","formula":"uv","bins":["uv"],"label":"Install uv (brew)"}]}}
---

# Gemini Image Generation

Generate images with support for multiple reference images (up to 14).

## Setup

**Required:** `GEMINI_API_KEY` environment variable

Get your API key at: https://aistudio.google.com/apikey

Set it:
```bash
export GEMINI_API_KEY="your-key-here"
```

Or in your OpenClaw config (`~/.openclaw/openclaw.json`):
```json
{
  "skills": {
    "entries": {
      "gemini-image": {
        "env": { "GEMINI_API_KEY": "your-key-here" }
      }
    }
  }
}
```

## Usage

```bash
# Generate from prompt
uv run {baseDir}/scripts/generate.py -p "a sunset over mountains" -o sunset.png

# Edit/transform one image
uv run {baseDir}/scripts/generate.py -p "make this pop art style" -i photo.png -o popart.png

# Combine multiple references (up to 14)
uv run {baseDir}/scripts/generate.py -p "combine style of first with content of second" \
  -i style-ref.png -i content.png -o combined.png

# With aspect ratio
uv run {baseDir}/scripts/generate.py -p "wide landscape" -a "16:9" -o wide.png

# Higher resolution
uv run {baseDir}/scripts/generate.py -p "detailed portrait" -r 2K -o portrait.png
```

## Options

| Flag | Description |
|------|-------------|
| `-p, --prompt` | Image prompt (required) |
| `-o, --output` | Output filename (required) |
| `-i, --input-image` | Reference image (repeatable, up to 14) |
| `-m, --model` | `pro` (default), `flash2`, `flash`, or `exp` |
| `-r, --resolution` | `1K` (default), `512`, `2K`, `4K` (pro/flash2) |
| `-a, --aspect-ratio` | See ratios below (pro/flash2) |
| `-t, --thinking` | `minimal` (default), `high`, `dynamic` (pro/flash2) |

## Models

- **pro** (`gemini-3-pro-image-preview`) — Highest quality, thinking mode, up to 14 refs, aspect ratio + resolution
- **flash2** (`gemini-3.1-flash-image-preview`) — **NEW: Nano Banana 2.** Best price/perf, thinking levels, great text rendering, localization, aspect ratio + resolution + 512px
- **flash** (`gemini-2.5-flash-image`) — Older Flash, simpler config, no aspect ratio/resolution control
- **exp** (`gemini-2.0-flash-exp`) — Experimental, good for edits

**When to use flash2 vs pro:**
- **flash2** — Fast iterations, text-heavy images, localization, bulk generation, great quality at lower cost
- **pro** — Maximum quality, complex multi-reference compositions, highest fidelity

## Aspect Ratios (pro/flash2)

`1:1` · `2:3` · `3:2` · `3:4` · `4:3` · `4:5` · `5:4` · `9:16` · `16:9` · `21:9` · `4:1` · `1:4` · `8:1` · `1:8`

## Thinking Levels (pro/flash2)

Control how much the model reasons before generating:
- **minimal** (default) — Fast, good for simple prompts
- **high** — Better quality for complex multi-element prompts
- **dynamic** — Model decides how much thinking is needed

```bash
# Complex scene with high thinking
uv run {baseDir}/scripts/generate.py -p "detailed city scene with specific text overlay" -m flash2 -t high -o city.png
```

## Reference Image Limits

| Model | Max Images | Notes |
|-------|------------|-------|
| **pro** | 14 total | 5 high-fidelity, 6 objects, 5 humans |
| **flash** | 3 | Best with ≤3 inputs |
| **exp** | varies | Experimental |

## Batch Generation (50% cheaper)

For bulk jobs that can wait 24hr, use the batch API.

### "Batch Submit" Workflow

When user says **"batch submit"**, follow this automated workflow:

1. **Submit batch job** — Create JSONL, run `batch.py submit`
2. **Create hourly cron** — Check batch status every hour
3. **On completion** — Download images to specified output directory
4. **Deliver to originating channel** — Send all images to the channel where the request was made (Telegram, Discord, Signal, etc.)
5. **Self-disable cron** — Remove the cron job after successful delivery

**Cron job text template:**
```
Check gemini-image batch [BATCH_ID]. If complete: download to [OUTPUT_DIR], send all images to [CHANNEL], then disable this cron job.
```

### Manual Batch Commands

**1. Create requests JSONL** (one per line):
```json
{"key": "sunset", "prompt": "a sunset over mountains", "aspect_ratio": "16:9", "resolution": "2K"}
{"key": "portrait", "prompt": "corporate headshot", "input_images": ["/path/to/ref.png"]}
```

**2. Submit batch:**
```bash
uv run {baseDir}/scripts/batch.py submit requests.jsonl
```

**3. Check status** (typically ready within 24hr):
```bash
uv run {baseDir}/scripts/batch.py status
```

**4. Download when done:**
```bash
uv run {baseDir}/scripts/batch.py download -o ./images/
```

**When to use batch vs instant:**
- Need it now → `generate.py` (instant, full price)
- Bulk generation, can wait → `batch.py` (24hr, 50% off)

## Prompting Guide

See [references/prompting.md](references/prompting.md) for detailed strategies:

**Generation:**
- Photorealistic scenes (camera/lens/lighting terms)
- Stylized illustrations & stickers (transparent backgrounds)
- Text rendering (logos, typography)
- Product mockups (commercial photography)
- Minimalist/negative space design
- Sequential art (comics, storyboards)
- Google Search grounding (real-time info)
- iOS wireframes & UI mockups

**Editing:**
- Adding/removing elements
- Inpainting (semantic masking)
- Style transfer
- Combining multiple images
- High-fidelity detail preservation
- Sketch → finished image
- Character consistency (360 views)

**Core principle:** Describe the scene narratively, don't just list keywords.

## Tips

- Images go first in context, prompt last — order `-i` flags intentionally
- For style transfer: first image = style reference, second = content
- Pro model uses "Thinking" phase to plan composition before generating
- Timestamps in filenames: `2026-01-26-sunset.png`
- Script outputs `MEDIA:` line for Clawdbot auto-attach

## Draft Mode (Preview Before Generate)

For complex generations — especially UI mockups and wireframes — use a two-step workflow:

### Step 1: Draft the JSON Prompt

When user asks for a wireframe or complex image, **show the structured prompt first** instead of generating immediately:

```
Here's the prompt I'll use:

{
  "image_type": "UI mockup",
  "device": {"frame": "iPhone 16 Pro", "orientation": "portrait"},
  "design_system": {
    "style": "iOS 18 native",
    "corners": "rounded, 16px radius",
    "shadows": "soft drop shadows",
    "spacing": "8pt grid",
    "font": "SF Pro"
  },
  "layout": {
    "header": "Navigation bar with back button and title 'Settings'",
    "content": "List of settings items with icons and toggles",
    "bottom": "Tab bar with 4 items"
  }
}

Want me to generate this, or should I adjust anything first?
```

### Step 2: User Approves or Tweaks

- **"looks good"** / **"generate"** → Run the generation
- **"make the header bigger"** / **"add a search bar"** → Update JSON, show again
- **"use flash model"** → Note the model preference

### Step 3: Generate

Convert JSON to narrative prompt and run:
```bash
uv run {baseDir}/scripts/generate.py \
  -p "[narrative version of JSON]" \
  -o mockup.png \
  -a "9:16" \
  -m pro
```

### When to Use Draft Mode

| Use Draft Mode | Skip Draft (Generate Direct) |
|----------------|------------------------------|
| UI mockups / wireframes (new) | Simple images ("sunset over mountains") |
| Complex multi-element scenes | Style transfer with clear reference |
| User says "let me see the prompt first" | User says "just make it" |
| Previous generation failed/missed the mark | Simple edits (color swap, minor tweaks) |
| **Structural changes to existing image** | — |

**Trigger phrases for draft mode:**
- "wireframe", "mockup", "UI", "screen design"
- "let me review the prompt"
- "show me what you'll generate"
- "draft first"

**Edit iterations:**
- **Simple tweaks** (color change, font swap) → Generate directly, no approval needed
- **Structural changes** (new elements, layout changes, removing sections) → Show change summary for approval

## iOS Wireframes

Quick example:
```bash
uv run {baseDir}/scripts/generate.py \
  -p "Convert this wireframe to high-fidelity iOS 18 UI. iPhone 16 Pro frame, rounded corners, soft shadows, SF Pro font. Interpret: scribbles→images, rectangles→buttons, lines→text" \
  -i wireframe-sketch.png \
  -o mockup.png \
  -a "9:16"
```

See [references/prompting.md](references/prompting.md) for detailed templates including JSON-structured prompts and multi-screen flows.
