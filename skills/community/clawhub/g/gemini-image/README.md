# 🎨 Gemini Image

An [OpenClaw](https://github.com/openclaw/openclaw) skill for generating and editing images with Google's Gemini API. Supports multiple reference images (up to 14), batch generation at 50% off, thinking levels, and 4 model tiers.

## Features

- **4 models** — Pro (highest quality), Flash 2 / Nano Banana 2 (best price/perf), Flash (simple), Exp (experimental)
- **Up to 14 reference images** — style transfer, multi-ref composition, character consistency
- **Batch API** — submit bulk jobs at 50% cost, results within 24hr
- **Thinking levels** — minimal, high, dynamic — control quality vs speed
- **Aspect ratios** — 14 options from 1:1 to 8:1
- **Resolution control** — 512px to 4K
- **Draft mode** — preview complex prompts before generating
- **Zero dependencies** beyond `uv` and a Gemini API key

## Install

### As an OpenClaw Skill

```bash
git clone https://github.com/teebs4140/gemini-image.git
cd gemini-image
./install-skill.sh
```

Then add your API key to your OpenClaw config (`~/.openclaw/openclaw.json`):

```json
{
  "skills": {
    "entries": {
      "gemini-image": {
        "env": {
          "GEMINI_API_KEY": "your-key-here"
        }
      }
    }
  }
}
```

Restart your gateway (`openclaw gateway restart`) and the skill is live.

### Standalone (No OpenClaw)

Just clone and run the scripts directly with `uv`:

```bash
git clone https://github.com/teebs4140/gemini-image.git
cd gemini-image
export GEMINI_API_KEY="your-key"
uv run scripts/generate.py -p "a sunset over mountains" -o sunset.png
```

## Requirements

1. A Gemini API key (free) — [aistudio.google.com/apikey](https://aistudio.google.com/apikey)
2. [uv](https://docs.astral.sh/uv/) — `brew install uv` or `curl -LsSf https://astral.sh/uv/install.sh | sh`

## Usage

### Generate from a prompt

```bash
uv run scripts/generate.py -p "a watercolor painting of a coastal town" -o town.png
```

### Edit an existing image

```bash
uv run scripts/generate.py -p "make this pop art style" -i photo.png -o popart.png
```

### Combine multiple reference images

```bash
uv run scripts/generate.py \
  -p "combine the style of the first image with the content of the second" \
  -i style-ref.png -i content.png -o combined.png
```

### Control aspect ratio and resolution

```bash
uv run scripts/generate.py -p "wide cinematic landscape" -a "16:9" -r 2K -o landscape.png
```

### Use thinking for complex prompts

```bash
uv run scripts/generate.py -p "detailed city scene with neon signs reading 'OPEN 24/7'" \
  -m flash2 -t high -o city.png
```

## Options

| Flag | Description |
|------|-------------|
| `-p, --prompt` | Image prompt (required) |
| `-o, --output` | Output filename (required) |
| `-i, --input-image` | Reference image (repeatable, up to 14) |
| `-m, --model` | `pro` (default), `flash2`, `flash`, `exp` |
| `-r, --resolution` | `512`, `1K` (default), `2K`, `4K` |
| `-a, --aspect-ratio` | `1:1`, `16:9`, `9:16`, `3:2`, etc. |
| `-t, --thinking` | `minimal` (default), `high`, `dynamic` |

## Models

| Model | Best For | Max Refs | Aspect/Resolution |
|-------|----------|----------|-------------------|
| **pro** | Maximum quality, complex compositions | 14 | ✅ |
| **flash2** | Fast iterations, text rendering, bulk work | 14 | ✅ |
| **flash** | Simple generations | 3 | ❌ |
| **exp** | Experimental edits | varies | ❌ |

## Batch API (50% Cheaper)

For bulk generation that can wait up to 24 hours:

**1. Create a requests file** (`requests.jsonl`):
```json
{"key": "sunset", "prompt": "a sunset over mountains", "aspect_ratio": "16:9", "resolution": "2K"}
{"key": "portrait", "prompt": "corporate headshot", "input_images": ["/path/to/ref.png"]}
```

**2. Submit, check, download:**
```bash
uv run scripts/batch.py submit requests.jsonl
uv run scripts/batch.py status
uv run scripts/batch.py download -o ./images/
```

## Prompting Guide

See [references/prompting.md](references/prompting.md) for detailed strategies covering:

- Photorealistic scenes (camera/lens/lighting terminology)
- Stylized illustrations & stickers
- Text rendering (logos, typography)
- Product mockups
- iOS wireframes & UI mockups
- Style transfer & multi-image composition
- Character consistency

**Core principle:** Describe the scene narratively. Paragraphs beat keyword lists.

## Companion Skills

- **nano-triple** by [@mvanhorn](https://x.com/mvanhorn) — generates 3 variations of the same prompt so you can pick the best one. Great UX pattern for iterative image work.

## License

MIT
