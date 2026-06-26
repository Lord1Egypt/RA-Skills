---
name: art-process-video
version: 1.0.0
description: "Generate vertical short videos of painting / retouching creative process (WeryAI): layered progression from sketch to finish—illustration coloring, posters, avatars, typography, and speedpaint-style storytelling. Use when you need art process timelapse, painting-process video, design creation reel, or the user asks for a full journey from line art to color. SEO: art process video; painting creative process video generation."

tags: [painting, design, process, creation, art, healing, short-video]

metadata: { "openclaw": { "emoji": "🎨", "primaryEnv": "WERYAI_API_KEY", "paid": true, "network_required": true, "requires": { "env": ["WERYAI_API_KEY"], "bins": ["node"], "node": ">=18" } } }
user-invocable: true
---

# Art process video generation

Time-compressed journey from pencil sketch to final piece—lines grow denser, color goes from none to full, detail stacks layer by layer, the last stroke lands, and the finished work is revealed. The process *is* the content; no on-screen copy needed. Fits illustrators, designers, and art accounts.

**Dependencies**: `scripts/video_gen.js` in this directory + `WERYAI_API_KEY` in the environment + Node.js 18+. No dependency on other Cursor skills.


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

- **Process arc:** sketch → base color → detail → **final frame** much richer than the opening blank or rough lines.
- **Medium & subject:** name tablet/paper/watercolor and what is being painted or designed; use **time-lapse / speed-ramp** language when `duration` is short.
- **Camera & light:** top-down, eye-level screen, or macro brush; motivated desk/canvas/monitor light; show stroke motion and rising saturation.

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

- `Character illustration on a tablet from pencil sketch to full color, vertical accelerated process`
- `Use this line-art image to animate gradual color, light, and shadow until the final piece`
- `Poster typography process from grid to final logotype, art-account style`
- `Digital painting process 9:16, layers build up, satisfying brush strokes`

---

## Default parameters

| Field | Value |
|-------|-------|
| Model | KLING_V3_0_PRO |
| Aspect ratio | 9:16 (fixed) |
| Duration | 10 seconds (`duration`: 10—enough time to show layered progression) |
| Audio | Off |
| Visual style | Top-down or eye-level close-up; canvas or tablet in frame; clear brush motion; color fills progressively; time-compressed timeline |

> **API validity (default `KLING_V3_0_PRO`):** Text-to-video `duration` only **5 / 10 / 15**; `aspect_ratio` only **9:16, 1:1, 16:9**. Image-to-video `aspect_ratio` only **9:16, 16:9, 1:1**. **No `resolution` field—do not send it.** For **fast** tier with VEO: text-to-video **`VEO_3_1_FAST`**, image-to-video **`CHATBOT_VEO_3_1_FAST`**, with `duration` **fixed at 8**, `aspect_ratio` only **9:16** or **16:9**. When switching `model_key`, follow the allowed sets in this section’s model/API constraints and the API validity note above; do not send `resolution` to models that do not support it.

---

## Full creative process: sketch to finish

**Purpose:** Show one illustration or design from blank to done. Pace is time-lapse compression: stroke density rises with progress, saturation climbs from low to high, and the final frame should feel dramatically richer than the starting blank.

**The user should provide:**
- Subject (bear / cat / bunny / or a theme like “forest spirit,” “cyber girl”)
- Style (dreamy watercolor / line-art B&W / thick oil-like paint / flat design / cyberpunk illustration)
- Medium (paper + pencil / tablet + stylus / watercolor paper / digital screen)

**Generation flow:**
1. Confirm subject, style, and medium.
2. Build the prompt in three phases: light sketch lines → base color blocking → detail polish and finish, with clear visual beats per phase.
3. If parameters are unspecified, show defaults and wait for confirmation:
**You must show all parameters in a table and wait for explicit user confirmation before submitting:**

   > 📋 **Ready to generate—please confirm:**
   >
   > | Parameter | This run | Notes |
   > |-----------|----------|-------|
   > | `model` | `KLING_V3_0_PRO` | Best tier default; say “cheap / draft / fast” → `WAN_2_6`; say “balanced” → `KLING_V3_0_STA`; or name a model directly |
   > | `aspect_ratio` | `9:16` | Default KLING: 9:16, 1:1, 16:9 only; if you change model, check that model’s `aspect_ratios` in the table |
   > | `duration` | `10s` | KLING family: 5 / 10 / 15; VEO fast: duration 8 only |
   > | `generate_audio` | `false` | Whether to auto-generate audio |
   > | `prompt` | **Full expanded English prompt** (entire text for this run) | Revise before confirm |
   > | `Loop seam` | No | Reply “loop” to enable seamless loop |
   >
   > Reply **“confirm”** to start, or list what to change.
4. After confirmation, run in the terminal (`{baseDir}` is the skill root):

   ```sh
   node {baseDir}/scripts/video_gen.js wait --json '{"model":"（model from confirmation table）","prompt":"（full expanded English prompt）","aspect_ratio":"9:16","duration":10,"generate_audio":false}'
   ```

   `aspect_ratio`, `duration`, `generate_audio`, and `model` must match the table; add `resolution` only if the model supports it. Parse stdout `videos` for URLs.

**Parameter configuration:**

| Field | Value |
|-------|-------|
| model | KLING_V3_0_PRO |
| aspect_ratio | 9:16 |
| duration | 10 |
| generate_audio | false |

**Expanded prompt:** Compose at generation time per `## Prompt expansion (mandatory)` from the user's actual brief—do not reuse fixed sample paragraphs.

**Expected outcome:** Clear three-beat rhythm (blocking color, detail pass, final reveal), rising visual density from sparse to rich, final frame clearly stronger than the start—good for process content on art accounts.

---

## Single “brushstroke” hero moment

Focus on one stunning beat: one highlight dot makes the eye “wake up,” a gradient snaps into place, one line closes the piece—better for punchy shorts than a full process.

Say which “one stroke” moment to show; build the prompt directly:

> Parameters are shown before generation; wait for confirmation before submit.

**Expanded prompt:** Compose at generation time per `## Prompt expansion (mandatory)` from the user's actual brief—do not reuse fixed sample paragraphs.

---

## Prompt tips

**Process rhythm:** `layer by layer`, `stage by stage with visible progress`, `time-lapse with speed ramp at details phase`, `complexity builds frame by frame`

**Finish impact:** `final reveal is dramatically more complex than the starting blank`, `the completed piece has gallery-quality depth`, `jaw-dropping transformation from empty canvas`

**Brush feel:** `stylus catches tablet light`, `pencil line weight variation visible`, `watercolor bleeds naturally at paper texture`, `digital brush softness in layered opacity`

> **Note:** Ten seconds is already tight for a full process; say **time-lapse compression** in the prompt so the model treats it as accelerated display, not real-time drawing speed.
