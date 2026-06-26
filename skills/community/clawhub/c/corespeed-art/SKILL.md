---
name: corespeed-art
description: Generate video, images, audio, and music using 40+ AI models via fal.ai. Use for video generation (Kling v3, Sora 2, Veo 3.1, LTX 2.3, Pixverse v5), image generation (Nano Banana 2, FLUX 2 Pro/Schnell, GPT Image 1.5, Qwen Image 2 Pro, Recraft V4, Seedream 5), text-to-speech (MiniMax Speech-02 HD), music/sound effects (Beatoven), and utilities (Topaz upscale, background removal, lipsync). Use when a user asks to create videos, generate images, produce voiceovers, create music/sound effects, upscale media, remove backgrounds, or combine multiple AI media models in a single workflow.
metadata:
  {
    "openclaw":
      {
        "emoji": "🎬",
        "requires": { "bins": ["uv"], "env": ["FAL_KEY"] },
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

# Corespeed Art — Multi-Model AI Media via fal.ai

Auth: Set `FAL_KEY` with your fal.ai API key (get one at https://fal.ai/dashboard/keys).

## Workflow

1. Pick a model from the tables below
2. **Read its reference file** to get the exact endpoint and parameters
3. Run the command with the endpoint and JSON parameters

## Usage

```bash
uv run {baseDir}/scripts/fal.py ENDPOINT --json '{"param":"value"}' -f output.ext [-i input.ext]
```

- `ENDPOINT` — the fal.ai model path from the reference file (e.g. `fal-ai/nano-banana-2`)
- `--json` — model parameters as JSON object
- `-f` — output filename
- `-i` — input file(s) to upload (repeat for multiple), auto-injected as `image_url`/`image_urls`/`start_image_url`/`video_url`
- `--audio` — audio input file (for lipsync)

## Image Generation

| Model | Best For | Reference |
|-------|----------|-----------|
| Nano Banana 2 | Pro quality, web search, thinking | Read [nanobanana.md](references/nanobanana.md) |
| FLUX 2 Pro | Photorealistic, zero-config | Read [flux.md](references/flux.md) |
| FLUX Schnell | ⚡ Fastest iteration | Read [flux.md](references/flux.md) |
| FLUX Pro v1.1 | Accelerated, commercial use | Read [flux.md](references/flux.md) |
| FLUX.1 Dev | 12B params, fine-tuning friendly | Read [flux.md](references/flux.md) |
| GPT Image 1.5 | Transparent bg, instruction following | Read [gpt.md](references/gpt.md) |
| Qwen Image 2 Pro | Chinese+English, typography, native 2K | Read [qwen.md](references/qwen.md) |
| Recraft V4 Pro | Design/marketing, color control | Read [recraft.md](references/recraft.md) |
| Seedream 5 Lite | Multi-image editing, reasoning | Read [seedream.md](references/seedream.md) |

## Video Generation

| Model | Best For | Reference |
|-------|----------|-----------|
| Kling v3 Pro I2V | Best I2V, multi-shot, audio, 3–15s | Read [kling.md](references/kling.md) |
| Sora 2 T2V | Long video up to 20s, characters | Read [sora.md](references/sora.md) |
| Sora 2 I2V | Image→video with Sora | Read [sora.md](references/sora.md) |
| Veo 3.1 T2V | Cinematic + native audio/dialogue | Read [veo.md](references/veo.md) |
| Veo 3.1 I2V | Image→video with audio | Read [veo.md](references/veo.md) |
| LTX 2.3 T2V Fast | ⚡ Fast, up to 2160p/20s, open source | Read [ltx.md](references/ltx.md) |
| LTX 2.3 I2V | Image→video, start+end frame | Read [ltx.md](references/ltx.md) |
| Pixverse v5 I2V | Anime, 3D, clay, cyberpunk styles | Read [pixverse.md](references/pixverse.md) |

## Audio / TTS

| Model | Best For | Reference |
|-------|----------|-----------|
| MiniMax Speech-02 HD | 30+ languages, loudness normalization | Read [minimax-speech.md](references/minimax-speech.md) |

## Music & Sound Effects

| Model | Best For | Reference |
|-------|----------|-----------|
| Beatoven Music | AI music, up to 90s | Read [beatoven-music.md](references/beatoven-music.md) |

## Utilities

| Tool | Best For | Reference |
|------|----------|-----------|
| Topaz Upscale | AI image/video upscale 2x–4x | Read [topaz.md](references/topaz.md) |
| BRIA RMBG | Professional background removal | Read [bria-rmbg.md](references/bria-rmbg.md) |
| Sync Lipsync | Audio-driven lip sync on video | Read [sync-lipsync.md](references/sync-lipsync.md) |

## Notes

- **No manual Python setup required.** The script uses [PEP 723 inline metadata](https://peps.python.org/pep-0723/). `uv run` automatically creates an isolated virtual environment and installs the `fal-client` dependency on first run.
- fal.ai uses a **queue** system — the script polls until generation completes.
- Video generation can take 30s–3min.
- Use timestamps in filenames: `yyyy-mm-dd-hh-mm-ss-name.ext`.
- Script prints `MEDIA:` line for OpenClaw to auto-attach.
- Do not read generated media back; report the saved path only.
