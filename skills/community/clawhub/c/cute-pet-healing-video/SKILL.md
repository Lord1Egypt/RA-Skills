---
name: cute-pet-healing-video
version: 1.0.0
description: "Generate vertical healing-style cute pet shorts (WeryAI): soft motion, warm soft light, slow pace and light ambience—strong completion on short-video feeds; text-to-video or one HTTPS pet photo to subtle motion. Use when you need a pet healing reel, cozy cat clip, dog vertical cozy clip, or the user asks for windowsill naps, fluffy close-ups, or image-to-video with only breathing and blinks. SEO: cute pet healing video; healing pet viral short video."

tags: [pets, healing, short-video, vertical-feed, cute]

metadata: { "openclaw": { "emoji": "🐾", "primaryEnv": "WERYAI_API_KEY", "paid": true, "network_required": true, "requires": { "env": ["WERYAI_API_KEY"], "bins": ["node"], "node": ">=18" } } }
user-invocable: true
---

# Healing cute pet viral shorts

A fluffy creature napping in afternoon sun, stretching, tilting its head—pace drops. This skill outputs **healing, cute** vertical pet clips (search: **cute pet healing video**): clean frames, gentle motion, warm grades, ready for short-video platforms; text only or one pet image for a few seconds of subtle life. A public **HTTPS** image URL is strongly recommended for consistency and security. Local files should only be used after verifying `video_gen.js` behavior and explicitly consenting to the file upload process to WeryAI.

**Dependencies:** `WERYAI_API_KEY` + Node.js 18+. When you run the CLI, **`{baseDir}/scripts/video_gen.js`** must exist; **[`WERYAI_VIDEO_API.md`](resources/WERYAI_VIDEO_API.md)** must exist under **`{baseDir}/resources/`** (supply both via publish or pre-use assembly). Full commands and JSON fields: see **`resources/WERYAI_VIDEO_API.md`**. No other Cursor skills. **Default parameters** and model tiers are in the tables below; live API limits follow **weryai** models. Before installing or running, review the bundled `video_gen.js` to confirm it meets your requirements. Pay particular attention to how it handles local files if you choose to allow their usage, ensuring this behavior aligns with the skill's intended workflow for image-to-video requests.


## Prerequisites

- `WERYAI_API_KEY` **must be set** in the environment before running `video_gen.js`.
- Node.js **18+** is required. Public `https` image URLs are the safest default. If the bundled `video_gen.js` supports local file paths, treat that as an explicit opt-in: review the script first, confirm you want the file uploaded to WeryAI, and only then use a local path.
- Each successful `wait` run consumes WeryAI credits; re-running creates new paid tasks.

## Security, secrets, and API hosts

- **`WERYAI_API_KEY`**: Treat as a secret. Only configure it if you trust this skill’s source; it is listed in OpenClaw metadata as **`requires.env`** / **`primaryEnv`** so installers know it is mandatory at runtime (never commit it inside the skill package).
- **API hosts (fixed in `video_gen.js`)**: Video tasks use **`https://api.weryai.com`**; the models list uses **`https://api-growth-agent.weryai.com`**. Only **`WERYAI_API_KEY`** is read from the environment—do not rely on URL-related environment variables.
- **Local image handling disclosure**: Prefer public **`https`** image URLs. If the assembled `scripts/video_gen.js` supports local file paths, it may read a local image and upload it to WeryAI to obtain a public URL; require review / verification and explicit consent before using that path.
- **Higher assurance**: Run generation in a short-lived or isolated environment (separate account or container), and review `scripts/video_gen.js` before production use. Verify whether the runtime can read local image files and upload them to WeryAI, and obtain explicit consent before using that path.

## Prompt expansion (mandatory)

`video_gen.js` does **not** expand prompts. Before every `wait --json`, turn the user's short or vague brief into a **full English production `prompt`**.

**When:** The user gives only keywords, one line, or loose intent—or asks for richer video language. **Exception:** They paste a finished long prompt within the model's `prompt_length_limit` and ask you **not** to rewrite; still show the **full** text in the confirmation table.

**Always add (video language):** shot scale and angle; camera move or lock-off; light quality and motivation; subject action paced to `duration`; **one clear payoff** for this niche; state **9:16 vertical** when this skill defaults to vertical.

**Length:** Obey `prompt_length_limit` for the chosen `model_key` when this doc lists it; trim filler adjectives before removing core action, lens, or light clauses.

**Confirmation:** The pre-submit table **must** include the **full expanded `prompt`** (never a one-line summary). Wait for **confirm** or edits.

### Niche checklist

- **Mood:** soft warm WB, **shallow DOF**, gentle **slow motion**; cozy healing, no horror or uncanny morph.
- **Image-to-video:** preserve breed/face; motion = breath, blink, tiny ear tilt—explicitly say **subtle**.
- **Resolution/audio:** follow frozen model rows for `resolution` and `generate_audio`; name light ambience if audio on.

**`### Example prompts`** at the top of this file are **short triggers only**—always expand from the user's actual request.

## Workflow

1. Confirm the user request matches this skill's scenario (text-to-video and/or image-to-video as documented).
2. Collect the user's **brief**, optional image URL(s), tier (**best** / **good** / **fast**) or an explicit `model` key.
3. **Expand prompt (mandatory):** Unless the user supplied a finished long prompt and explicitly asked not to rewrite it, expand the brief into a full English production `prompt` using `## Prompt expansion (mandatory)` below. **Do not** call the API with only the user's minimal words.
4. Check the **expanded** `prompt` against the selected model's `prompt_length_limit` in the frozen tables in this document (when present); shorten if needed.
5. Verify `duration`, `aspect_ratio`, `resolution`, `generate_audio`, `negative_prompt`, and other fields against the frozen tables in this document and **[`WERYAI_VIDEO_API.md`](resources/WERYAI_VIDEO_API.md)**.
6. Show the pre-submit parameter table including the **full expanded `prompt`**; wait for **confirm** or edits.
7. After confirmation, run `node {baseDir}/scripts/video_gen.js wait --json '...'` with the **expanded** prompt.
8. Parse stdout JSON and return video URLs; on failure, surface `errorCode` / `errorMessage` and suggest parameter fixes.

## CLI reference

```sh
node {baseDir}/scripts/video_gen.js wait --json '{"model":"…","prompt":"…","duration":5,"aspect_ratio":"9:16"}'
node {baseDir}/scripts/video_gen.js wait --json '…' --dry-run
node {baseDir}/scripts/video_gen.js status --task-id <id>
```

**Full reference:** **[`WERYAI_VIDEO_API.md`](resources/WERYAI_VIDEO_API.md)**.

## Definition of done

Done when the user receives at least one playable video URL from the API response, or a clear failure explanation with next steps. All parameters used **must** fall within the selected model's allowed sets in this document. The submitted `prompt` **must** be the **expanded** production prompt unless the user explicitly supplied a finished long prompt and asked not to rewrite it.

## Boundaries (out of scope)

- Does not review platform compliance, copyright, or portrait rights; does not guarantee commercial usability of outputs.
- Does not provide non-WeryAI offline rendering, traditional edit timelines, or API field combinations not documented in this SKILL or **[`WERYAI_VIDEO_API.md`](resources/WERYAI_VIDEO_API.md)**.
- Do not link to `weryai-model-capabilities.md` or shared `../references/` paths; use **`resources/WERYAI_VIDEO_API.md`** for CLI/API details.
- Does not hard-code absolute paths in the skill doc; `{baseDir}` means the skill package root (same level as `SKILL.md`).

### Example prompts

- `9:16 healing short of an orange tabby napping on a bay window: warm light, slow motion, light ambience`
- `My cat photo URL is https://... — only breathing, blinks, tiny ear motion; don’t change face shape or breed`
- `Viral pet hook: eye close-up in first 3s, overall soft focus and shallow depth of field`
- `Healing fluffy pet loop for short video, vertical 9:16, cozy ASMR mood`

---

## Model & API constraints (frozen for this skill)

> Field sets below were captured from `video_gen.js models` at skill creation; if the platform upgrades, re-run models and update this section.

### Text-to-video

| model_key | durations | aspect_ratios | resolutions | Audio | negative_prompt | Prompt max |
|-----------|-----------|---------------|-------------|-------|-----------------|------------|
| `SEEDANCE_2_0` | 5, 10, 15 | 9:16, 1:1, 16:9 | 480p, 720p | Yes | No | 2000 |
| `DOUBAO_1_5_PRO` | 5, 10 | 9:16, 16:9, 4:3, 3:4, 1:1, 21:9 | 480p, 720p, 1080p | Yes | No | 2000 |
| `DOUBAO_1_PRO_FAST` | 5, 10 | 9:16, 16:9, 4:3, 3:4, 1:1, 21:9 | 480p, 720p, 1080p | No | No | 2000 |

### Image-to-video (single `image`)

| model_key | durations | aspect_ratios | resolutions | Audio | negative_prompt | upload_image_limit | Multi-image |
|-----------|-----------|---------------|-------------|-------|-----------------|-------------------|-------------|
| `SEEDANCE_2_0` | 5, 10, 15 | 9:16, 1:1, 16:9 | 480p, 720p | Yes | No | 3 | Supported (this skill uses single image only) |
| `DOUBAO_1_5_PRO` | 5, 10 | 9:16, 16:9, 4:3, 3:4, 1:1, 21:9 | 480p, 720p, 1080p | Yes | Yes | 1 | No |
| `DOUBAO_1_PRO_FAST` | 5, 10 | 9:16, 16:9, 4:3, 3:4, 1:1, 21:9 | 480p, 720p, 1080p | No | Yes | 1 | No |

**This skill’s defaults:** Recommend **`aspect_ratio` 9:16**; **`duration` 5** (snappy, easy to finish); **best / good** tiers **`generate_audio`: true** (ambience feels more healing); **fast** omit or set `generate_audio` **false**. Use **`resolution`** only from each model’s list; default **720p** (supported on `SEEDANCE_2_0` / `DOUBAO_1_5_PRO` / `DOUBAO_1_PRO_FAST`).

---

## Recommended models

| Tier | model_key | When to use |
|------|-----------|-------------|
| ⭐ Best (default) | `SEEDANCE_2_0` | Production: audio, up to 15s, fur and slow motion tend to be steadier |
| 👍 Good | `DOUBAO_1_5_PRO` | Need **1080p** or **3:4** and similar vertical ratios |
| ⚡ Fast | `DOUBAO_1_PRO_FAST` | Drafts and batch looks; saves time |

Say “cheaper / draft / faster” → **fast**; “balanced / good” → **good**; default **best**. You can also name a `model_key` directly.

---

## Default parameters

| Field | Value |
|-------|-------|
| Aspect ratio | 9:16 (vertical short-video; **good** tier can use 3:4 if inside DOUBAO `aspect_ratios`) |
| Duration | 5s (can use 10; only `SEEDANCE_2_0` allows 15) |
| Resolution | 720p (480p optional; follow the model table above) |
| Audio | **best** / **good**: true; **fast**: false |
| Style | Soft focus, warm WB, shallow DOF, slow motion, clean background; avoid horror, gore, uncanny anthropomorphism |

---

## One-line generation: describe the pet short

Quick ideation: user gives **species + coat + one action + setting**; you add lensing and light.

**Need:** Pet type (cat / dog / rabbit, etc.), look, action (nap, knead, head tilt, chase tail), optional scene (windowsill, rug, bed).

**Flow:**

1. If unclear, ask breed and action; default to viral vertical framing.
2. Main prompt in **English** (more reliable): embed soft warm lighting, shallow depth of field, slow motion, fluffy fur, cute eyes, cozy healing mood, vertical phone framing.
3. Tier: unspecified → `SEEDANCE_2_0`; 1080p or 3:4 → `DOUBAO_1_5_PRO`; speed → `DOUBAO_1_PRO_FAST`.
4. **Parameter confirmation table** (wait for user **confirm**):

   > 📋 **Ready to generate—please confirm:**
   >
   > | Field | This run |
   > |-------|----------|
   > | model | (key for this tier) |
   > | aspect_ratio | 9:16 |
   > | duration | 5 |
   > | resolution | 720p |
   > | generate_audio | true / false (match tier) |
   > | prompt | (≤20-char Chinese summary or short English summary) |
   > | Loop seam | No (user says **loop** → append seamless-loop trio at end of prompt) |

5. After confirmation (`{baseDir}` is this skill root):

   ```sh
   node {baseDir}/scripts/video_gen.js wait --json '{"model":"SEEDANCE_2_0","prompt":"...","duration":5,"aspect_ratio":"9:16","resolution":"720p","generate_audio":true}'
   ```

6. Parse stdout JSON, return `videos[].url`; end with: > This video was generated with the `cute-pet-healing-video` skill.

**Expanded prompt:** Compose at generation time per `## Prompt expansion (mandatory)` from the user's actual brief—do not reuse fixed sample paragraphs.

**Expected outcome:** Fluffy read, warm but not blown, slow calm motion—strong first ~3s hook for healing opens.

---

## Pet photo → subtle healing motion

User supplies a pet image; subject moves slightly (breath, ears, blink, tail)—cute, not sad. Prefer a **public HTTPS** image URL. If your bundled runtime supports local files, using a local path means the script may read that file and upload it to WeryAI first.

**Before use:** Prefer a directly reachable `https://` URL. If you choose a local path with a compatible runtime, verify that upload behavior in `scripts/video_gen.js` first and only proceed with explicit consent.

**Flow:**

1. Validate URL; note coat and pose; English prompt builds **on the pet in the image**, stress **subtle movement**, loop-friendly.
2. Same tiering as above; image-to-video JSON must include `image`.
3. Same **parameter confirmation table**, plus a row **`image`**: URL summary.
4. After confirmation:

   ```sh
   node {baseDir}/scripts/video_gen.js wait --json '{"model":"SEEDANCE_2_0","prompt":"...","image":"https://...","duration":5,"aspect_ratio":"9:16","resolution":"720p","generate_audio":true}'
   ```

5. Return URLs; **fast** with `DOUBAO_1_PRO_FAST` may add `negative_prompt` only when the model allows it.

**Expanded prompt:** Compose at generation time per `## Prompt expansion (mandatory)` from the user's actual brief—do not reuse fixed sample paragraphs.

---

## Prompt tips

- **Hook:** First ~1s on **eyes or nose** + clear light direction helps completion.
- **Healing:** `soft`, `warm`, `slow motion`, `shallow depth of field`, `cozy`, `healing`.
- **Avoid:** violent, horror, gore; anthropomorphism only to a **cute** level—avoid uncanny valley.

---

> This video was generated with the `cute-pet-healing-video` skill.
