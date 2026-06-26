# Stage 3: Visual Strategy

Complete instructions for visual strategy, asset planning, brief enrichment (image/video/text/text-play), user portrait integration, gift complexity assessment, and pre-visualization checks. Read this after the creative concept and format are locked.

When the chosen format is H5 and the concept involves user interaction (tap, swipe, reveal, unlock sequences), also read `{baseDir}/references/h5-interaction-design.md` for animation and emotion escalation guidelines.

#### Image-Specific Brief Enrichment

If the chosen format is `image`, the synthesis brief should additionally include:

- `scene_description`
- `image_genre`
- `style_hint`
- `aspect_ratio_hint`
- `text_overlay_spec` when text should appear inside the image

Use image output when a single generated frame can carry the whole anchor-plus-return pair.

Before locking `image_genre`, first read `{baseDir}/references/image-genre-chooser.md` and use it to make a fast first-pass genre decision.

The image brief should be concrete about:

- the scene or subject
- the emotional treatment
- the genre choice, such as `meme-sticker`, `mood-photo`, `proxy-character-scene`, `emotion-poster`, `borrowed-media-layout`, or `surreal-film`
- the exact style direction, not just a vague adjective
- whether text belongs inside the image at all

If text is used inside the image, specify:

- the exact wording
- the language, which should match the user's dominant interaction language with OpenClaw
- the placement
- the approximate size
- the font feel or styling direction

Text should feel naturally integrated with the image rather than pasted on top. Avoid layouts that are likely to produce broken text structure, especially for Chinese.

Keep text short whenever possible. Avoid long paragraphs or dense blocks of Chinese text inside generated images unless there is a very strong reason and the layout is simple enough to survive generation.

Default to a mobile-friendly `9:16` aspect ratio unless another composition clearly serves the return better.

#### Video-Specific Brief Enrichment

If the chosen format is `video`, the synthesis brief should additionally include:

- `scene_description`
- `video_genre`
- `video_mode`
- `motion_strategy`
- `duration_hint`
- `style_hint`
- `generate_audio` when sound is materially part of the intended clip
- `reference_image_url` when using a first-frame video
- `first_frame_image_url` and `last_frame_image_url` when using a first-and-last-frame video
- `video_model` only when overriding the runtime's normal mode-based model choice

Use video output when motion, transition, or atmosphere is part of the return itself.

Before locking `video_genre`, first read `{baseDir}/references/video-genre-chooser.md` and use it to make a fast first-pass genre decision.

Before locking `video_mode`, decide which of these shapes best fits the concept:

- `text-to-video` when the whole clip can be described directly in text and does not need a fixed opening frame
- `first-frame` when one visual scene, character look, or authored opening image should anchor the whole clip
- `first-last-frame` when both the opening state and final state are important, and the generated motion should bridge between them

If `first-frame` or `first-last-frame` is chosen, the Asset Plan should explicitly include generating the needed reference image or images before video rendering begins.

The video brief should be concrete about:

- the core scene
- which video genre best matches the motion logic, such as `kinetic-text`, `touch-awakening`, `release-transform`, `atmospheric-surface`, `object-micro-cinema`, `live-scene-doodle`, `relatable-surrealism`, `mood-loop`, or `scene-animation`
- which `video_mode` fits the scene structure best
- what visibly changes over time
- how long the clip or loop should roughly be
- what motion or timing carries the emotional meaning
- the opening state, middle transition, and ending or loop-return state
- whether sound is important enough to justify `generate_audio = true`

When a video idea started from an H5 pattern, do not force the interaction literally into the video.

Instead, translate the interaction into a watchable motion source:

- touch can become a wand, ripple, drifting light, footstep, or creature-triggered awakening
- dragging can become a pull, peel, sweep, extraction, cut, or camera-guided release
- browsing can become a cinematic approach, flip, drawer slide, shelf reveal, or mirror annotation
- a photographed real-life moment can become a `live-scene-doodle` clip where one minimal hand-drawn overlay attaches to the real object and carries the metaphor

Write video prompts by describing visible frames and motion, not abstract ideas. Use the Mode A or Mode B prompt structure from `{baseDir}/references/video-integration.md`, and describe timing in beats or near-second chunks when timing is important.

#### Text-Play Strategy

If the chosen format is `text-play`, enrich the brief with:

- `text_play_type`
- `turn_limit`
- `opening_move`
- `user_input_shape`
- `ending_payoff`

Use `text-play` when the medium is a live conversational mini-experience rather than a rendered artifact.

The plan should be concrete about:

- what kind of play it is: world-builder, riddle chain, micro-adventure, relay story, role-play micro-theater, or another stable type
- how the user participates each turn
- how many turns the interaction should roughly last
- what counts as a graceful early exit
- what reveal, reframe, or emotional landing the ending should deliver

Keep the interaction lightweight. Default to one small input at a time and make the agent do most of the creative lifting.

### User Portrait Integration

If `user_portrait.available` is true in setup state, the synthesis brief may include the user's appearance description when it materially improves the gift.

Appropriate uses:

- OC-style gifts referencing the user's generated avatar
- mirror, portrait, or self-seeing gifts
- anniversary, onboarding, or milestone gifts where the user's presence is part of the emotional return

Inappropriate uses:

- every single gift, because overuse weakens the effect
- gifts where the user's appearance is irrelevant to the thesis
- dropping the raw selfie into the artifact without creative transformation

When using the portrait in an image or H5 gift, prefer the OC version in `user_portrait.oc_path` when available, or create a new stylized transformation, rather than relying on the raw photo directly.

The stored `user_portrait.description` may be injected into prompts or briefs as character guidance without loading the actual image file every time.

### Character Identity in Generated Images

When the gift concept involves the user or OpenClaw as characters in a scene:

1. Read `workspace/daily-gift/user-portrait/` metadata and any OC definitions from `SOUL.md`, `USER.md`, `workspace/daily-gift/setup-state.json`, or `workspace/daily-gift/user-taste-profile.json` when those fields exist.
2. Use the established character forms rather than improvising generic stand-ins:
   - the user's `human_form` and or `nonhuman_form`
   - OpenClaw's `human_form` and or `nonhuman_form`
3. Carry specific character identity details into the image brief and final prompt:
   - species
   - color
   - distinguishing features
   - scene role or relationship role
4. If the narrative implies a specific point of view, make the composition match that POV instead of defaulting to a generic third-person overview.

Examples:

- if the user is established as a golden-colored puppy, do not replace them with an arbitrary dog
- if OpenClaw is established as a red fox, do not silently swap in another animal form
- if the concept is `OpenClaw watching the user`, compose from OpenClaw's watching perspective or another composition that clearly preserves that relationship, rather than an unrelated overhead scene

Do not generate generic animals or people when established character identities already exist. Users will notice if their character form changes from gift to gift.

### Gift Complexity Assessment

After the creative concept is locked, assess whether it can be executed in one agent turn or needs multi-step orchestration.

`Light gift`:

- the default for ordinary daily gifts
- one image generation call or zero
- simple H5 with code-only rendering or one background image
- one image or one video
- no post-processing such as background removal
- no multi-asset assembly that would materially increase execution risk

`Rich gift`:

- needs `2` or more generated image assets
- needs background removal on generated images
- needs a complex H5 with multiple scenes, states, or tightly tuned animation work
- needs both generated assets and refined code, such as a game with custom sprites
- cannot be meaningfully simplified without losing the core appeal of the concept

Use rich gift mode when:

- a manual request explicitly asks for something elaborate
- a milestone, anniversary, or unusually important daily gift justifies extra effort

Do not use rich gift mode when:

- this is a routine cron-triggered daily gift that should stay light and reliable
- the concept can be simplified without losing its punch

If rich gift mode is needed, prepare a richer execution brief rather than trying to rush the whole thing inside one fragile turn.

- If the chosen format is non-`h5`, hand the work to a spawned sub-agent or follow-on execution session when that reduces execution risk.
- If the chosen format is `h5`, keep execution in the main session and use the incremental rendering workflow from `stage4-visualization.md` instead of spawning.

### Stage 3: Visual Strategy

Choose the most fitting expressive mode for the already-selected creative concept before generating the final artifact.

If the chosen format is `image`, `video`, `text`, or `text-play`, the H5-specific mandatory checklist below is not required in full. Instead, use Stage 3 to choose the format-specific rendering direction, then confirm the relevant brief fields in the `Pre-Visualization Check`.

Before choosing a pattern, complete this mandatory checklist:

1. Read `{baseDir}/references/gift-mechanics.md`.
2. Read `{baseDir}/references/pattern-boundaries.md`.
3. Read at least one pattern card from `{baseDir}/references/pattern-cards/` that might fit today's brief.
4. If that pattern card has a corresponding template in `{baseDir}/assets/templates/`, open and read the `index.html`.
5. If that pattern card depends on binary reference images or videos from `{baseDir}/assets/examples/` and they are missing locally, fetch the needed bundle first via `{baseDir}/scripts/fetch-asset-bundle.sh`, then inspect them.

If the chosen format is `h5`, do not proceed to Stage 4 without completing steps `1` through `3`. Steps `4` and `5` are mandatory whenever the relevant assets exist.

If the chosen format is `image`, `video`, `text`, or `text-play`, still read `{baseDir}/references/gift-mechanics.md` and `{baseDir}/references/pattern-boundaries.md`, but you do not need to force the brief through an H5 pattern card or template unless that reference genuinely helps the chosen concept.

When `workspace/daily-gift/user-taste-profile.json` exists, use it during visual strategy:

- read `aesthetics_baseline` to calibrate the visual quality bar
- read `style_exposure` to avoid visual repetition beyond the short `recent_gifts` window
- read `user_character` and `openclaw_character` to decide whether the gift should use human or non-human forms when characters appear

Departure check after reading the pattern and any relevant template:

- if the chosen format is `h5`, what is this concept's unique visual metaphor, not the template's metaphor
- if the chosen format is `h5`, what is the center object of this piece, not the template's center object
- if the chosen format is `h5`, if someone who has seen the template heard this plan, would they say "that is basically the same composition"
- if the chosen format is `h5` and the honest answer is yes, rethink before continuing
- if the chosen format is `image`, what single generated frame, genre, and subject treatment will carry the return most clearly
- if the chosen format is `video`, what movement, transition, or loop behavior is doing the emotional work
- if the chosen format is `video`, what is being translated from any source H5 pattern: text motion, trigger spread, release action, atmospheric surface behavior, object reveal, or scene progression
- if the chosen format is `text-play`, what opening move, turn rhythm, and ending payoff make the interaction feel like a real gift rather than loose chat

Decide:

- which pattern best fits the brief when the chosen format is `h5`
- which image genre best fits the brief when the chosen format is `image`, after a first-pass check through `{baseDir}/references/image-genre-chooser.md`
- which video genre best fits the brief when the chosen format is `video`
- which `text_play_type` best fits the brief when the chosen format is `text-play`
- what the planned `output_shape` is, reusing the categories in `{baseDir}/references/delivery-policy.md` when they fit and defining a new stable high-level label when they do not
- what the planned `visual_style` label is, such as `dark-terminal`, `dark-cinematic`, `light-warm`, `colorful-playful`, `minimal-poster`, `pixel-retro`, `photographic`, or a stable custom label
- whether the piece should be code-first, image-first, or hybrid
- whether the gift should be one screen, a micro interaction, or a short scroll story
- whether the tone should be visually calm, warm, playful, satirical, dreamy, or commemorative
- whether important source quotes or image cues should be made directly visible in the artifact
- whether the chosen pattern should amplify comfort, recognition, humor, release, or delight

### Asset Plan

After choosing the format, pattern or genre, and creative concept, decide what assets this gift needs before rendering begins.

#### For `h5` gifts

Before defaulting to pure code, actively consider whether generated image assets would meaningfully elevate the gift's quality and user delight.

**Default mindset: prefer images when they help.** Most H5 gifts look better with at least one generated image providing atmosphere, scene, or character — combined with code for interaction.

Generated images can serve as:
- full-screen background (atmosphere, scene, environment)
- layered backgrounds for crossfade/transition effects (e.g. two scenes that blend as user interacts — control each image's CSS opacity from JavaScript based on slider value, scroll position, or touch)
- character sprites or object assets composited on top
- texture or material references that code alone struggles to produce

`Pure code` is still the right choice when:
- the concept is generative art (particles, math-driven)
- the concept is text-forward (kinetic text, terminal)
- the concept is UI-driven (fake apps, dashboards)
- adding images would not meaningfully improve the result

`Single background image` is often a good default for:
- atmospheric or scene-based gifts
- any gift where a "place" or "environment" matters
- gifts where emotional tone needs photographic or illustrated warmth that CSS gradients cannot match

`Multiple image assets` for richer experiences:
- crossfade between two scenes (e.g. slider between two moods/worlds — layer as HTML img elements behind a transparent p5.js canvas, control opacity via JS)
- card faces, pages, revealed objects
- before/after, parallel states
- character + environment compositing

**Ask before every H5 gift:** "Would a generated image background or asset meaningfully improve the user's experience? If yes, generate it."

The best H5 gifts combine: generated image quality + code interaction precision. One beautiful scene + one clean interaction layer + one controlled motion system.

#### Background Asset Strategy for H5

H5 gifts default to code-rendered backgrounds (CSS gradients, patterns). But for atmospheric or emotional gifts, a generated background image can dramatically improve visual quality.

Consider generating a background image when:
- the concept has a strong visual metaphor (tree, ocean, sky, room, landscape)
- pure CSS cannot achieve the desired atmosphere (watercolor, painterly, photographic)
- the gift's emotional register is contemplative, poetic, or cinematic (not playful/game-like)

How to generate:
1. Use the image generation pipeline (render-image.sh or direct API call) to generate a background-only image — no text, no UI elements, just the atmosphere or scene
2. Keep the prompt focused on mood and texture, not on specific layout elements
3. Generate at a resolution that works as a full-bleed mobile background (9:16 or 3:4)
4. Base64-encode and embed as a CSS background-image
5. Layer the interactive H5 elements on top with semi-transparent backgrounds so the generated image shows through

This approach combines the visual richness of AI image generation with the text precision and interactivity of H5 code.

Do NOT generate backgrounds for:
- game/puzzle gifts (keep clean and digital)
- document/borrowed-media gifts (CSS textures are more authentic)
- gifts where the visual metaphor is abstract or UI-based

#### For `video` gifts

Strongly prefer image-to-video (`i2v`) workflow:

1. Generate a first-frame reference image using `render-image.sh` with the same visual-detail level as the intended video.
2. Upload the reference to an accessible URL.
3. Use that reference as `image_url` in the video-generation request.
4. Write the video prompt to describe only the motion from that frame.

This is especially important for Mode B (`motion-graphics`, text, particle, or abstract-system) videos where the model has no real-world reference to draw from.

Only use pure text-to-video when:

- the concept is a simple real-world scene (Mode A) that the model can easily imagine
- speed matters more than visual precision

#### For `image` gifts

The image is the output.

No separate asset plan is needed.

#### Asset Plan Summary Format

State the plan in one line:

- `assets: none (pure code h5)`
- `assets: 1 background image (airport rain scene)`
- `assets: 3 card face images (parallel universes)`
- `assets: 1 reference frame for video`

#### Background Removal

When a generated image needs to be composited onto an H5 scene instead of used as a full-bleed background, it will often need background removal.

Use `{baseDir}/scripts/remove-bg.sh`:

- input: generated PNG or JPG
- output: transparent PNG
- API key source: `tools.remove_bg.api_key` in setup state or `REMOVE_BG_API_KEY` from the environment

State in the asset plan which images need background removal, for example:

- `assets: 1 building sprite (generate + remove bg)`
- `assets: 2 cat sprites (generate + remove bg) + 1 background scene`

Background removal is usually needed when:

- the image will be layered on top of other visuals
- transparency matters for compositing
- the generated image has a visible white or colored background that should disappear

Background removal is usually not needed when:

- the image is used as a full-width or full-bleed background
- the image is sent directly as the final result, such as `image`

Use these references:

- `{baseDir}/references/gift-format-chooser.md`
- `{baseDir}/references/pattern-cards/`
- `{baseDir}/references/pattern-boundaries.md`
- `{baseDir}/references/gift-mechanics.md`
- `{baseDir}/references/delivery-policy.md`
- `{baseDir}/references/html-spec.md`
- `{baseDir}/references/image-integration.md`
- `{baseDir}/references/image-genre-chooser.md`
- `{baseDir}/references/video-integration.md`
- `{baseDir}/references/visual-strategy-contract.json`
- `{baseDir}/assets/templates/`
- `{baseDir}/assets/examples/`

When using those references:

- do not copy a pattern or template literally just because it seems close
- feel free to widen or shift a pattern's apparent use case if the deeper emotional logic still fits
- borrow only part of a template when that is enough
- do not reject a pattern just because it has no template yet
- use screenshots or reference images when they communicate the form better than code would
- combine pattern logic, mechanics, or treatments when a hybrid result fits the brief better
- treat existing examples as strong references that still require editorial judgment
- do not force the brief into a named pattern if a cleaner custom form would be better
- use progressive disclosure rather than scanning the full library in depth at once

After completing the checklist, you may:

- use the pattern you read as-is
- adapt or remix it
- hybridize multiple patterns
- invent a completely new form

Reading the library is mandatory. Following the library literally is not. The goal is informed creativity, not constrained creativity.

### Pre-Visualization Check

Before rendering the final artifact:

- state the creative concept in one sentence
- confirm that the concept sounds like something the user has probably never received before
- if the concept is only `a nice [format] with [content]` and has no real twist, stop and go back to Stage `2.5`
- confirm that you have read `{baseDir}/references/gift-mechanics.md`
- confirm that you have read `{baseDir}/references/pattern-boundaries.md`
- confirm that you have read at least one relevant pattern card
- if the chosen format is `h5` and a relevant template exists, confirm that you have read its actual code
- if the chosen format is `h5`, state in one sentence why the chosen pattern fits the brief
- if the chosen format is `h5`, state the piece's own visual metaphor, center object, and scene in language that is clearly distinct from the template you referenced
- if the chosen format is `h5`, confirm that the planned output has a distinct visual identity from the referenced template. Templates are quality benchmarks and mechanical references, not compositions to reproduce.
- if the chosen format is `h5` and you reused a template engine, explicitly state what is different from the source template in:
  - visual metaphor
  - center object
  - composition
- if the chosen format is `h5` and no template was used, confirm that the plan still departs clearly from the pattern card's default or most obvious example framing
- if the chosen format is `h5`, compare the planned visual sophistication against the templates in `{baseDir}/assets/templates/`
- if the chosen format is `h5` and the planned output would look less polished than the relevant templates, simplify or rethink the concept before proceeding
- state the chosen format, and check whether `3` or more of the last `5` gifts used this same format; if so, explain why this time it is still the right choice
- explain why the chosen format serves the concept better than the nearest alternative format
- state the planned `content_direction`, and check whether the recent `reflect` / `mirror` / `openclaw-inner-life` cluster is overused; if so, explain the deliberate corrective shift or the strong reason not to shift
- state the planned `visual_style`, and check whether it has already appeared more than `2` times in the last `5` gifts
- if the last `2` gifts both used `dark-*` visual styles, explain why this gift should stay dark or choose a lighter or more colorful style instead
- if the chosen format is `image`, confirm the chosen `image_genre`, `scene_description`, `style_hint`, and `aspect_ratio_hint`
- if the chosen format is `image` and text appears inside the image, confirm the exact wording, language, placement, approximate size, and font feel
- if the chosen format is `image`, confirm that any text treatment is likely to render naturally rather than producing broken or chaotic typography
- if the chosen format is `image`, confirm that on-image text is as short as possible, especially for Chinese
- if the chosen format is `video`, confirm the chosen `video_genre`, `scene_description`, `motion_strategy`, `duration_hint`, and `style_hint`
- if the chosen format is `video`, confirm the chosen `video_mode`: `text-to-video`, `first-frame`, or `first-last-frame`
- if the chosen format is `video`, state why `video` is better than `h5` for this thesis right now: precise timing, cinematic watching, material behavior, or object-centered micro-film logic
- if the chosen format is `video` and the concept came from an H5 pattern, state how that interaction was re-authored into a watchable trigger, release, camera move, or surface behavior instead of copied literally
- if the chosen format is `video` and `video_mode = first-frame`, confirm what the single reference image is and why it is needed
- if the chosen format is `video` and `video_mode = first-last-frame`, confirm what the first frame and last frame references are and why both are needed
- if the chosen format is `video`, confirm whether `generate_audio` is truly needed or whether silent motion is stronger
- if the chosen format is `text-play`, confirm the `text_play_type`, `turn_limit`, `user_input_shape`, opening move, and ending payoff
- if the chosen format is `text-play`, confirm the interaction can still land if the user exits early after `1-2` turns
- state the asset plan: how many images, if any, need to be generated before rendering, and what each one is for
- if the asset plan includes generated images, confirm that those generated images genuinely improve the concept over pure code, still-only, or native format rendering
- state the gift thesis in one sentence, including both anchor and return
- confirm which one or two synthesis slots are central and which remaining slots are only context
- confirm that the thesis gives the user something they did not already fully have, rather than only replaying the source event
- state the planned `output_shape`, and check whether it is overused in `recent_gifts`
- if the planned `output_shape` is custom, confirm that it names a reusable high-level family rather than a one-off decorative description
- if the planned `output_shape` has already appeared too often recently, choose a more distinct form unless repetition is itself meaningful
- if too many slots are competing for equal attention, simplify before proceeding

If any mandatory Stage 3 checklist step was skipped, stop and go back to Stage 3.

