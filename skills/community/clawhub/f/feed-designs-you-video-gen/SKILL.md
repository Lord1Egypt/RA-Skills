---
name: feed-designs-you-video-gen
version: 1.0.0
description: "Create vertical algorithm-control shorts: five equal caption beats across the runtime, UI/data-stream montage (WeryAI). Use for attention-economy critique, doomscroll hooks, or feed-steering rhetoric. Use when the user says the app chooses for them. SEO: algorithm control video; feed manipulation video."

tags: [algorithm, social-media, tech, psychology, hooks, subtitles, short-video, video-gen]

metadata: { "openclaw": { "emoji": "📱", "primaryEnv": "WERYAI_API_KEY", "paid": true, "network_required": true, "requires": { "env": ["WERYAI_API_KEY"], "bins": ["node"], "node": ">=18" } } }
user-invocable: true
---

# You’re being designed (scroll → log → steer)

**Template (five equal segments; list exact seconds for the chosen `duration`, e.g. 10 → 2s each, 15 → 3s each):**

- **Segment 1** — *YOU THINK YOU’RE SCROLLING* (or *YOU’RE NOT REALLY CHOOSING*).
- **Segment 2** — *THE FEED IS SCROLLING YOU* (or equivalent flip).
- **Segment 3** — *EVERY PAUSE GETS LOGGED*.
- **Segment 4** — *LAYOUT NUDGES YOU*.
- **Segment 5** — *THEY STEER WHAT YOU SEE*.

User may **swap wording** but **must keep five windows** unless they explicitly compress (then show **full** custom schedule in confirmation). Default **`duration`** is **10** when unspecified.

**Dependencies:** `WERYAI_API_KEY` + Node.js 18+. **`{baseDir}/scripts/video_gen.js`** + **[`WERYAI_VIDEO_API.md`](resources/WERYAI_VIDEO_API.md)**. **No other Cursor skills required.**

## Prerequisites

- `WERYAI_API_KEY` **must be set**; Node **18+**; `https` images only.
- Non-empty `model`.

## Security, secrets, and API hosts

- **`WERYAI_API_KEY`**: Secret; **`requires.env`** / **`primaryEnv`**.
- **API hosts** fixed in `video_gen.js`.

## Prompt expansion (mandatory)

- **Duration:** Default **10**; **5** or **15** when allowed and requested. For **five equal beats**, each caption span = **`duration / 5`** seconds (state numeric ranges explicitly in the prompt).
- **Timeline scaling:** If merging to fewer than five lines, list **new non-overlapping** windows in the confirmation table.

**Visuals:** Thumb on glass, **tiles exploding** into **data streams**, **recommendation grid**, **heatmap vibe**, **dark mode neon** accents, **glitch** tastefully; **hook in the first segment** must be **visually loud**.

**Typography:** Bold sans, white + black outline, lower third, **no overlap** between the five lines.

**Motion:** **Continuous**—scroll inertia, parallax UI, particles.

**Audio:** Sub pulse, digital risers if `generate_audio` true.

**Negatives (Kling):** illegible HUD text, watermark, crowded captions.

**Language:** **English** on screen unless user requests otherwise.

**Confirmation:** Full expanded `prompt` with **explicit non-overlapping second ranges** for all five lines (derive from `duration`).

### Niche checklist

- Reads as **critique of systems**, not attacks on **named individuals**.
- Avoid implying **illegal surveillance** claims unless user explicitly frames fiction.

## Workflow

1. Text / image / multi-image (**SEEDANCE_2_0**, ≤3).
2. Collect optional **wording tweaks**; default to template lines if user says “use default.”
3. Expand → validate → confirm → `wait`.
4. **`[Video](url)`** only for links.

## CLI reference

~~~sh
node {baseDir}/scripts/video_gen.js wait --json '{"model":"KLING_V3_0_PRO","prompt":"…","duration":10,"aspect_ratio":"9:16","generate_audio":true,"negative_prompt":"illegible text, watermark, garbled captions"}'
node {baseDir}/scripts/video_gen.js wait --json '{"model":"SEEDANCE_2_0","prompt":"…","duration":10,"aspect_ratio":"9:16","resolution":"720p","generate_audio":true}'
~~~

**Full reference:** **[`WERYAI_VIDEO_API.md`](resources/WERYAI_VIDEO_API.md)**.

## Definition of done

**[Video](url)** or error; **five** timed English lines present in `prompt`, with **numeric second ranges** matching the chosen **`duration`**.

## Boundaries (out of scope)

- Not factual **platform internals** documentation—**rhetorical short** only.
- **`resources/WERYAI_VIDEO_API.md`** for CLI; no `negative_prompt` on Seedance.
- **Multi-image** only **SEEDANCE_2_0**, max **3**.

### Example prompts

- `Default five-beat feed paranoia, cyberpunk UI`
- `Softer aesthetic: pastel social app, same five captions`
- `Screenshot-style image URL → animate with same subtitle schedule`
- `Parental controls aesthetic but same five-beat ‘who’s really in control’ lines`

---

## Model and API constraints (frozen for this skill)

### Text-to-video

| model_key | durations | aspect_ratios | resolutions | audio | negative_prompt | prompt limit |
|-----------|-----------|---------------|-------------|-------|-----------------|--------------|
| KLING_V3_0_PRO | 5, 10, 15 | 9:16, 1:1, 16:9 | *(omit)* | yes | yes | 2000 |
| KLING_V3_0_STA | 5, 10, 15 | 9:16, 1:1, 16:9 | *(omit)* | yes | yes | 2000 |
| SEEDANCE_2_0 | 5, 10, 15 | 9:16, 1:1, 16:9 | 480p, 720p | yes | no | 2000 |

### Image-to-video

| model_key | durations | aspect_ratios | resolutions | audio | negative_prompt | image slots |
|-----------|-----------|---------------|-------------|-------|-----------------|-------------|
| KLING_V3_0_PRO | 5, 10, 15 | 9:16, 16:9, 1:1 | *(omit)* | yes | yes | single `image` |
| KLING_V3_0_STA | 5, 10, 15 | 9:16, 16:9, 1:1 | *(omit)* | yes | yes | single `image` |
| SEEDANCE_2_0 | 5, 10, 15 | 9:16, 1:1, 16:9 | 480p, 720p | yes | no | up to **3** `images` |

## Recommended models

| Tier | model_key | Default duration |
|------|-----------|------------------|
| ⭐ Best | KLING_V3_0_PRO | 10 |
| 👍 Good | KLING_V3_0_STA | 10 |
| ⚡ Fast | SEEDANCE_2_0 | 10 (`resolution`: **720p**) |

## Default parameters

| Field | Value |
|-------|--------|
| aspect_ratio | 9:16 |
| duration | 10 |
| generate_audio | true |
| resolution | 720p (Seedance) |
| negative_prompt | Kling: `illegible text, garbled captions, watermark, HUD clutter` |

## Text-to-video (primary)

Default **five-line** schedule unless user overrides with a written table.

## Image-to-video (optional)

Phone UI still → **animate** with parallax + same captions.

## Tips

- First **2s** should **sync a hard cut** to the first caption.
- Shorter words survive model text rendering better.

> Packaged as **`feed-designs-you-video-gen`**.
