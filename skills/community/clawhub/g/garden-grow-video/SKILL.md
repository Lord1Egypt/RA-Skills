---
name: garden-grow-video
version: 1.0.0
description: "Generate vertical short videos of gardening and plant growth (WeryAI): seed germination, bloom and fruit, succulents, mushrooms, and time-lapse growth stories. Use when you need plant growth timelapse, cozy gardening video, cute character gardener clip, or the user asks for bunny planting strawberries, balcony tomatoes, or succulents filling a pot. SEO: garden grow video; gardening growth video generation."

tags: [gardening, healing, growth, nature, lifestyle, short-video]

metadata: { "openclaw": { "emoji": "🌱", "primaryEnv": "WERYAI_API_KEY", "paid": true, "network_required": true, "requires": { "env": ["WERYAI_API_KEY"], "bins": ["node"], "node": ">=18" } } }
user-invocable: true
---

# Gardening & plant growth video generation

A seed in soil, roots reaching down, cotyledons breaking the surface, stems stretching day by day, buds swelling, a flower opening in sun—ten seconds can hold a whole life cycle; that’s the magic of timelapse. Bunny with strawberries, bear with succulents, cat with balcony tomatoes: growth *is* the plot.

**Dependencies**: `scripts/video_gen.js` in this directory + `WERYAI_API_KEY` + Node.js 18+. No dependency on other Cursor skills.


## Prerequisites

- `WERYAI_API_KEY` **must be set** in the environment before running `video_gen.js`.
- Node.js **18+** is required. Image inputs **must** be public `https` URLs (no local file paths).
- Each successful `wait` run consumes WeryAI credits; re-running creates new paid tasks.

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

- **Time language:** **time-lapse**, visible days/weeks compression, light angle or shadow drift for elapsed time.
- **Beats:** seed/sprout/leaf/flower/fruit as applicable; hands or paws optional; terracotta, soil, glass root views.
- **Payoff:** harvest, full bloom, or filled planter **clearer than start**.

**`### Example prompts`** at the top of this file are **short triggers only**—always expand from the user's actual request.

## Workflow

1. Confirm the user request matches this skill's scenario (text-to-video and/or image-to-video as documented).
2. Collect the user's **brief**, optional image URL(s), tier (**best** / **good** / **fast**) or an explicit `model` key.
3. **Expand prompt (mandatory):** Unless the user supplied a finished long prompt and explicitly asked not to rewrite it, expand the brief into a full English production `prompt` using `## Prompt expansion (mandatory)` below. **Do not** call the API with only the user's minimal words.
4. Check the **expanded** `prompt` against the selected model's `prompt_length_limit` in the frozen tables in this document (when present); shorten if needed.
5. Verify `duration`, `aspect_ratio`, `resolution`, `generate_audio`, `negative_prompt`, and other fields against the frozen tables and API notes in this SKILL.md.
6. Show the pre-submit parameter table including the **full expanded `prompt`**; wait for **confirm** or edits.
7. After confirmation, run `node {baseDir}/scripts/video_gen.js wait --json '...'` with the **expanded** prompt.
8. Parse stdout JSON and return video URLs; on failure, surface `errorCode` / `errorMessage` and suggest parameter fixes.

## CLI reference

```sh
node {baseDir}/scripts/video_gen.js wait --json '{"model":"…","prompt":"…","duration":5,"aspect_ratio":"9:16"}'
node {baseDir}/scripts/video_gen.js wait --json '…' --dry-run
node {baseDir}/scripts/video_gen.js status --task-id <id>
```

## Definition of done

Done when the user receives at least one playable video URL from the API response, or a clear failure explanation with next steps. All parameters used **must** fall within the selected model's allowed sets in this document. The submitted `prompt` **must** be the **expanded** production prompt unless the user explicitly supplied a finished long prompt and asked not to rewrite it.

## Boundaries (out of scope)

- Does not review platform compliance, copyright, or portrait rights; does not guarantee commercial usability of outputs.
- Does not provide non-WeryAI offline rendering, traditional edit timelines, or API field combinations not documented here.
- Does not hard-code absolute paths in the skill doc; `{baseDir}` means the skill package root (same level as `SKILL.md`).

### Example prompts

- `Bunny grows tomatoes on a balcony: seed to red fruit on the vine, vertical timelapse growth`
- `Use this succulent pot image: leaves plump and colors intensify over days`
- `Mushrooms from bag to harvest, healing natural light`
- `Cozy plant growth timelapse 9:16, window sunlight, cute animal gardener`

---

## Default parameters

| Field | Value |
|-------|-------|
| Model | KLING_V3_0_PRO |
| Aspect ratio | 9:16 (fixed) |
| Duration | 10 seconds (`duration`: 10—full growth arc) |
| Audio | Off |
| Visual style | Front medium or top-down; natural light (window sun); timelapse feel; light direction shifts over “days”; simple background (soil, terracotta, wood) |

> **API validity (default `KLING_V3_0_PRO`):** Text-to-video `duration` only **5 / 10 / 15**; `aspect_ratio` only **9:16, 1:1, 16:9**. Image-to-video `aspect_ratio` only **9:16, 16:9, 1:1**. **No `resolution` field—do not send it.** For **fast** tier with VEO: text-to-video **`VEO_3_1_FAST`**, image-to-video **`CHATBOT_VEO_3_1_FAST`**, with `duration` **fixed at 8**, `aspect_ratio` only **9:16** or **16:9**. When switching `model_key`, follow the allowed sets in this section’s model/API constraints and the API validity note above; do not send `resolution` to models that do not support it.

---

## Seed to sprout to flower and fruit

**Purpose:** Time-compressed growth from planting through a satisfying harvest or bloom. Hero beats: breaking soil and the final flower or fruit moment.

Describe the character and plant—no extra form:

e.g. “bunny grows strawberries” or “cat grows balcony tomatoes”—the skill fills in the full growth arc and visual detail.

Show parameters before generate:

> Generating with the parameters below—reply **confirm** or say what to change:
> - model: KLING_V3_0_PRO
> - aspect_ratio: 9:16
> - duration: 10
> - generate_audio: false
> - Loop seam: No (reply **loop** to enable; appends `seamless loop` to the prompt)

**Expanded prompt:** Compose at generation time per `## Prompt expansion (mandatory)` from the user's actual brief—do not reuse fixed sample paragraphs.

**Parameter configuration:**

| Field | Value |
|-------|-------|
| model | KLING_V3_0_PRO |
| aspect_ratio | 9:16 |
| duration | 10 |
| generate_audio | false |

**Expected outcome:** Clear time advance; sprouting and bloom/fruit as peaks; light cycles or angle shifts sell the passage of time; ending feels like a payoff.

---

## Microscopic growth close-ups

Single-plant life at extreme detail: roots in a clear vessel, bud-to-full-bloom timelapse, mushroom from spore stage to pickable—no long story, one magnified process.

Name the plant and stage; then generate:

**You must show all parameters in a table and wait for explicit user confirmation before submitting:**

   > 📋 **Ready to generate—please confirm:**
   >
   > | Parameter | This run | Notes |
   > |-----------|----------|-------|
   > | `model` | `KLING_V3_0_PRO` | Best default; say “cheap / draft / fast” → `KLING_V3_0_STA`; say “balanced” → `WAN_2_6`; or name a model |
   > | `aspect_ratio` | `9:16` | Default KLING: 9:16, 1:1, 16:9 |
   > | `duration` | `10s` | KLING: 5 / 10 / 15; VEO fast: 8 only |
   > | `generate_audio` | `false` | Whether to auto-generate audio |
   > | `prompt` | **Full expanded English prompt** (entire text for this run) | Revise before confirm |
   > | `Loop seam` | No | Reply “loop” for seamless loop |
   >
   > Reply **“confirm”** to start, or list what to change.

**Expanded prompt:** Compose at generation time per `## Prompt expansion (mandatory)` from the user's actual brief—do not reuse fixed sample paragraphs.

---

## Prompt tips

**Timelapse feel:** `time-lapse compression`, `days visible in seconds`, `light cycles through the sequence`, `daily shadows rotate revealing passage of time`

**Life beats:** `seedling breaks through soil surface`, `root tip emerges driven by gravity`, `flower petals open in slow motion`, `fruit swells and deepens in color`

**Texture:** `terracotta pot texture`, `soil granularity visible`, `glass-sided container reveals root system`, `morning window light on dew-covered leaves`

> **Note:** Say **`time-lapse`** explicitly or the model may output a static plant instead of growth. Adding **`light cycling`** or **`shadow angle changing`** strengthens the sense of elapsed time.
