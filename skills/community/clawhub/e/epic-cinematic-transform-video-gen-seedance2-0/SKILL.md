---
name: "epic-cinematic-transform-video-gen-seedance2.0"
version: 1.0.0
description: "Upscale ordinary beats into trailer-scale drama: anamorphic mood in vertical, bold contrast, heroic pacing—WeryAI Seedance 2.0 only. Use when you need hype reels, faux movie poster motion, or image-to-video with blockbuster lighting. SEO: epic cinematic video; trailer style short video."

tags: [cinematic, epic, trailer, drama, short-video, video-gen]

metadata: { "openclaw": { "emoji": "🎬", "primaryEnv": "WERYAI_API_KEY", "paid": true, "network_required": true, "requires": { "env": ["WERYAI_API_KEY"], "bins": ["node"], "node": ">=18" } } }
user-invocable: true
---

# Epic cinematic trailer style transform (Seedance 2.0)

**Blockbuster read in 9:16:** dramatic skies, volumetric god-rays, slow push-ins, percussive motion cuts implied in prompt, huge scale cues.

**Dependencies:** `WERYAI_API_KEY` + Node.js 18+. This skill uses **only** `SEEDANCE_2_0`. When you run the CLI, **`{baseDir}/scripts/video_gen.js`** must exist; **[`WERYAI_VIDEO_API.md`](resources/WERYAI_VIDEO_API.md)** must exist under **`{baseDir}/resources/`** (supply both via publish or pre-use assembly). Full commands and JSON fields: see **`resources/WERYAI_VIDEO_API.md`**. **No other Cursor skills required.**

## Prerequisites

- `WERYAI_API_KEY` **must be set** before running `video_gen.js`.
- Node.js **18+**; image inputs **must** be public `https` URLs (no local paths).
- **Model (caller / agent):** The bundled `video_gen.js` **requires** a non-empty `model` in JSON—if `model` is missing or blank, the CLI exits with **`MISSING_PARAM`** (no default model). The script **does not** enforce this skill's allowed model in code: you **must** set `"model":"SEEDANCE_2_0"` for this package and show it in the confirmation table before submit—see [`WERYAI_VIDEO_API.md`](resources/WERYAI_VIDEO_API.md) (`model` row).
- Each `wait` run may consume credits; re-run creates new paid tasks.

## Security, secrets, and API hosts

- **`WERYAI_API_KEY`**: Treat as a secret. Only configure it if you trust this skill's source; it is listed in OpenClaw metadata as **`requires.env`** / **`primaryEnv`** so installers know it is mandatory at runtime (never commit it inside the skill package).
- **API hosts (fixed in `video_gen.js`)**: Video tasks use **`https://api.weryai.com`**; the models list uses **`https://api-growth-agent.weryai.com`**. Child skills must not document or rely on URL environment-variable overrides—only **`WERYAI_API_KEY`** is read from the environment.
- **Higher assurance**: Run generation in a short-lived or isolated environment (separate account or container), and review `scripts/video_gen.js` (HTTPS submit + poll loop) before production use.

## Prompt expansion (mandatory)

`video_gen.js` does **not** expand prompts. Before every `wait --json`, turn the user's short or vague brief into a **full English production `prompt`** that **re-styles** the described event into this skill's look.

**When:** User input is short, vague, or missing cinematic detail. **Exception:** They supply a finished long prompt within **2000** characters and ask you **not** to rewrite—still show the **full** text in the confirmation table.

**Always add:** shot size and angle; camera move; lighting and color grade aligned to this skill; subject action paced to `duration`; **one clear payoff**; platform framing (**9:16** unless user chose another allowed ratio); if `generate_audio` is **true**, describe ambience / SFX in generic words (no copyrighted music references).

**Length:** Stay within **`prompt_length_limit` 2000** for `SEEDANCE_2_0`; trim adjectives before losing the core transformation beat.

**Confirmation:** The pre-submit table **must** include the **full expanded `prompt`**.

### Style transformation checklist

- **Lens grammar:** wide establishing → medium hero; subtle dolly in.
- **Light:** chiaroscuro, rim for silhouette reads, storm or golden hour motivation.
- **Trailer rhythm:** build–pause–hit within `duration` seconds.
- **Scale:** crowds implied, vast plates, foreground debris parallax.
- **Action:** destiny-weighted gestures, cape or coat motion—even on mundane tasks played epic.
- **Sound (if on):** braams, drums, whooshes—generic descriptors only.

**Fits:** Big moments, sports hype, product hero shots, mythic storytelling.

**`### Example prompts`** below are **richness targets only**—always derive from the user's actual brief.

## Workflow

1. Confirm the request matches this skill (text-to-video and/or single image-to-video).
2. Collect the user's **brief**, optional **`image`** URL, and tier (**best** / **good** / **fast**)—all map to **`SEEDANCE_2_0`** with different duration defaults (see **Recommended models**).
3. **Expand prompt (mandatory):** Unless the user opted out with a finished long prompt, expand using `## Prompt expansion (mandatory)`. **Do not** submit only the user's minimal words.
4. Validate **`model`** is **`SEEDANCE_2_0` only**; validate `duration`, `aspect_ratio`, `resolution`, `generate_audio` against the frozen tables.
5. Show the confirmation table with the **full expanded `prompt`**; wait for **confirm** or edits.
6. Run `node {baseDir}/scripts/video_gen.js wait --json '...'`.
7. Parse stdout JSON; return `videos` URLs or explain errors.
8. When presenting playable URLs to the user, use **Markdown inline links only** (e.g. `[Video](https://...)`). **Do not** wrap user-facing links in code fences.

## CLI reference

~~~sh
node {baseDir}/scripts/video_gen.js wait --json '{"model":"SEEDANCE_2_0","prompt":"…","duration":10,"aspect_ratio":"9:16","resolution":"720p","generate_audio":true}'
~~~

**Full reference:** **[`WERYAI_VIDEO_API.md`](resources/WERYAI_VIDEO_API.md)**.

## Definition of done

Done when the user gets at least one playable **[Video](url)**-style link, or a clear failure with next steps. Submitted `prompt` must be the **expanded** prompt unless the user explicitly opted out. **Never** use another `model_key` in this skill.

## Boundaries (out of scope)

- Do not use **any model other than `SEEDANCE_2_0`** for this package.
- Do not link to `weryai-model-capabilities.md` or shared `../references/` paths; use **`resources/WERYAI_VIDEO_API.md`** for CLI/API details.
- Do not use local file paths for `image`; never embed the secret value of `WERYAI_API_KEY` in files.
- Do not invent API fields; do not send `negative_prompt` (not supported for this model).
- Do not wrap user-facing playable URLs in Markdown code fences.

### Example prompts

- `Pouring water → treated like mythic libation, storm light, massive scale mist`
- `Opening a laptop → beam of light, dust particles, heroic low angle, 9:16`
- `HTTPS athlete still → slow epic zoom, stadium haze implied, dramatic rim`

---

## Model and API constraints (frozen for this skill)

> Derived from `node {baseDir}/scripts/video_gen.js models` alignment at authoring time; re-run `models` after platform upgrades. **This skill is locked to `SEEDANCE_2_0` only.**

### Text-to-video

| model_key | durations | aspect_ratios | resolutions | Audio | negative_prompt | prompt limit |
|-----------|-----------|---------------|-------------|-------|-----------------|---------------|
| `SEEDANCE_2_0` | 5, 10, 15 | 9:16, 1:1, 16:9 | 480p, 720p | Yes | No (do not send) | 2000 |

### Image-to-video (single `image`)

| model_key | durations | aspect_ratios | resolutions | Audio | negative_prompt | upload_image_limit |
|-----------|-----------|---------------|-------------|-------|-----------------|-------------------|
| `SEEDANCE_2_0` | 5, 10, 15 | 9:16, 1:1, 16:9 | 480p, 720p | Yes | No (do not send) | 3 |

---

## Recommended models

| Tier | model_key | Notes |
|------|-----------|-------|
| ⭐ Best (default) | `SEEDANCE_2_0` | Prefer **`duration` 10 or 15**, **`resolution` 720p**, **`generate_audio` true** for fullest mood |
| 👍 Good | `SEEDANCE_2_0` | Balanced: **`duration` 10**, **`resolution` 720p**, audio per user |
| ⚡ Fast | `SEEDANCE_2_0` | Snappy: **`duration` 5**, **`resolution` 480p** or **720p**, audio optional |

Tier only changes **duration / resolution / audio** defaults—**never** the model.

---

## Default parameters

| Field | Value |
|-------|--------|
| Model | `SEEDANCE_2_0` (fixed) |
| Aspect ratio | `9:16` |
| Duration | `10` (use `5` for punchy; `15` for slower ceremony) |
| Resolution | `720p` (`480p` allowed) |
| Audio | `true` unless user wants silent |

---

## Scenario: Text-to-video style transform

**Flow**

1. Capture the user's mundane event in one or two sentences.
2. Expand into English with the **Style transformation checklist**; keep identity generic unless user names a character.
3. Confirmation table → user **confirm**.
4. Execute:

~~~sh
node {baseDir}/scripts/video_gen.js wait --json '{"model":"SEEDANCE_2_0","prompt":"<expanded>","duration":10,"aspect_ratio":"9:16","resolution":"720p","generate_audio":true}'
~~~

5. Return `[Video](url)` links.

---

## Scenario: Image-to-video style transform

**Before use:** `image` must be `https://` and reachable.

1. Plan how the still **re-styles** in motion (props, light, environment) without breaking likeness if the user requests preservation.
2. Expand prompt; add `image` to the confirmation table.
3. After **confirm**:

~~~sh
node {baseDir}/scripts/video_gen.js wait --json '{"model":"SEEDANCE_2_0","prompt":"<expanded>","image":"https://…","duration":10,"aspect_ratio":"9:16","resolution":"720p","generate_audio":true}'
~~~

4. Return `[Video](url)` links.

---

## Loop seam (optional)

If the user asks for a **seamless loop**, append a short English trio at the **end** of the expanded prompt: `seamless loop`, `perfect loop`, `ends where it begins`—no separate API flag.

> Generated for skill `epic-cinematic-transform-video-gen-seedance2.0`.
