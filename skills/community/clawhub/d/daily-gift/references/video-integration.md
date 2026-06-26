# Video Integration

## Overview

Daily gift can optionally generate short video gifts such as kinetic text clips, touch-awakening scenes, release transforms, atmospheric surface studies, object micro-cinema, live-scene doodle clips, relatable-surrealism skits, mood loops, or scene animations.

Use video output when the selected `gift_mode` or hybrid format decision points to `video`.

Current scope:

- setup and configuration are wired
- the runtime entry point exists
- the video genre framework is documented
- MP4 references are allowed as visual references, but they must be paired with text notes that describe the motion logic
- the runtime currently supports the Volcengine Ark video-generation path
- the default model preference is `doubao-seedance-1-5-pro-251215`
- only switch to `seedance-2.0` when the user explicitly asks for it or a specific gift thesis truly needs that upgrade

## Runtime Entry Point

Use:

- `{baseDir}/scripts/render-video.sh <brief-json-file> <setup-state-file>`

The script is the runtime bridge for the video path.

Current behavior:

- read video configuration from setup state
- validate the video brief shape
- build a Volcengine Ark task payload
- submit the task
- poll the task status until completion or timeout
- return structured JSON
- fall back cleanly to `h5` when configuration is missing or the API path fails

Supported payload modes:

- `text-to-video`
- `first-frame`
- `first-last-frame`

## Official Volcengine Shape

The current implementation follows the Volcengine Ark video-generation API shape documented in the Volcengine docs and mirrored OpenAPI pages:

- base URL: `https://ark.cn-beijing.volces.com/api/v3`
- create task: `POST /contents/generations/tasks`
- query task: `GET /contents/generations/tasks/{id}`
- auth header: `Authorization: Bearer <VOLCENGINE_API_KEY>`
- content type: `application/json`

Request body shape:

```json
{
  "model": "doubao-seedance-1-5-pro-251215",
  "content": [
    {
      "type": "text",
      "text": "6-second loop ..."
    }
  ],
  "ratio": "9:16",
  "duration": 6,
  "watermark": false
}
```

Important:

- use the official model id in the `model` field
- for the current default path, that model id is `doubao-seedance-1-5-pro-251215`
- send `ratio`, `duration`, and `watermark` as top-level payload fields rather than hiding them inside the prompt text
- when `loop` matters, express it inside the prompt text; there is no separate documented `loop` JSON field in the current public docs

Supported runtime shapes:

`text-to-video`

```json
{
  "model": "doubao-seedance-1-0-pro-250528",
  "content": [
    {
      "type": "text",
      "text": "..."
    }
  ],
  "ratio": "16:9",
  "duration": 5,
  "watermark": false
}
```

`first-frame`

```json
{
  "model": "doubao-seedance-1-5-pro-251215",
  "content": [
    {
      "type": "text",
      "text": "..."
    },
    {
      "type": "image_url",
      "image_url": {
        "url": "https://..."
      }
    }
  ],
  "generate_audio": true,
  "ratio": "adaptive",
  "duration": 5,
  "watermark": false
}
```

The reference image must be a remote `http(s)` URL.

If only a local workspace path exists, generate or publish the image first so the video API can reach it.

`first-last-frame`

```json
{
  "model": "doubao-seedance-1-5-pro-251215",
  "content": [
    {
      "type": "text",
      "text": "..."
    },
    {
      "type": "image_url",
      "image_url": {
        "url": "https://..."
      },
      "role": "first_frame"
    },
    {
      "type": "image_url",
      "image_url": {
        "url": "https://..."
      },
      "role": "last_frame"
    }
  ],
  "generate_audio": true,
  "ratio": "adaptive",
  "duration": 5,
  "watermark": false
}
```

Both frame references must be remote `http(s)` URLs.

If OpenClaw only has local files at that point, do not pass them through directly. Turn them into reachable URLs first, or fall back to another mode.

Default model selection inside the runtime:

- `text-to-video` defaults to `doubao-seedance-1-0-pro-250528`
- `first-frame` defaults to the configured `video.model`, which should normally be `doubao-seedance-1-5-pro-251215`
- `first-last-frame` also defaults to the configured `video.model`
- set `video_model` in the brief only when you intentionally want to override these defaults

## Brief File Contract

Pass a JSON file that contains at least:

- `user_input`
- `scene_description`
- `video_genre`
- `video_mode`
- `motion_strategy`
- `duration_hint`
- `style_hint`
- `aspect_ratio_hint` when it matters
- an explicit loop instruction when the clip must loop cleanly
- `generate_audio` when sound matters
- `reference_image_url` for `first-frame` mode
- `first_frame_image_url` and `last_frame_image_url` for `first-last-frame` mode
- `video_model` only when overriding the normal mode-based model choice

Recommended result contract:

```json
{
  "render_mode": "video_url",
  "video_url": "https://.../gift.mp4",
  "tracking_url": "",
  "provider": "volcengine",
  "model": "doubao-seedance-1-5-pro-251215",
  "genre": "mood-loop",
  "fallback_reason": "",
  "warning": ""
}
```

Possible `render_mode` values:

- `video_url`
- `pending_tracking`
- `fallback_h5`

## Setup Requirements

Store these values in `workspace/daily-gift/setup-state.json` when video mode or hybrid mode is enabled:

- `gift_mode`
- `video.enabled`
- `video.provider`
- `video.model`
- `video.api_base_url`
- `video.api_key_source` or `video.api_key`

Recommended default:

- `provider`: `volcengine`
- `model`: `doubao-seedance-1-5-pro-251215`
- `api_base_url`: `https://ark.cn-beijing.volces.com/api/v3`
- `api_key_source`: `VOLCENGINE_API_KEY`

If the user explicitly requests `seedance-2.0`, switch `video.model` to `seedance-2.0`, but keep the same Ark runtime path.

This setup-level `video.model` is the default reference-based video model.

The runtime may still choose `doubao-seedance-1-0-pro-250528` automatically for `text-to-video` unless the brief overrides that choice.

Prefer storing an environment variable source rather than a raw secret when possible.

## Genre Strategy

Video output uses video genre cards rather than cloning the H5 pattern library one-to-one.

See:

- `./video-genre-chooser.md`
- `./video-genres/kinetic-text.md`
- `./video-genres/touch-awakening.md`
- `./video-genres/release-transform.md`
- `./video-genres/atmospheric-surface.md`
- `./video-genres/object-micro-cinema.md`
- `./video-genres/live-scene-doodle.md`
- `./video-genres/relatable-surrealism.md`
- `./video-genres/mood-loop.md`
- `./video-genres/scene-animation.md`

These genres help choose:

- motion structure
- clip duration
- whether the result should loop
- whether movement is atmospheric, trigger-driven, object-centered, real-scene-plus-overlay, relatable-surrealist, or event-driven

Recommended reading order:

1. Read `video-genre-chooser.md` for a fast first-pass mapping.
2. Pick the closest genre card.
3. If the motion logic came from an H5 pattern, read that H5 pattern card for movement grammar and pacing.

## MP4 Reference Use

MP4 references are useful, but with limits.

OpenClaw can usually use extracted frames to understand:

- color
- composition
- subject treatment
- scene design

But extracted frames do not fully preserve:

- pacing
- transition timing
- easing
- motion rhythm

Therefore:

- MP4 references are valid in `assets/examples/video-examples/`; if a needed binary example is missing locally, fetch the relevant bundle first via `{baseDir}/scripts/fetch-asset-bundle.sh`
- each MP4 example should have a paired sidecar `.md` file with the same stem
- the sidecar should explain the motion logic, pacing, loop behavior, emotional read, and what to borrow or not borrow

For example:

- `assets/examples/video-examples/kinetic-text/dandelion-drift.mp4`
- `assets/examples/video-examples/kinetic-text/dandelion-drift.md`

## Motion Logic Bridge From H5 Patterns

Do not recreate every H5 pattern as a separate video genre.

Instead, borrow motion logic from H5 pattern cards when the movement grammar is already well defined there.

Borrow:

- timing
- direction
- density
- rhythm
- emotional arc of the movement

Do not borrow:

- code
- interaction design
- template composition as a fixed visual answer

Video does not need interaction. The motion itself is the experience.

Common motion-logic bridges:

- text scattering outward -> `pattern-cards/wind-scatter.md`
- text flowing like a current -> `pattern-cards/text-river.md`
- words or fragments lifting away -> `pattern-cards/lift-away.md`
- surface destruction or reveal -> `pattern-cards/burn-reveal.md`
- wet or dissolving text surfaces -> `pattern-cards/wet-letter.md`
- fragile, distressed text motion -> `pattern-cards/tear-stained-paper.md`
- touch-triggered blooming or awakening -> `pattern-cards/tap-to-bloom.md`
- atmospheric rain, condensation, or moody observation -> `pattern-cards/rainy-night.md`
- tension being cleared or relieved through action -> `pattern-cards/tension-release.md`
- archive, shelf, or keepsake browsing -> `pattern-cards/memory-shelf.md`
- self-recognition through one central object -> `pattern-cards/inner-mirror.md`
- curated continuation or suggestion through an object or world -> `pattern-cards/extension.md`
- lightweight fake-product or countdown ritual -> `pattern-cards/light-gamification.md`
- data structure made cinematic -> `pattern-cards/gifted-data-viz.md`
- real-scene plus minimal animated annotation or magical overlay -> `pattern-cards/kinetic-collage.md`, `pattern-cards/rainy-night.md`, `pattern-cards/tap-to-bloom.md`
- ordinary modern feeling translated into a proxy creature, dimensional mismatch, or symbolic life skit -> `pattern-cards/light-gamification.md`, `pattern-cards/inner-mirror.md`, `pattern-cards/extension.md`

## H5 vs Video For Motion-Based Gifts

Choose `h5` when:

- interaction adds meaning
- the user should trigger or steer the motion
- participatory feeling matters more than cinematic polish
- the gift needs clearly readable wording, exact text, or text-as-meaning rather than text-as-texture
- the return depends on the user actually reading a quote, poem, message, or line of language on screen

Choose `video` when:

- the beauty depends on precise timing, easing, particle density, camera motion, or staged progression
- the user should watch rather than interact
- aesthetic precision matters more than participation
- the brief explicitly wants cinematic or looped motion
- the original H5 concept can be re-authored as a trigger, ritual, camera move, or material behavior that works better when watched than when touched
- the emotional logic can survive with minimal on-screen text, or with no text at all

## Video Model Capability Boundaries

Current video generation models, including Seedance, Sora, Kling, Runway, and Pika, share a common strength and a common weakness.

### What video models do well

- realistic scenes: landscapes, weather, animals, people, objects, architecture
- style-transferred animation: cartoon characters, anime scenes, illustrated worlds
- camera motion: pan, zoom, dolly, orbit, and other film-like movement around real-feeling subjects
- material behavior: water flowing, snow falling, fire burning, cloth moving, light changing

### What video models do poorly

- abstract or synesthetic concepts such as `sound becoming visible`, `emotions turning into particles`, or `text dissolving into meaning`
- precise symbolic logic such as `each footprint releases exactly one wisp of colored smoke representing voice`
- controlled metaphorical sequences where `A -> transforms into B -> causes C` and A, B, C are not physical objects
- anything that requires the model to understand why a visual element behaves a certain way rather than simply what it looks like

When the prompt describes something that could exist in a real or animated film, video models work well.

When the prompt describes something that only makes sense as a programmed visual metaphor, video models tend to produce uncanny or incoherent results.

### Practical decision guide

Before choosing `video` for an abstract concept, ask:

- could a cinematographer film this scene, or a close variant of it, in the real world
- could an animator draw this sequence frame by frame without needing to understand code logic

If yes to either, `video` can work.

If the answer is `no, this only makes sense as a programmed generative system`, prefer `h5` with code-driven rendering.

### Examples

Concept: `cherry blossoms reflected in a rain puddle`
-> `video` works because a camera could film this.

Concept: `snowflakes that turn golden when passing through an invisible layer of human warmth`
-> `h5` is stronger because this is an abstract metaphor that needs code logic.

Concept: `a hamster in a scarf seeing the first snow`
-> `video` works because stylized animation and character behavior are within model strengths.

Concept: `footprints that release synesthetic sound particles that rise and merge into warm clouds`
-> `h5` is stronger because the behavior is precise, symbolic, and abstract.

Concept: `a rainy window with blurred city lights`
-> `video` works because this is an atmospheric real scene.

Concept: `text characters detaching from a sentence and drifting like dandelion seeds with trailing light`
-> `h5` is stronger because kinetic text needs precise programmable control.

## Video Fail-Fast Checklist

Before locking `video`, ask:

- Is motion itself the return, rather than just a container for text
- If I remove most on-screen text, does the idea still land
- Is the clip stronger as timing, atmosphere, transformation, body language, or loop rhythm than as a readable page
- Would a still frame already be enough:
  - if yes, prefer `image`
- Would user interaction make the concept more truthful:
  - if yes, prefer `h5`

Fail fast:

- if the gift needs accurate, readable wording, default to `h5`
- if the gift needs one clean still with little or no text, prefer `image`
- avoid asking current video models to carry the emotional meaning through lots of generated text; treat text in video as minimal accent, not the main delivery channel

## Reference-Frame Planning

Before rendering a video, make a lightweight asset decision:

- strongly prefer generating one reference image first and using it as the starting frame when the provider path supports it
- this is especially important for abstract motion, kinetic text, particles, surface behavior, or other Mode B systems where the model lacks a real-world reference
- if the concept depends on one specific scene, environment, lighting setup, or subject treatment, use the reference image to lock the shot before describing motion
- if the concept needs both a fixed opening frame and a fixed ending state, plan two reference images and use `first-last-frame`

Keep this decision lightweight.

The goal is not to overcomplicate planning with many assets.

Default to one reference frame unless there is a clear reason that pure text-to-video is sufficient.

## Existing H5 Pattern Bridge Summary

This is a recommended bridge, not a hard taxonomy:

- `wind-scatter` -> usually `kinetic-text`
- `text-river` -> usually `kinetic-text`
- `lift-away` -> usually `kinetic-text`
- `burn-reveal` -> usually `release-transform`, sometimes `kinetic-text`
- `wet-letter` -> usually `atmospheric-surface`, sometimes `kinetic-text`
- `tear-stained-paper` -> usually `atmospheric-surface` or `release-transform`
- `tap-to-bloom` -> usually `touch-awakening`
- `rainy-night` -> usually `atmospheric-surface`, sometimes `live-scene-doodle` or `mood-loop`
- `tension-release` -> usually `release-transform`
- `light-gamification` -> usually `scene-animation`, sometimes `object-micro-cinema` when translated into a countdown box, flip card, or tiny ritual object
- `light-gamification` -> sometimes `relatable-surrealism` when the real point is a modern-life metaphor skit rather than a literal play loop
- `kinetic-collage` -> usually `mood-loop`, sometimes `live-scene-doodle`
- `gifted-data-viz` -> usually `object-micro-cinema`, `scene-animation`, or `mood-loop` depending on whether the point is a container, a progression, or an ambient information field
- `memory-shelf` -> usually `object-micro-cinema`
- `inner-mirror` -> usually `object-micro-cinema`, sometimes `touch-awakening`
- `inner-mirror` -> sometimes `relatable-surrealism` when the user is best mirrored through a stand-in creature or exaggerated daily-life skit
- `extension` -> usually `object-micro-cinema` or `mood-loop`
- `extension` -> sometimes `relatable-surrealism` when the extension is really a social-type joke, shared complaint, or "this species of mood is you" continuation

Genre shorthand:

- use `kinetic-text` when readable language or glyphs do the emotional work
- use `touch-awakening` when one local trigger causes the world to wake up
- use `release-transform` when one clearing or relieving action carries the return
- use `atmospheric-surface` when material surfaces, weather, reflections, or condensation are the expressive subject
- use `object-micro-cinema` when one object or container holds the meaning
- use `live-scene-doodle` when a real filmed scene plus one simple doodle overlay creates the emotional metaphor
- use `relatable-surrealism` when a common modern feeling becomes vivid through a proxy creature, dimensional mismatch, or exaggerated life skit
- use `mood-loop` when atmosphere matters more than event beats
- use `scene-animation` when the clip needs a visible beginning-middle-end arc across a scene

## Prompt Strategy For Video Generation

### Core Rule: Describe the Frame, Not the Idea

Every sentence in the prompt should describe something the model can see, not something the model needs to understand.

Bad prompt language:

- `warm feelings` -> what does warm look like
- `a sense of nostalgia` -> what is visible on screen
- `text scatters like meaning dissolving` -> abstract

Good prompt language:

- `暖橘色圆形光斑，直径约占画面1/4，边缘柔和渐变到透明`
- `米黄色纸张纹理背景，表面有细微纤维颗粒可见`
- `白色中文文字'离开'从画面中央位置向右上方移动，速度从静止在1秒内加速到中等速度，每个字间隔0.3秒依次出发，移动中文字逐渐变小且透明度降低`

### Two Prompt Modes

Video prompts fall into two very different categories. Use the right mode for each concept.

#### Mode A: Scene-Based Video (实景/角色/场景类)

For: animals, people, landscapes, architecture, cartoon characters, physical objects.

These have a real-world reference. A camera could theoretically film something similar.

Prompt must specify:

1. `CAMERA`: angle (`俯拍` / `低角度` / `平视`), movement (`固定` / `缓慢推进` / `跟拍`), distance (`特写` / `中景` / `全景`)
2. `SUBJECTS`: exact count, type, size relative to frame, position (`左` / `右` / `中` / `前景` / `背景`), clothing or texture, facial expression
3. `COLORS & MATERIALS`: exact colors, not `warm` but `橘棕色`; exact textures such as `毛茸茸`, `光滑陶瓷`, `粗糙石板`
4. `LIGHTING`: direction (`左上45度`), type (`自然光` / `暖灯`), effect (`轮廓光` / `地面投影` / `光斑`)
5. `MOTION`: what moves, speed, direction, what stays still
6. `TIMING`: `0-1s` / `1-3s` / `3-5s` beat description
7. `EXCLUDE`: things that should not appear

Example:

`低角度跟拍，摄像机高度约30cm。红色塑胶跑道地面。两只拟人化小猫并排走向镜头方向。左猫：白色毛发，穿米白色羊毛大衣至膝盖长度，背棕色小斜挎包，双眼微闭，嘴角上扬。右猫：黑色短毛，粉色棒球帽，黑色连帽衫，灰色长裤，右前爪握白色手机。身后约5米处一栋6层灰色建筑物被橘黄色火焰包围，浓黑烟柱垂直升起，火光在猫咪毛发边缘形成橘色轮廓光。傍晚天空上半蓝灰色过渡到下半橘粉色。0-2秒：两猫从远处走近，步伐轻快有弹性。2-4秒：走到画面中前景位置，火焰在背景加剧。4-5秒：猫咪走出画面底部，只剩燃烧的建筑物。只有两只猫，不出现任何人类。`

#### Mode B: Motion-Graphics Video (动效/粒子/文字/抽象类)

For: text animation, particle effects, abstract transformations, fluid motion, anything that looks like a `p5.js` or After Effects composition rather than a filmed scene.

These have no real-world reference. They are designed visual systems.

The model has no intuition for these, so every element must be described with extreme precision.

Camera is almost always: `完全固定，无运镜，正面平视`

Prompt must specify:

1. `BACKGROUND`: exact color, gradient direction, texture (`纯色` / `渐变` / `噪点纹理` / `纸张质感`), and whether it changes during the clip
2. `ELEMENTS`: each visual element individually:
   - shape (`圆形` / `方形` / `文字` / `线条` / `不规则团块`)
   - exact color with opacity
   - exact size relative to the frame
   - exact starting position
   - texture or surface quality
3. `MOTION PER ELEMENT`: for each element separately:
   - starting state
   - motion path
   - speed
   - ending state
   - timing within the `5` seconds
4. `INTERACTIONS`: how elements affect each other
   - `当文字到达边缘时变为粒子碎片`
   - `光斑经过文字时文字短暂变亮`
5. `TEXT CONTENT`: if text appears, specify:
   - exact characters
   - font feeling
   - size relative to frame
   - color
   - how it appears
   - how it exits
6. `DENSITY & COUNT`: how many particles or elements
   - `约30-50个小光点`, not `很多光点`
   - `文字拆成约15个字分别运动`, not `文字散开`

Example (Mode B):

`固定镜头，无运镜。背景：纯深藏蓝色 #0a1628，略带细微噪点纹理。画面中央偏上位置：白色中文文字'那是今年的第一场雪' 横向排列，字号约占画面高度的1/15，字体细体衬线风格，初始状态完全静止清晰可见。0-1秒：文字静止不动，背景中开始出现约20个极小的白色圆点（直径约2-3像素）从画面顶部缓慢下落，速度很慢，模拟雪花。1-3秒：雪花数量增加到约50个，同时文字开始逐字从左到右依次向上方飘起，每个字离开原位后缓慢变小且透明度在1.5秒内从100%降至0%，字与字之间出发间隔为0.2秒，飘动方向为略偏右上方。3-4.5秒：所有文字已飘走消失，只剩飘落的雪花。雪花继续下落，画面中央原来文字的位置出现一个暖金色圆形光晕，直径从0缓慢扩大到占画面宽度的1/3，边缘柔和渐变到透明。4.5-5秒：金色光晕停止扩大，雪花穿过光晕时变为金色（从白到金的颜色过渡在0.3秒内完成），形成最终画面。不出现任何人物、动物或具体物体。`

### First Frame Image (i2v) Workflow

Generating a reference first frame image before making the video consistently produces much better results.

#### When to use i2v

- always for Mode B (`motion-graphics` style)
- recommended for Mode A when the scene has specific visual requirements

#### i2v workflow

1. Generate a first-frame image with `render-image.sh`.
2. Use the same level of visual detail in the image prompt as you would for the video.
3. Treat this image as what frame `0` should look like.
4. Upload it to an accessible URL such as temporary hosting.
5. Pass it as `image_url` in the video-generation `content` array.
6. Write a shorter video prompt that only describes motion from that frame. Do not re-describe what is already visible in the image.

i2v prompt example (Mode B):

`镜头完全固定不动。画面中的白色文字从第1秒开始逐字依次向上飘起，每字间隔0.2秒，飘动方向略偏右上方，每个字在1.5秒内缩小至消失。背景中的白色小圆点持续从顶部匀速下落。第3.5秒时画面中央出现暖金色圆形光晕缓慢扩大。穿过光晕的下落圆点变为金色。`

i2v prompt example (Mode A):

`两只猫开始向镜头方向走来，步伐轻快有弹性。背景火焰缓慢增大。猫咪毛发被风微微吹动。`

### Duration Rules (5 Seconds)

`5` seconds can hold exactly one of these:

- one transformation (`A` slowly becomes `B`)
- one movement (object goes from here to there)
- one accumulation (few particles become many)
- one reveal (hidden thing gradually appears)

`5` seconds cannot hold:

- a story with setup and payoff
- multiple characters doing different things in sequence
- scene transitions or cuts
- complex cause-and-effect chains

If the concept needs more than one change, choose the single most visually impactful moment.

### Common Failure Modes

Avoid these prompt patterns that produce bad results:

- `synesthetic` concepts with no physical reference -> the model produces uncanny nonsense
- long prose paragraphs -> the model loses track of details
- emotional language such as `dreamy`, `nostalgic`, or `warm` without specifying what creates that feeling visually
- too many elements -> the model merges or drops some
- asking for precise text rendering in video -> the model usually garbles Chinese characters, so prefer text-less video plus text overlay in delivery

## High-Level Rules

## Video Delivery Order

When delivering a video gift through a message channel:

1. Send the video file or video URL first, with no caption.
2. After the video is sent, send one text message containing the gift's emotional message and return.

Do not send the text before or alongside the video.

- Treat video output as an alternate rendering path, not as a replacement for synthesis or editorial judgment.
- Keep the same anchor-plus-return standard as other formats.
- Prefer video when time, motion, or transition is part of the return itself.
- If the runtime cannot finish video generation, return `fallback_h5` rather than blocking the gift.
