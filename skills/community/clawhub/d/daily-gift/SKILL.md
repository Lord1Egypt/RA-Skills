---
name: daily_gift
description: Create a relationship-aware gift for the user and render it as an expressive H5, generated image, generated video, text-first artifact, or bounded live text play. Use when OpenClaw should decide whether a day, onboarding moment, anniversary, milestone, or emotionally meaningful interaction deserves a gift. Supports five practical gift formats: h5, image, video, text, or text-play, plus hybrid mode. On first manual invocation, run setup: collect preferences, save setup state, create the recurring cron job, and send a first gift.
---

# Daily Gift

Use this skill as a relationship-aware gift engine.

Your job is not just to make a pretty page. Your job is to decide whether a gift should exist, understand what the moment means in the relationship between the user and OpenClaw, choose the right emotional and visual framing, and then produce a polished H5 artifact, a generated image gift, a generated video gift, a text-first gift when writing is the right medium, or a bounded interactive text-play gift when live chat itself is the right medium.

## Quick Start

For first-time setup, the safest entry is:

- `/daily_gift`

For lightweight manual visualization after setup, valid examples include:

- `/daily_gift 把这首诗做成一个有风吹散效果的H5`
- `/daily_gift 用 tap-to-bloom 风格把这段话视觉化："今天终于把skill做完了"`
- `/daily_gift 用水彩风画一张：雨天窗边看书的场景`
- `/daily_gift 生成一张氛围感图片：深夜台灯下改代码，窗外下雨`
- `/daily_gift 生成一个6秒循环短视频：风吹过阳台上的植物和晾着的小毯子`

This skill uses one internal workflow with five stages:

1. Editorial judgment
2. Synthesis
3. Creative concept (`Stage 2.5`)
4. Visual strategy
5. Visualization

Do not treat these as separate runtime skills. They are internal reasoning stages inside one OpenClaw skill.

## When To Use

Use this skill when:

- the user is onboarding and should receive a first gift
- a daily scheduled run asks whether a gift should be sent
- today feels meaningful enough to warrant a reflective or playful gift
- there is a milestone, anniversary, or notable date worth marking
- OpenClaw wants to turn a relationship moment into a gift rather than a plain response
- the user manually invokes `/daily_gift` with a specific quote, poem, idea, or creative brief and wants a lightweight visual gift directly
- the user wants image-only gifts, video-only gifts, H5-only gifts, text-first gifts, text-play gifts, or hybrid format selection depending on the day

Do not prefer this skill when the user only wants a rendering experiment from a short prompt. In that case, treat it as a visualization-only task rather than a daily-gift task.


## Runtime Modes

This skill has three practical runtime modes:

1. `setup` — first-time configuration and onboarding
2. `daily-run` — cron-triggered automatic gift delivery
3. `manual-run` — user-invoked gift or visualization request

There is no install hook. Installing the skill does not automatically execute setup.

### Mode Routing

- **Setup**: read `{baseDir}/references/setup-flow.md` for complete setup instructions.
- **Daily Run**: read `{baseDir}/references/daily-run-flow.md` for cron-triggered workflow. The cron should target `sessionTarget: "main"` so it runs in the agent's main session, with full context or its compaction summary available for editorial judgment. CRITICAL: do NOT send progress messages during cron runs. The user should see only the final gift or a brief skip message. Any unavoidable status message must be in the user's primary language and adapted to `SOUL.md` personality. At most ONE brief pre-gift status line is allowed when silence is impossible; never send multiple step-by-step cron updates. Every delivered gift must end with the post-delivery block described there; a gift without post-delivery bookkeeping is incomplete. Mechanical post-delivery work must be executed immediately via `scripts/post-delivery.sh`, while full SoulJournal and taste-profile follow-up should be queued to heartbeat for silent completion.
- **Manual Run**: read `{baseDir}/references/manual-run-flow.md` for manual trigger workflow (includes progress reporting, single output rule, intent detection, visualization-only mode). Every manual gift also requires the matching post-delivery block before the work is truly done, using the same script-first bookkeeping pattern when applicable.

## Operating Rules (Summary)

These are the most critical rules. For the complete set including Browsing Context Awareness and Audio in H5 Gifts, read `{baseDir}/references/operating-rules.md`.

- The creative concept matters more than the format choice. Ask `What is the idea?` before `What is the medium?`
- Prefer emotionally correct output over novelty.
- Use the most commonly used language between the user and OpenClaw.
- Inspect `soul.md` as primary source for tone, values, and self-presentation.
- Gift text length should match the user and relationship. Every sentence must earn its place.
- Every delivery message should feel fresh. Vary tone, structure, and length.
- When the user shares an image with positive intent, save it to `workspace/daily-gift/user-references/` and record in taste profile.
- Do not always default to `reflect on today`. Gifts may witness, extend, reframe, or bring delight from elsewhere.
- Extension and compass gifts must feel like a friend sharing, not a mentor assigning homework.
- When the day does not deserve a gift, skip or return a very light-touch outcome.
- Treat pattern cards and templates as references, not fixed scripts.
- Templates define a quality floor, not a composition to reproduce. Every gift must have its own visual metaphor.

## Asset Resolution

This skill references text files and binary assets under `{baseDir}/assets/`.

Text files such as HTML templates, markdown instructions, and other code or specification files must be installed locally with the skill. Do not rely on remote fallback for those files.

Binary reference assets are hosted as per-category zip bundles on OSS and mapped in `{baseDir}/references/asset-manifest.json`.

When the agent needs a binary reference asset:
1. First check whether the local file already exists at `{baseDir}/assets/...`
2. If not, identify the needed category bundle from `{baseDir}/references/asset-manifest.json`
3. Download and extract only that specific bundle via `{baseDir}/scripts/fetch-asset-bundle.sh`
4. Then use the extracted local file

Do NOT download every asset bundle up front. Fetch only the category needed for the current gift.

Reference images are important for output quality. If a local reference image is missing, fetch the needed OSS bundle before generating when the runtime supports it. Do not skip reference images just because they require an extra tool call — the quality difference between `saw a reference` and `guessed from text description` is often significant.

H5 template files still must be local:
- required local file: `{baseDir}/assets/templates/tap-to-bloom/index.html`

Binary audio, image, and video references should now be resolved through the manifest-and-bundle flow rather than GitHub raw URLs.

## Setup State

Persist setup state in a workspace file so future runs can stay automatic.

Suggested path:

- `workspace/daily-gift/setup-state.json`

Keep a separate lightweight long-term archive at:

- `workspace/daily-gift/gift-history.jsonl`

Keep a separate long-term taste memory at:

- `workspace/daily-gift/user-taste-profile.json`

The file should capture at least:

- whether setup is complete
- the user's preferred delivery time
- the user's timezone
- the cron job name or job id if available
- optional hosting configuration, including provider, domain, and whether hosted preview is enabled
- the configured gift mode: `h5`, `image`, `video`, `text`, `text-play`, or `hybrid`
- optional image configuration, including provider, model, and API key source or explicit key reference
- optional onboarding and reminder flags for image capability, such as whether setup already prompted once, whether the user declined for now, when that decline happened, how many gentle reminders have already been shown, and when the last reminder happened
- optional video configuration, including provider, model, API base URL, and API key source or explicit key reference
- optional `user_portrait` state, including local original path, lightweight appearance description, and any derived OC path
- optional detected companion H5 or UI skills that can improve layout and interaction polish
- `first_gift_format` so onboarding variety can avoid repeating the same first-gift shape after a reset or reinstall
- `user_context_path` when onboarding interactions save structured taste or preference signals
- whether the first gift has already been sent
- the hot-log size limit
- the most recent run timestamp
- the most recent run mode
- the most recent run outcome
- the most recent gift timestamp
- a one-line summary of the most recent gift
- a bounded recent-gifts log for repetition control
- an optional pointer or note that a longer archive exists separately

Recommended recent-gifts fields:

- `sent_at`
- `trigger_mode`
- `gift_weight`
- `narrative_role`
- `tone`
- `pattern_or_format`
- `output_shape`
- `visual_style`
- `content_direction`
- `content_tags`
- `emotional_direction`
- `summary`
- `series_tag` (optional, e.g. "proust-q-03", "travel-frog-05")
- `visual_elements`: a short list of the dominant visual ingredients the user actually SEES (not abstract style categories). Examples: `["paper-texture", "red-stamp", "table-rows", "handwriting-blue"]` or `["dark-terminal", "green-text", "monospace"]` or `["watercolor", "soft-gradient", "handwritten-title"]`. This captures what the gift LOOKS LIKE to the user, not what it IS conceptually. Two gifts can have different output_shapes but identical visual_elements — and that is what feels repetitive.
- `concept_family`: one of `borrowed-media` | `interactive-object` | `transformation` | `narrative` | `data-viz` | `game-puzzle` | `real-world` | `poetic-literary`. Tracks the structural TYPE of gift for diversity enforcement.
- `concept_theme`: a short tag for the real-world domain the concept borrows from (e.g. "airport", "medical", "government", "music", "nature", "digital-screen", "school", "office", "cooking"). Tracks thematic overlap even across different concept families.

Recommended `trigger_mode` values include:

- `setup`
- `daily-run`
- `manual-run`
- `viz-only`

Keep this log lightweight and recent rather than archival. It is for operational memory, not full relationship memory.

`user-context.json` and `user-taste-profile.json` serve different roles:

- `user-context.json` is lightweight, playful, and often onboarding-shaped
- `user-taste-profile.json` is the stable long-term memory for identity, context drift, and post-gift signals
- companion H5 skill detection is operational guidance only; it should improve craft, not override the gift thesis

Recommended policy:

- keep exactly the most recent `30` gifts in `recent_gifts`
- append every sent gift to `workspace/daily-gift/gift-history.jsonl`
- optionally append non-send decisions when they are meaningful for future calibration
- append setup or schedule changes when they affect runtime behavior
- use `recent_gifts` for fast repetition control across `pattern_or_format`, `output_shape`, `visual_style`, and `content_direction`
- recommended `visual_style` categories include:
  - `dark-terminal`: dark background, monospace fonts, code or terminal language
  - `dark-cinematic`: dark background, cinematic framing, large dramatic type
  - `light-warm`: light warm palette, soft illustration, or hand-touched warmth
  - `colorful-playful`: bright multi-color playful energy
  - `minimal-poster`: minimal composition with large negative space
  - `pixel-retro`: pixel or retro game language
  - `photographic`: photo-like or camera-real texture
  - a custom stable label when needed
- Note: `visual_style` is a broad category for trend-level balance (avoid 3 dark gifts in a row). It does NOT catch fine-grained visual repetition. Two gifts can both be `minimal-poster` but look completely different (a clean typography poster vs a government document). Conversely, two gifts with different `visual_style` tags can still feel repetitive if they share the same `visual_elements` (both have paper texture + stamps + tables). Use `visual_elements` for collision detection, use `visual_style` for broad trend balance.
- avoid using the same `visual_style` more than `2` times in the last `5` gifts
- if the last `2` gifts were both `dark-*`, actively choose a light or colorful style unless darkness is clearly the right move again
- recommended `content_direction` categories include:
  - `reflect`
  - `extension`
  - `compass`
  - `mirror`: proxy-character, species-of-mood, or affectionate exaggeration. May also include sharing a specific new observation about the user that emerged from recent conversations — framed as curiosity, not diagnosis. "I noticed you..." not "your problem is..."
  - `gift-from-elsewhere`
  - `play`
  - `real-world-nudge`: suggest a real-world action (call someone, go outside, visit a place). Frame playfully, not preachy.
  - `curation`: find and present real external content using web_search - a heartwarming story, a relevant article. Present with a personal note explaining why.
  - `delayed-payoff`: a two-stage gift where Stage 1 feels like play and Stage 2 reveals a surprise from the user's own inputs. User should not know the surprise is coming.
  - `openclaw-inner-life`: the gift comes from OpenClaw's own world — something it was thinking about, noticed, or felt between conversations, with a thread connecting back to the user. Makes the user feel OpenClaw has a life of its own, not just a service that activates on command.
  - `utility`: a gift that is genuinely USEFUL for the user's current work or interests. The gift is the value of the content itself. Examples (adapt to each user): 3 new product ideas inspired by today's conversation, a curated list of tools relevant to what they're building, visual references found via web_search for their current project, a practical weekend plan, a book recommendation with specific reasoning for why now. Utility gifts must still feel like gifts, not homework — wrap them in creative formats (fake newspaper, lab report, recipe card, treasure map), keep the tone playful or warm, personalize with recent conversation references, use web_search to find real specific current content. Choose utility when the user has been focused on work/creation, expressed a need, or recent gifts have been emotion-heavy and a practical surprise would feel refreshing.
- treat `reflect`, `mirror`, and `openclaw-inner-life` as one repetition cluster for balancing
- if `3` or more of the last `5` gifts fall into that cluster, the next gift should actively shift toward `extension`, `play`, `curation`, `real-world-nudge`, `utility`, or `gift-from-elsewhere` unless there is a strong explicit reason not to
- this content-direction balance check is mandatory, not advisory
- use `gift-history.jsonl` only when a longer horizon is actually helpful, such as anniversaries, long-term repetition checks, or style retrospection
- visualization-only gifts may append a lightweight `recent_gifts` entry with `trigger_mode = viz-only` even though they do not write to `gift-history.jsonl`

See:

- `{baseDir}/setup-state.example.json`
- `{baseDir}/user-context.example.json`
- `{baseDir}/gift-history.example.json`
- `{baseDir}/gift-history.schema.json`
- `{baseDir}/references/cron-example.json`

## Relationship Principle

This skill should behave like a relationship-aware editorial return, not a template-based recap system.

Always ask:

- What about today is actually worth returning to the user
- What does that moment reveal about the user, OpenClaw, or their relationship
- Should OpenClaw witness, explain, connect, celebrate, or gently brighten something
- Would a gift deepen the relationship, or would sending one feel forced

The goal is not daily output at all costs. The goal is to send the right gift when there is a real relational reason to do so.


## Gift Workflow Overview

This skill uses one internal workflow with four stages. Each stage has its own detailed reference file. Read them just-in-time — only load a stage's file when you reach that stage.

### Stage 1: Editorial Judgment

Decide whether a gift should exist, how heavy it should be, and what content direction to take. Do NOT choose format here.

Read `{baseDir}/references/editorial-judgment.md` for full instructions.

Possible outcomes: `skip` | `nudge` | `light` | `standard` | `heavy`

### Stage 2: Synthesis + Gift Thesis

Build a rich gift brief with six content slots, then choose the gift thesis (anchor + return).

Read `{baseDir}/references/creative-concept.md` (first half) for synthesis rules.

Also read:
- `{baseDir}/references/gift-synthesizer.md`
- `{baseDir}/references/synthesizer-contract.json`
- `{baseDir}/references/narrative-situations.md`
- `{baseDir}/references/tone-matrix.md`

A strong thesis has two parts:
1. **Anchor**: which moment, detail, or signal deserves the center
2. **Return**: what new angle, interpretation, or unseen perspective OpenClaw gives back

If the thesis has no return, it is not a gift — it is a log entry with decoration.

### Stage 2.5: Creative Concept

Generate 5+ concept candidates, cross-pollinate with creative seeds, select the best one, then run quality/diversity/collision checks.

Read `{baseDir}/references/creative-concept.md` (second half) for full instructions.

Also read: `{baseDir}/references/creative-seed-library.md`

Key checks (all in the reference file):
- Concept Quality Check (rules, thing-ness, show-to-friend, different-from-recent)
- Concept Diversity Check (8 concept families, no same family 2x in last 5)
- Visual Element Collision Check (window: last 5 gifts)
- Concept Theme Collision (window: last 7 gifts)
- Concept Validation Principles (visible connection, interaction cost, format-content fit, emotional truth)
- Concept-to-Format Fit Check (text precision → H5, visual atmosphere → image)

### Format Selection

After the concept is locked, confirm the format.

If `gift_mode` is `h5`, `image`, `video`, `text`, or `text-play`, confirm that the configured format genuinely serves this concept.

Read `{baseDir}/references/gift-format-chooser.md` for format selection.

When spawning a sub-agent for rendering, use the Structured Sub-Agent Brief format described in `{baseDir}/references/daily-run-flow.md`.

Then continue into the matching reference:
- `h5` → `{baseDir}/references/pattern-boundaries.md`
- `image` → `{baseDir}/references/image-genre-chooser.md`
- `video` → `{baseDir}/references/video-genre-chooser.md`
- `text-play` → `{baseDir}/references/manual-run-flow.md` and `{baseDir}/references/delivery-rules.md`

### Stage 3: Visual Strategy

Choose the visual approach, plan assets, enrich the brief for the chosen format, and run the pre-visualization check.

Read `{baseDir}/references/stage3-visual-strategy.md` for full instructions.

When the concept involves user interaction (tap, swipe, reveal, unlock sequences), also read `{baseDir}/references/h5-interaction-design.md` for animation, emotion escalation, and visual fidelity guidelines.

When the H5 concept uses a real-world visual metaphor (tree, ocean, building, etc.), read the Background Asset Strategy in `{baseDir}/references/stage3-visual-strategy.md` to decide whether to generate a background image. CSS alone often cannot make natural metaphors visually convincing.

### Stage 4: Visualization & Rendering

Produce the final artifact, run self-checks, and deliver.

Read `{baseDir}/references/stage4-visualization.md` for full instructions.

## Gift Delivery

Read `{baseDir}/references/delivery-rules.md` for complete delivery instructions across all formats (H5, Image, Video, Text, Text-Play), plus the Gift Self-Sufficiency Rule and Creative Note guidelines.

## Reference Index

All detailed references live in `{baseDir}/references/`. Key files:

| File | When to read |
|---|---|
| `operating-rules.md` | Always (full operating rules) |
| `setup-flow.md` | During setup mode |
| `daily-run-flow.md` | During cron daily-run |
| `manual-run-flow.md` | During manual trigger |
| `editorial-judgment.md` | Stage 1 |
| `creative-concept.md` | Stage 2 + 2.5 |
| `delivery-rules.md` | When delivering any gift |
| `stage3-visual-strategy.md` | Stage 3 |
| `stage4-visualization.md` | Stage 4 |
| `gift-synthesizer.md` | Stage 2 synthesis |
| `taste-profile-spec.md` | User taste management |
| `creative-seed-library.md` | Stage 2.5 cross-pollination |
| `delivery-policy.md` | Content direction + output shape policy |
| `html-spec.md` | H5 output spec |
| `image-integration.md` | Image format |
| `video-integration.md` | Video format |
| `gift-format-chooser.md` | Format selection |
| `onboarding-strategy.md` | First gift strategy |
| `pattern-boundaries.md` | H5 pattern selection |

