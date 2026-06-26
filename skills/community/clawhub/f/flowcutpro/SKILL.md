---
name: flowcutpro
version: 1.0.0
description: >
  AI-powered cinematic video production using Google Veo 3 as the renderer and
  OpenClaw's configured LLM as the creative brain. Use when asked to create
  videos, animate concepts, generate Reels/TikToks, produce commercials, or
  turn any text concept into a stitched cinematic video. The LLM plans shots,
  writes optimized Veo 3 prompts, maintains style consistency, and runs a
  quality loop. Veo 3 renders. ffmpeg stitches. Triggers on: "make a video",
  "create a clip", "generate a reel", "produce a commercial", "animate this",
  "video generation", "FlowCutPro", "flowcutpro".
author: flowverse
tags: [video, veo3, cinematic, reels, tiktok, content, production]
install: clawhub install flowcutpro
---

# FlowCutPro — AI Cinematic Video Production

**Two-layer architecture:**
- **Brain:** OpenClaw's configured LLM — shot planning, prompt engineering, style consistency, quality evaluation
- **Renderer:** Google Veo 3 (`veo-3.1-generate-preview`) — photorealistic, physics-accurate, cinematic camera moves, 9:16/16:9/1:1

The LLM does the creative work. Veo 3 renders. ffmpeg stitches. You get professional video from a casual prompt.

---

## Pipeline

```
User concept
    ↓
LLM: Shot Planner — breaks concept into N shots with timing + camera moves
    ↓
LLM: Prompt Engineer — expands each shot into optimized Veo 3 cinematic prompt
    ↓
Veo 3: Render shots in batches of 5 (API concurrent limit)
    ↓
LLM: Quality Evaluator — reviews output thumbnails vs brief, flags misses
    ↓
Veo 3: Regenerate any failing shots (up to 2 retries)
    ↓
ffmpeg: Stitch clips with crossfades → final video
    ↓
Deliver
```

---

## Setup

### Veo 3 API Key
Get a Gemini API key from https://aistudio.google.com/apikeys
```bash
export VEO_API_KEY="your-key-here"
```
Or store in 1Password: `op://flow/gemini-api-key/key`

### Dependencies
```bash
pip install Pillow requests  # optional for thumbnails
brew install ffmpeg
```

---

## Usage

```bash
# Single concept → full stitched video
python3 ~/clawd/skills/flowcutpro/scripts/flowcutpro.py \
  --concept "A luxury hotel guest arriving at sunset in Puerto Rico" \
  --shots 6 \
  --aspect-ratio 9:16 \
  --output-dir ~/clawd/output/flowcutpro/

# Reel / TikTok
python3 ~/clawd/skills/flowcutpro/scripts/flowcutpro.py \
  --concept "Morning coffee ritual in a minimalist Tokyo apartment" \
  --shots 4 \
  --aspect-ratio 9:16 \
  --duration 5 \
  --output-dir ~/clawd/output/flowcutpro/

# Cinematic widescreen
python3 ~/clawd/skills/flowcutpro/scripts/flowcutpro.py \
  --concept "A founder's journey from garage to IPO day" \
  --shots 8 \
  --aspect-ratio 16:9 \
  --output-dir ~/clawd/output/flowcutpro/

# Dry run (inspect shot plan without rendering)
python3 ~/clawd/skills/flowcutpro/scripts/flowcutpro.py \
  --concept "Product launch event at a Silicon Valley rooftop" \
  --shots 5 \
  --dry-run

# Render specific shots only (re-render misses)
python3 ~/clawd/skills/flowcutpro/scripts/flowcutpro.py \
  --concept "..." \
  --shots 6 \
  --only-shots 3 5
```

---

## Output

```
~/clawd/output/flowcutpro/
  20260329-120000-shot01-arrival.mp4
  20260329-120000-shot02-lobby.mp4
  ...
  20260329-120000-FINAL-9x16.mp4   ← stitched master
```

---

## Prompt Engineering — Veo 3 Best Practices

FlowCutPro automatically applies these rules when generating prompts:

1. **Always specify aspect ratio** at the start: "Cinematic vertical 9:16 portrait..."
2. **Describe camera movement** explicitly: slow push-in, dolly, crane, static wide, tracking shot
3. **Specify lighting**: golden hour, overcast, blue hour, candlelit, harsh noon
4. **Include motion direction**: "camera slowly pushes forward", "slow pan left to right"
5. **Name the aesthetic**: cinematic, film grain, photorealistic, documentary, editorial
6. **Negative elements**: "no text overlays, no logos, no CGI artifacts"
7. **Duration awareness**: 5–8s per shot is optimal; 5s for fast cuts, 8s for slow moody shots
8. **Style consistency prefix**: Start every shot prompt with the same style fingerprint for visual coherence across cuts

---

## Examples

See `examples/` folder:
- `hotel-commercial.py` — 8-shot luxury hotel commercial (9:16)
- `product-launch.py` — 6-shot product launch reel (9:16)
- `brand-story.py` — 10-shot founder story (16:9)

---

## Technical Details

- **Model:** `veo-3.1-generate-preview` (Google Generative AI)
- **Endpoint:** `https://generativelanguage.googleapis.com/v1beta/models/veo-3.1-generate-preview:predictLongRunning`
- **Aspect ratios:** `9:16`, `16:9`, `1:1`
- **Duration:** 5–8 seconds per shot
- **Concurrent limit:** 5 shots per batch (enforced automatically)
- **Stitch:** ffmpeg xfade crossfade (0.5s transitions)
- **Output codec:** H.264, CRF 18 (high quality)
- **Polling:** 15s intervals, 10-minute timeout per shot

---

## Limits & Notes

- Veo 3 API is currently in preview — requires allowlist access via Google AI Studio
- Each shot takes ~2–4 minutes to render
- 10-shot video ≈ 20–40 minutes total (parallel batches of 5)
- API key needs Gemini API enabled in Google Cloud Console
- Free tier: limited daily quota; paid tier recommended for production use
