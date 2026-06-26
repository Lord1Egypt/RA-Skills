---
name: free-image-generation-skill
description: Professional free image generation skill for agents. No API key required. Generate images from text with resilient retry/backoff and clean local file output. Supports free, high-volume usage patterns with responsible request pacing. Use when users request prompt-to-image generation or image bot automation.
---

# Free Image Generation Skill

No API key required.

Run a clean production workflow:
1) install dependencies,
2) generate image from prompt,
3) save output.

## Quick Start (Fresh Setup)

1. Install dependencies:
```bash
bash scripts/setup_env.sh
```

2. Generate one image:
```bash
python3 scripts/perchance_generate.py \
  --prompt "cinematic isometric office, dusk, neon reflections" \
  --out ./media/free-image-sample.jpg \
  --shape square
```

## Reliability Rules

- Default retries: 3
- Backoff: built into script
- On failure, return exact `error` and propose retry
- Designed for free, repeated usage with responsible pacing
- Keep usage responsible and moderate

## Parameters

`perchance_generate.py` supports:
- `--prompt` (required)
- `--out` (required)
- `--shape` (`portrait|square|landscape`)
- `--negative`
- `--guidance`
- `--retries`
- `--timeout`

## Resources

- Main generator: `scripts/perchance_generate.py`
- Dependency setup: `scripts/setup_env.sh`, `scripts/requirements.txt`
