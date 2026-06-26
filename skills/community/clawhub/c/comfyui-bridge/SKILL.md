---
name: comfyui-bridge
description: "Generate images, faceswap, edit photos, animate expressions, and do style transfer via a self-hosted ComfyUI instance on your LAN. Your GPU, your models."
homepage: https://github.com/Bortlesboat/comfyui-bridge
metadata:
  {
    "openclaw":
      {
        "emoji": "🎨",
        "requires": { "bins": ["uv"] },
        "install":
          [
            {
              "id": "uv-brew",
              "kind": "brew",
              "formula": "uv",
              "bins": ["uv"],
              "label": "Install uv (brew)",
            },
          ],
      },
  }
---

# ComfyUI Bridge

Generate images, faceswap, animate expressions, and do style transfer via a self-hosted [ComfyUI](https://github.com/comfyanonymous/ComfyUI) instance running on your LAN. No cloud API — your GPU, your models.

## Requirements

- ComfyUI Desktop (or server) running somewhere on your LAN
- [ComfyUI Bridge server](https://github.com/Bortlesboat/comfyui-bridge) running on the same machine as ComfyUI (see Setup)
- `uv` installed on the machine running OpenClaw

## Setup

### 1. Install the bridge server (on your ComfyUI machine)

The bridge is a lightweight FastAPI server that wraps ComfyUI's API:

```bash
git clone https://github.com/Bortlesboat/comfyui-bridge
cd comfyui-bridge
pip install -r requirements.txt
python bridge_server.py
# Listening on http://0.0.0.0:8100
```

### 2. Configure the skill

Set the bridge URL as an environment variable on your OpenClaw machine:

```bash
export COMFYUI_BRIDGE_URL=http://YOUR_COMFYUI_MACHINE_IP:8100
```

Or add it to your LaunchAgent/systemd service environment.

### 3. Required ComfyUI custom nodes (for all features)

Install via ComfyUI Manager:
- **ReActor** — faceswap
- **ComfyUI-LivePortrait** — expression animation
- **ComfyUI_IPAdapter_plus** — style transfer
- **WAS Node Suite** — utilities
- **ComfyUI-GGUF** — GGUF model support (optional, for FLUX)
- **rgthree-comfy** — workflow utilities

### 4. Recommended models

| Model | Use |
|---|---|
| Juggernaut XL Ragnarok | Architecture, objects, general |
| RealVisXL V5.0 Lightning | People, portraits, fast |
| FLUX.1 Dev Q5 GGUF | Maximum photorealism (slow, VRAM-heavy) |

---

## Usage

All commands use the `comfyui_generate.py` script via `uv run`. Replace `SKILL_SCRIPTS` with the path to this skill's `scripts/` directory.

**Always use `--no-media`** — include one `MEDIA: /full/path/to/output.png` in your text response instead.

### 1. Text to Image

```bash
uv run $SKILL_SCRIPTS/comfyui_generate.py \
  --prompt "your description" \
  --filename ~/.openclaw/media/outbound/output.png \
  --no-media
```

### 2. Image to Image

```bash
uv run $SKILL_SCRIPTS/comfyui_generate.py \
  --prompt "make it sunset" \
  -i /path/to/input.png \
  --strength 0.5 \
  --filename ~/.openclaw/media/outbound/output.png \
  --no-media
```

### 3. Faceswap (pipeline — best quality)

Swaps a face then runs img2img cleanup for natural blending. ~30 seconds total.

```bash
uv run $SKILL_SCRIPTS/comfyui_generate.py \
  --faceswap-pipeline \
  --source-face /path/to/source_face.png \
  -i /path/to/target.png \
  --cleanup-strength 0.40 \
  --filename ~/.openclaw/media/outbound/output.png \
  --no-media
```

### 4. Faceswap (basic)

```bash
uv run $SKILL_SCRIPTS/comfyui_generate.py \
  --faceswap \
  --source-face /path/to/source_face.png \
  -i /path/to/target.png \
  --filename ~/.openclaw/media/outbound/output.png \
  --no-media
```

### 5. Targeted Faceswap (specific face in group photo)

```bash
uv run $SKILL_SCRIPTS/comfyui_generate.py \
  --targeted-faceswap \
  --source-face /path/to/source_face.png \
  -i /path/to/group_photo.png \
  --target-face-index "1" \
  --filename ~/.openclaw/media/outbound/output.png \
  --no-media
```

Face indices: `0` = leftmost, `1` = second from left, `"0,2"` = first and third.

### 6. LivePortrait (expression animation)

```bash
uv run $SKILL_SCRIPTS/comfyui_generate.py \
  --liveportrait \
  -i /path/to/portrait.png \
  --expression-preset smile \
  --filename ~/.openclaw/media/outbound/output.png \
  --no-media
```

Presets: `smile`, `surprised`, `wink`, `suspicious`, `derp`, `angry`, `sleepy`

Fine-grained control: `--smile` (-0.3 to 1.3), `--blink-val` (-20 to 5), `--eyebrow-val` (-10 to 15), `--aaa` (-30 to 120, mouth open), `--pitch`/`--yaw`/`--roll` (-20 to 20, head rotation).

### 7. Style Transfer

Generate a new image in the style of a reference:

```bash
uv run $SKILL_SCRIPTS/comfyui_generate.py \
  --style-transfer \
  --style-ref /path/to/reference.png \
  --prompt "a portrait of a man" \
  --style-weight 0.85 \
  --filename ~/.openclaw/media/outbound/output.png \
  --no-media
```

### 8. Restyle

Apply a reference image's style to an existing photo:

```bash
uv run $SKILL_SCRIPTS/comfyui_generate.py \
  --restyle \
  --style-ref /path/to/reference.png \
  -i /path/to/photo.png \
  --style-weight 0.85 \
  --strength 0.65 \
  --filename ~/.openclaw/media/outbound/output.png \
  --no-media
```

### 9. Enhanced mode

Add `--enhanced` to any command for FaceDetailer + 4x-UltraSharp upscale (net ~2x resolution). Works with txt2img and faceswap.

---

## Quality Gates (built-in)

The script includes two automatic quality checks on faceswap outputs:

**Gate 1 — Size check:** ReActor blank outputs when no face is detected (~2KB). Any faceswap output under 10KB automatically retries once. If still blank, exits with `FACESWAP_BLANK:` error — no garbage delivered.

**Gate 2 — Vision QA:** If you have [Ollama](https://ollama.ai) running locally with `gemma3:12b`, faceswap outputs are checked with vision QA before delivery. PASS → deliver normally. FAIL → file renamed `_qa_flagged` and still delivered. Add ~10-20s but catches glitchy outputs. Disable by not having Ollama/gemma3 installed (fails open).

---

## Offline Queue

When the bridge is unreachable, requests are automatically queued to `~/.openclaw/faceswap-queue/`. A companion daemon (`queue_processor.py`) polls every 5 minutes and delivers via iMessage when the bridge comes back online.

Tell users: "Got it — the system is offline right now but your request is queued and will be sent automatically when it comes back."

---

## Options Reference

| Flag | Default | Description |
|---|---|---|
| `--prompt` / `-p` | — | Text description |
| `--filename` / `-f` | required | Output path (use `~/.openclaw/media/outbound/`) |
| `-i` / `--input-image` | — | Input image (img2img target / faceswap target / portrait) |
| `--source-face` | — | Source face image (faceswap modes) |
| `--faceswap` | false | Basic faceswap |
| `--faceswap-pipeline` | false | Faceswap + cleanup (best quality) |
| `--cleanup-strength` | `0.40` | Pipeline cleanup denoise strength |
| `--targeted-faceswap` | false | Swap specific face in multi-face image |
| `--target-face-index` | `0` | Which face(s) to replace (comma-separated) |
| `--liveportrait` | false | Expression animation mode |
| `--expression-preset` | — | smile / surprised / wink / suspicious / derp / angry / sleepy |
| `--style-transfer` | false | Generate in reference style |
| `--restyle` | false | Apply reference style to existing photo |
| `--style-ref` | — | Style reference image |
| `--style-weight` | `0.85` | Style influence (0.5–1.0) |
| `--model` / `-m` | `juggernaut` | `juggernaut`, `flux`, `realvis` |
| `--aspect-ratio` / `-a` | `1:1` | `1:1`, `4:5`, `9:16`, `16:9`, `5:4` |
| `--strength` / `-s` | `0.6` | img2img denoise strength |
| `--seed` | `-1` | Seed (-1 = random) |
| `--enhanced` / `-e` | false | FaceDetailer + 4x upscale |
| `--no-media` | false | Suppress MEDIA: stdout line (always use this) |

---

## Routing Guide

| User says | Mode |
|---|---|
| "generate an image of..." | txt2img |
| "make this look like..." (with image) | img2img |
| "put [person]'s face on this" | --faceswap-pipeline |
| "swap the second face" | --targeted-faceswap --target-face-index 1 |
| "make him smile / look surprised" | --liveportrait --expression-preset |
| "generate something that looks like this painting" | --style-transfer |
| "make this photo look like a painting" | --restyle |
| "high quality / best quality" | add --enhanced |

---

## Timing Reference

| Mode | Approximate time |
|---|---|
| txt2img (realvis) | ~5 seconds |
| txt2img (juggernaut) | ~5 minutes |
| txt2img (flux) | ~10 minutes |
| faceswap pipeline | ~30 seconds |
| liveportrait | ~7 seconds (21s first run) |
| style transfer / restyle | ~5 minutes |
| +enhanced | +10-30 seconds |
