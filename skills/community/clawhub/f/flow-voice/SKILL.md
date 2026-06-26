---
name: FlowVoice
description: Clone any voice from a short audio sample and generate speech with it. Powered by LuxTTS (150x realtime, local, free, no API key). Use when asked to clone a voice, generate a voiceover, add speech to a video, or bake audio into an animation. Supports wav/mp3 input, 48kHz output. Works on CPU and MPS (Apple Silicon).
homepage: https://github.com/ysharma3501/LuxTTS
metadata:
  openclaw:
    emoji: "🎙️"
    version: "1.0.0"
    author: "windseeker1111"
    requires:
      bins: ["uv", "ffmpeg"]
      pip: ["zipvoice", "soundfile", "librosa"]
---

# Flow Voice — Voice Cloning for OpenClaw

Clone any voice from a 3–30 second audio sample and generate speech from text. Powered by **LuxTTS** — 150x realtime, runs locally, fits in 1GB VRAM, works on CPU and Apple Silicon MPS. No API key, no cloud, no cost.

**Output directory:** `~/clawd/output/voice/`

---

## Commands

| What you say | What it does |
|---|---|
| "clone this voice [audio file]" | Encode a voice profile from a sample |
| "speak as [name]: [text]" | Generate speech using a saved voice profile |
| "add voiceover to [video]: [text]" | Generate speech + bake into video with ffmpeg |
| "list voices" | Show saved voice profiles |
| "clone voice from URL [url]" | Download audio from URL, then clone |

---

## Workflow

### Step 1: Clone a voice

```bash
uv run ~/clawd/skills/flow-voice/scripts/clone.py \
  --sample /path/to/sample.wav \
  --name "eric"
```

Saves encoded profile to `~/clawd/output/voice/profiles/eric.pkl`.
Requires at least 3 seconds of clean audio. 10–30 seconds is ideal.

### Step 2: Generate speech

```bash
uv run ~/clawd/skills/flow-voice/scripts/speak.py \
  --voice "eric" \
  --text "Hello, this is a test of voice cloning." \
  --output ~/clawd/output/voice/output.wav
```

Outputs 48kHz WAV. Use `--speed 1.0` to adjust pace.

### Step 3: Bake into video (optional)

```bash
uv run ~/clawd/skills/flow-voice/scripts/speak.py \
  --voice "eric" \
  --text "Your agent can think. Now teach it to draw." \
  --output /tmp/vo.wav

ffmpeg -i input.mp4 -i /tmp/vo.wav \
  -c:v copy -c:a aac -shortest output_with_voice.mp4
```

---

## One-Shot: Clone + Speak in one command

```bash
uv run ~/clawd/skills/flow-voice/scripts/flow_voice.py \
  --sample /path/to/sample.wav \
  --text "Beautiful diagrams, from a single prompt." \
  --output ~/clawd/output/voice/result.wav
```

No profile saving — just clone and speak immediately.

### Bake voiceover directly into a video

```bash
uv run ~/clawd/skills/flow-voice/scripts/flow_voice.py \
  --sample /path/to/sample.wav \
  --text "Your agent can think. Now teach it to draw." \
  --video /path/to/animation.mp4 \
  --output ~/clawd/output/voice/final_with_voice.mp4
```

---

## Parameters

| Flag | Default | Description |
|---|---|---|
| `--sample` | required | Reference audio file (wav/mp3, min 3s) |
| `--text` | required | Text to speak |
| `--output` | auto-named | Output file path |
| `--video` | none | If set, bakes audio into this video |
| `--voice` | none | Use saved profile instead of --sample |
| `--name` | none | Save cloned profile with this name |
| `--speed` | 1.0 | Speech speed (0.8 = slower, 1.2 = faster) |
| `--steps` | 4 | Inference steps (3–4 recommended) |
| `--t-shift` | 0.9 | Sampling param (higher = potentially better quality) |
| `--smooth` | false | Add smoothing (reduces metallic artifacts) |
| `--device` | auto | Force cpu / mps / cuda |

---

## Tips

- **Minimum 3 seconds** of audio for cloning — 10–30s is ideal
- If you hear **metallic artifacts**, add `--smooth`
- For Apple Silicon (M1/M2/M3), device defaults to `mps` automatically
- First run downloads the model (~200MB) to `~/.cache/huggingface/`
- **Clean audio works best** — no background music or noise in the reference sample

---

## Examples

**Clone Eric's voice from a recording:**
```bash
uv run ~/clawd/skills/flow-voice/scripts/flow_voice.py \
  --sample ~/recordings/eric-30s.wav \
  --name eric \
  --text "FlowStay is live. Book your room with AI." \
  --output ~/clawd/output/voice/flowstay-promo.wav
```

**Add voiceover to a Flow Visual Explainer animation:**
```bash
uv run ~/clawd/skills/flow-voice/scripts/flow_voice.py \
  --voice eric \
  --text "Your agent can think. Now teach it to draw." \
  --video ~/clawd/2026-03-10-flowvisual-c3-magic-wand-comp.mp4 \
  --output ~/clawd/output/voice/flowvisual-voiced.mp4
```

**Quick one-shot from a downloaded audio clip:**
```bash
yt-dlp -x --audio-format wav -o /tmp/ref.wav "https://www.instagram.com/reel/..."
uv run ~/clawd/skills/flow-voice/scripts/flow_voice.py \
  --sample /tmp/ref.wav \
  --text "Hello from OpenClaw." \
  --output ~/clawd/output/voice/test.wav
```

---

*Powered by LuxTTS (ysharma3501/LuxTTS, ZipVoice-based) — Free, local, no API key required.*
*Packaged for OpenClaw by Flow — March 2026*
