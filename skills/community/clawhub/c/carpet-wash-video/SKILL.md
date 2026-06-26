---
name: carpet-wash-video
version: 1.0.0
description: "Generate satisfying vertical carpet deep-clean shorts (WeryAI): text-to-video or dirty rug photo to rinse, grime runoff, and fiber revival. Use when you need carpet cleaning satisfying video, stain removal rinse, dirty-to-clean reveal, or users ask for grime line, fluffy pile comeback, before/after contrast."

tags: [cleaning, satisfying, asmr, short-video, vertical]

metadata: { "openclaw": { "emoji": "🧹", "primaryEnv": "WERYAI_API_KEY", "paid": true, "network_required": true, "requires": { "env": ["WERYAI_API_KEY"], "bins": ["node"], "node": ">=18" } } }
user-invocable: true
---

# Carpet wash & restore videos

For cleaning / satisfying creators: pressure rinse, brush agitation, dirty water running out, fibers standing up again—strong before/after and ASMR wash sounds. One prompt or one dirty carpet photo.

**Dependencies:** `scripts/video_gen.js` + `WERYAI_API_KEY` + Node.js 18+.

## Prerequisites

- `WERYAI_API_KEY` **must be set**.
- Node.js **18+**; images **must** be `https` URLs.

## Security, secrets, and API hosts

- **`WERYAI_API_KEY`**: Treat as a secret. Only configure it if you trust this skill's source; it is listed in OpenClaw metadata as **`requires.env`** / **`primaryEnv`** so installers know it is mandatory at runtime (never commit it inside the skill package).
- **Optional URL overrides** (`WERYAI_BASE_URL`, `WERYAI_MODELS_BASE_URL`): `video_gen.js` defaults to **`https://api.weryai.com`** and **`https://api-growth-agent.weryai.com`**. Overrides are intended for testing or approved alternate endpoints. If these variables are set in your environment, confirm they point to hosts you trust—otherwise prompts, images, and your bearer token could be sent elsewhere.
- **Higher assurance**: Run generation in a short-lived or isolated environment (separate account or container), and review `scripts/video_gen.js` (HTTPS submit + poll loop) before production use.


## Prompt expansion (mandatory)

`video_gen.js` does **not** expand prompts. Before every `wait --json`, turn the user's short or vague brief into a **full English production `prompt`**.

**When:** The user gives only keywords, one line, or loose intent—or asks for richer video language. **Exception:** They paste a finished long prompt within the model's `prompt_length_limit` and ask you **not** to rewrite; still show the **full** text in the confirmation table.

**Always add (video language):** shot scale and angle; camera move or lock-off; light quality and motivation; subject action paced to `duration`; **one clear payoff** for this niche; state **9:16 vertical** when this skill defaults to vertical.

**Length:** Obey `prompt_length_limit` for the chosen `model_key` when this doc lists it; trim filler adjectives before removing core action, lens, or light clauses.

**Confirmation:** The pre-submit table **must** include the **full expanded `prompt`** (never a one-line summary). Wait for **confirm** or edits.

### Niche checklist

- **Wash physics:** water/foam migration, **dirty runoff**, fiber lift, before/after color stripe or patch.
- **Camera:** top-down or low side angle; **slow motion** on squeeze or extractor pass; ASMR-forward if audio on.
- **Stains:** tie language to user rug type (mud, pet, grey traffic) and method (pressure, brush, steam).

**`### Example prompts`** at the top of this file are **short triggers only**—always expand from the user's actual request.

## Workflow

1. Confirm scenario (text-to-video and/or image-to-video as documented).
2. Collect the user's **brief**, optional `https` image URL, tier (**best** / **good** / **fast**) or explicit `model`.
3. **Expand prompt (mandatory):** Unless the user supplied a finished long prompt and asked not to rewrite, expand the brief with full shot, light, wash physics, and audio cues per `## Prompt expansion (mandatory)`. **Do not** submit a one-liner.
4. Check the **expanded** `prompt` against `prompt_length_limit` if listed for the model; trim if needed.
5. Verify `duration`, `aspect_ratio`, `generate_audio`, and other fields against this doc.
6. Show the confirmation table with the **full expanded `prompt`**; wait for **confirm** or edits.
7. After confirmation, run `node {baseDir}/scripts/video_gen.js wait --json '...'` with the **expanded** prompt.
8. Return playable URL(s) or clear error guidance.

## CLI reference

```sh
node {baseDir}/scripts/video_gen.js wait --json '{"model":"…","prompt":"…","duration":5,"aspect_ratio":"9:16"}'
node {baseDir}/scripts/video_gen.js wait --json '…' --dry-run
node {baseDir}/scripts/video_gen.js status --task-id <id>
```

## Definition of done

Playable URL(s) or clear failure; parameters within model limits. The submitted `prompt` **must** be the **expanded** production prompt unless the user explicitly supplied a finished long prompt and asked not to rewrite it.

## Boundaries (out of scope)

- No legal/commercial guarantees; no offline editing stacks; `{baseDir}` only—no absolute paths.

### Example prompts

- `Filthy living-room rug, pressure washer leaves a clean stripe, vertical satisfying`
- `From this moldy carpet photo—rinse and dark water pouring off`
- `OCD clean macro: pile goes grey to bright, foam and squeeze moment`
- `Satisfying carpet deep clean 9:16, dirty-to-clean reveal line`

---

## Default parameters

| Field | Value |
|-------|--------|
| Model | KLING_V3_0_PRO |
| Aspect | 9:16 |
| Duration | 5 (short hook) |
| Audio | On (brush, water, squeeze ASMR) |
| Look | Top-down close, soft light, extreme before/after color, slow grime flow, minimal background |

> **API validity (`KLING_V3_0_PRO`):** Text: `duration` **5 / 10 / 15**, `aspect_ratio` **9:16, 1:1, 16:9**; image: `aspect_ratio` **9:16, 16:9, 1:1**; **no `resolution`.** VEO fast: **`VEO_3_1_FAST`** / **`CHATBOT_VEO_3_1_FAST`**, `duration` **8**, `aspect_ratio` **9:16** or **16:9**. Other keys: follow tables here.

---

## Text-to-video: wash process

**User provides:** rug type (short pile / shag / weave / vintage / pet mat), stain type (overall grey / embedded fur / mud spot / drink / years of dust), optional method (pressure / brush / steam / extractor).

**Flow:** collect → build English prompt (runoff, color return, fiber lift) → run:

```sh
node {baseDir}/scripts/video_gen.js wait --json '{"model":"KLING_V3_0_PRO","prompt":"(English prompt)","aspect_ratio":"9:16","duration":5,"generate_audio":true}'
```

**Parameters:** model KLING_V3_0_PRO, 9:16, 5, generate_audio true.

**Expanded prompt:** Build per `## Prompt expansion (mandatory)` from the user's rug/stain brief; do not paste fixed samples.

**Expected:** Visible dirty water, strong color bounce-back, ASMR-friendly audio.

---

## Image-to-video: clean the photo rug

**User provides:** `https` image URL + effect (pressure / brush / extract / steam).

**Flow:** validate URL → prompt matched to stains in image →

```sh
node {baseDir}/scripts/video_gen.js wait --json '{"model":"KLING_V3_0_PRO","prompt":"(English)","image":"(URL)","aspect_ratio":"9:16","duration":5,"generate_audio":true}'
```

**Expected:** Grime matches photo; true color emerges; pattern continuity.

---

## Prompt blocks

**Grime:** `thick dark water flows outward`, `murky brown runoff cascades`, `grime releases in satisfying rivulets`

**Color return:** `vivid original color emerges beneath`, `saturated hues pop`, `before-after color contrast in single frame`

**Pile:** `fibers lift and separate`, `pile stands upright after cleaning`, `fluffy texture restored`

**Sound:** `ASMR scrubbing`, `pressure washer hiss`, `wet squeegee drag`

> Upload local shots to a public host first; API needs reachable HTTPS.
