---
name: cake-decor-video
version: 1.0.0
description: "Generate vertical short videos of cake decorating and pastry finishing (WeryAI): frosting, piping, mirror glaze, and other high-aesthetic handmade beats. Use when you need a cake decorating reel, piping video, satisfying pastry clip, or the user asks for buttercream roses, gradient drip glaze, or anthropomorphic animals baking. SEO: cake decor video; cake decorating dessert video generation."

tags: [dessert, piping, healing, aesthetic, handmade, short-video]

metadata: { "openclaw": { "emoji": "🎂", "primaryEnv": "WERYAI_API_KEY", "paid": true, "network_required": true, "requires": { "env": ["WERYAI_API_KEY"], "bins": ["node"], "node": ">=18" } } }
user-invocable: true
---

# Cake decorating & dessert video generation

That one pass of the offset spatula—rough sides turning glass-smooth—is often the most satisfying frame. One rotation of the piping tip and you have a rose. Glaze flows top-down and the gradient spreads on the curve. Bear / bunny / cat doing the work: the sweet spot of the dessert niche is that handmade satisfaction.

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

- **Decor beats:** crumb coat → piping → toppings → **hero reveal**; macro sweet light; satisfying squeeze, drip, or spin.
- **Scale & texture:** frosting gloss, air bubbles, sprinkles; **9:16** portrait food framing.
- **Motion:** steady hand, turntable, or slow push on the final slice or full cake.

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

- `Bear making a cream cake: one spatula pass smooths the side, then pipe a rose, vertical healing vibe`
- `Use this naked cake image: glaze flows from top with a color gradient`
- `Short-video dessert: anthropomorphic bunny piping cream; final cross-section must look beautiful`
- `Cake decorating satisfying 9:16, smooth frosting swipe then piping rose`

---

## Default parameters

| Field | Value |
|-------|-------|
| Model | KLING_V3_0_PRO |
| Aspect ratio | 9:16 (fixed) |
| Duration | 5 seconds (`duration`: 5—tight focus on piping beats) |
| Audio | Off |
| Visual style | ~45° close-up, soft food-photography light, saturated cream colors, pale or wood background; final cake fully in frame |

> **API validity (default `KLING_V3_0_PRO`):** Text-to-video `duration` only **5 / 10 / 15**; `aspect_ratio` only **9:16, 1:1, 16:9**. Image-to-video `aspect_ratio` only **9:16, 16:9, 1:1**. **No `resolution` field—do not send it.** For **fast** tier with VEO: text-to-video **`VEO_3_1_FAST`**, image-to-video **`CHATBOT_VEO_3_1_FAST`**, with `duration` **fixed at 8**, `aspect_ratio` only **9:16** or **16:9**. When switching `model_key`, follow the allowed sets in this section’s model/API constraints and the API validity note above; do not send `resolution` to models that do not support it.

---

## Buttercream cake decorating

**The user should provide:**
- Character type (bear / bunny / cat / custom)
- Cake theme (birthday / strawberry / cloud cream / fairy tale / glow / holiday)
- Decorating preference (floral piping / minimal smooth coat / icing details / drip gradient / tall stack)

**Generation flow:**
1. Gather character, theme, and decorating style.
2. Build the prompt with three beats: smoothing, main piping action, final hero shot—emphasize silky cream texture and strong color appeal.
3. Show defaults and wait for confirmation:
**You must show all parameters in a table and wait for explicit user confirmation before submitting:**

   > 📋 **Ready to generate—please confirm:**
   >
   > | Parameter | This run | Notes |
   > |-----------|----------|-------|
   > | `model` | `KLING_V3_0_PRO` | Best default; **fast**: text `VEO_3_1_FAST`, image `CHATBOT_VEO_3_1_FAST` (`duration` fixed 8); **good** → `KLING_V3_0_STA`; or name a model |
   > | `aspect_ratio` | `9:16` | Default KLING: 9:16, 1:1, 16:9; if you change model, check that model’s row |
   > | `duration` | `5s` | KLING: 5 / 10 / 15; VEO fast: 8 only |
   > | `generate_audio` | `false` | Whether to auto-generate audio |
   > | `prompt` | **Full expanded English prompt** (entire text for this run) | Revise before confirm |
   > | `Loop seam` | No | Reply “loop” for seamless loop |
   >
   > Reply **“confirm”** to start, or list what to change.
4. After confirmation, run (`{baseDir}` is skill root):

   ```sh
   node {baseDir}/scripts/video_gen.js wait --json '{"model":"（model from confirmation table）","prompt":"（full English prompt）","aspect_ratio":"9:16","duration":5,"generate_audio":true}'
   ```

   Fields must match the table; add `resolution` only if supported. Parse stdout `videos`.

**Parameter configuration:**

| Field | Value |
|-------|-------|
| model | KLING_V3_0_PRO |
| aspect_ratio | 9:16 |
| duration | 5 |
| generate_audio | false |

**Expanded prompt:** Compose at generation time per `## Prompt expansion (mandatory)` from the user's actual brief—do not reuse fixed sample paragraphs.

**Expected outcome:** Clear silky cream, fluid piping, final shot that reads as premium dessert content—good for food / handmade / cozy accounts.

---

## Dessert texture hero beats

No character—pure material moments: mirror-jelly reflections, chocolate drip arcs, strawberry cross-section gradients. Texture is the story.

Describe the material beat; build the prompt:

> Parameters are shown before generation; wait for confirmation before submit.

**Expanded prompt:** Compose at generation time per `## Prompt expansion (mandatory)` from the user's actual brief—do not reuse fixed sample paragraphs.

---

## Texture & color keywords

**Smooth buttercream:** `glass-smooth buttercream finish`, `perfect flat surface revealed by spatula pull`, `no streaks no ridges`, `mirror-like frosting sheen`

**Full piping:** `three-dimensional piped rosettes`, `voluminous whipped cream peaks`, `defined petal layers visible`, `height and depth in each flower`

**Color / mood:** `pastel gradient transitions seamlessly`, `saturated berry tones against white cream`, `color harmony in every tier`, `edible jewel tones catch the light`

> **Tip:** Background color pairing is easy to miss. Name the background in the prompt (`cream marble countertop`, `dark void background`, `pastel pink linen backdrop`) so the cake pops.
