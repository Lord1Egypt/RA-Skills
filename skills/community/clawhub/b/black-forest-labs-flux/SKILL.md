---
name: black-forest-labs-flux
description: Generate images with Black Forest Labs FLUX models using a direct BFL API key. Use when the user wants FLUX image generation through Black Forest Labs itself (not fal.ai), already has a BFL API key, or specifically mentions Black Forest Labs, BFL, flux-2-pro-preview, flux-pro, flux-dev, or flux-kontext models.
---

# Black Forest Labs FLUX

Generate images through **Black Forest Labs' direct API** using the bundled script in `scripts/bfl-generate.sh`.

## Quick start

1. Ensure `BFL_API_KEY` is available in the environment or in `/root/.clawdbot/.env`.
2. Run:

```bash
/root/clawd/skills/black-forest-labs-flux/scripts/bfl-generate.sh "your prompt here" [output-file]
```

Example:

```bash
/root/clawd/skills/black-forest-labs-flux/scripts/bfl-generate.sh \
  "A cinematic scene of a monkey sitting proudly on top of a red Ferrari sports car" \
  /root/clawd/output/monkey-ferrari.jpg
```

The script prints the saved file path on success.

## When to use this skill

Use this skill when:
- The user has a **Black Forest Labs API key**
- The user wants **direct FLUX generation** instead of fal.ai or another wrapper
- The user mentions **BFL**, **Black Forest Labs**, or direct FLUX model endpoints

Do **not** use this skill for:
- fal.ai keys (`FAL_KEY`) — use built-in fal support instead
- OpenAI image generation
- Google Gemini image generation

## Default behavior

The script defaults to:
- model: `flux-2-pro-preview`
- width: `1536`
- height: `1024`

Override these with environment variables before running:

```bash
export BFL_MODEL=flux-pro
export BFL_WIDTH=1024
export BFL_HEIGHT=1024
```

Then call the script normally.

## How it works

The BFL API is asynchronous:
1. Submit a generation request
2. Capture `polling_url`
3. Poll until status becomes `Ready`
4. Download the returned image URL

The bundled script already handles this flow.

## Troubleshooting

- If the script says `BFL_API_KEY not set`, add the key to the environment first.
- If generation fails, inspect the JSON returned by the API; the script prints it to stderr.
- If the request succeeds but takes longer than expected, re-run with a simpler prompt or smaller dimensions.

## scripts/

- `scripts/bfl-generate.sh` — direct Black Forest Labs FLUX generation via API
