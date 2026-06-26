---
name: video-overlay-cleanup
description: Use this skill when the user wants to clean a video or screen recording by removing overlays such as status bars, notification banners, floating controls, subtitle bars, fixed watermarks, or other surface UI elements. Especially useful for FFmpeg-based frame extraction, region mask generation, fixed-overlay removal with ffmpeg removelogo, and orchestrating frame-by-frame restoration workflows that use Gemini Nano Banana 2 before rebuilding the video.
homepage: https://github.com/hyuuuliu/video-overlay-cleanup-skill
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
metadata: {"openclaw":{"emoji":"🎬","requires":{"bins":["bash","ffmpeg","ffprobe","python3"],"packages":["google-genai","Pillow"]},"env":[{"name":"GEMINI_API_KEY","required":true,"sensitive":true,"description":"Required API key for Gemini Nano Banana 2 image editing mode."},{"name":"GEMINI_MODEL","required":false,"description":"Optional Gemini model override."},{"name":"GEMINI_IMAGE_SIZE","required":false,"description":"Optional Gemini image size override."}],"primaryEnv":"GEMINI_API_KEY"}}
---

# Video Overlay Cleanup

**Repository**: https://github.com/hyuuuliu/video-overlay-cleanup-skill

## Overview

Use this skill to turn a raw video or screen recording into a cleaner version with fewer visible overlays.

This skill is a workflow skill, not a claim of magical ground-truth recovery. It is best for:

- fixed overlays at stable positions
- short-lived banners or floating UI with a known mask
- cleaning screen recordings for editing or redistribution
- preparing a frame-by-frame restoration job for Gemini Nano Banana 2

This skill should frame the task as `video cleanup` or `overlay removal`, not guaranteed factual restoration of hidden content.

## Provider Support

This version supports one real model provider for generative frame repair:

- `Gemini Nano Banana 2` via the Gemini image generation and editing API

Before using `gemini-nano-banana` mode, the user must configure an API key:

```bash
export GEMINI_API_KEY='your_api_key_here'
```

Optional model override:

```bash
export GEMINI_MODEL='gemini-3.1-flash-image-preview'
export GEMINI_IMAGE_SIZE='1K'
```

## Runtime Requirements

Declare these explicitly when installing or reviewing the skill:

- required binaries:
  - `bash`
  - `ffmpeg`
  - `ffprobe`
  - `python3`
- required credential for Gemini mode:
  - `GEMINI_API_KEY`
- optional Gemini env vars:
  - `GEMINI_MODEL`
  - `GEMINI_IMAGE_SIZE`
- required Python packages for Gemini mode:
  - `google-genai`
  - `Pillow`

Read [references/gemini-provider.md](references/gemini-provider.md) when the user wants the Gemini path.

## Best-Fit Requests

Use this skill when the user asks for any of the following:

- remove a status bar, top bar, bottom bar, subtitle strip, watermark, or floating control from a video
- clean a phone screen recording before reuse or clipping
- split a video into frames, repair masked regions, and rebuild it
- prepare a repeatable FFmpeg pipeline for video overlay removal
- use Gemini Nano Banana 2 to repair a masked overlay region frame by frame
- generate masks or region specs for known overlay areas

## Default Strategy

Choose the lightest path that can work:

1. Fixed overlay, stable region: use `ffmpeg` with a generated mask and `removelogo`
2. Fixed region but `removelogo` quality is not enough: extract frames and run Gemini Nano Banana 2 on the masked area
3. Dynamic overlay: extract frames, create or propagate masks, run Gemini Nano Banana 2, then rebuild the video

Do not default to full-frame generative editing when a fixed-region or deterministic method is enough.

## Workflow

### 1. Classify the overlay

Decide which of these cases applies:

- `fixed-edge-overlay`: top status bar, bottom nav bar, subtitle strip, corner logo
- `fixed-box-overlay`: stable watermark or floating widget in one area
- `dynamic-overlay`: notification banner, moving sticker, transient floating control
- `unknown`: the user has not yet provided enough detail to define a mask

If the overlay location is unclear, ask for the smallest missing detail needed, or propose a reasonable first mask and label it as a draft.

### 2. Pick the path

For `fixed-edge-overlay` or `fixed-box-overlay`, prefer the built-in scripts:

- `scripts/make_mask.py`
- `scripts/clean_video.sh --mode removelogo`

For Gemini-based workflows, use:

- `scripts/clean_video.sh --mode gemini-nano-banana`
- `scripts/gemini_nano_banana_edit.py`

For low-level or custom provider workflows, use:

- `scripts/extract_frames.sh`
- `scripts/restore_frames.py`
- `scripts/rebuild_video.sh`

Read [references/pipeline.md](references/pipeline.md) for the end-to-end flow, [references/mask-strategies.md](references/mask-strategies.md) for mask design guidance, and [references/gemini-provider.md](references/gemini-provider.md) for Gemini-specific behavior.

### 3. Build the mask carefully

Masks decide success. Keep these rules:

- Mask only the overlay, not the whole frame
- Prefer a slightly tight mask over an oversized one
- For fixed bars, use presets or percentage-based regions
- For dynamic overlays, keep the frame-edit scope local and explicit

Region format used by this skill is `x:y:w:h`.
Each value may be pixels like `120` or a percentage like `8%`.

Examples:

- Top 7 percent: `0:0:100%:7%`
- Bottom strip: `0:92%:100%:8%`
- Corner watermark: `78%:3%:18%:12%`

### 4. Run the cleanup path

#### Fast fixed-overlay path

Use when the overlay stays in one place.

```bash
bash scripts/clean_video.sh \
  --input /abs/path/input.mp4 \
  --output /abs/path/output.mp4 \
  --mode removelogo \
  --region '0:0:100%:7%'
```

You can also add presets:

```bash
bash scripts/clean_video.sh \
  --input /abs/path/input.mp4 \
  --output /abs/path/output.mp4 \
  --mode removelogo \
  --preset iphone-status-bar
```

#### Gemini Nano Banana 2 path

Use when the user wants masked per-frame restoration.

```bash
export GEMINI_API_KEY='your_api_key_here'

bash scripts/clean_video.sh \
  --input /abs/path/input.mp4 \
  --output /abs/path/output.mp4 \
  --mode gemini-nano-banana \
  --region '0:0:100%:12%' \
  --image-size 1K
```

Optional model override:

```bash
bash scripts/clean_video.sh \
  --input /abs/path/input.mp4 \
  --output /abs/path/output.mp4 \
  --mode gemini-nano-banana \
  --region '0:0:100%:12%' \
  --model gemini-3.1-flash-image-preview \
  --image-size 2K
```

#### Custom frame-edit path

Use only when the user explicitly wants a custom editor command instead of Gemini.

```bash
bash scripts/clean_video.sh \
  --input /abs/path/input.mp4 \
  --output /abs/path/output.mp4 \
  --mode frame-edit \
  --region '0:0:100%:12%' \
  --editor-cmd 'my-editor --input {input} --mask {mask} --output {output}'
```

The editor command receives:

- `{input}`: source frame path
- `{mask}`: mask path
- `{output}`: destination frame path
- `{index}`: zero-based frame number

### 5. Be explicit about limits

Always note when one of these is true:

- the hidden content was never visible in any frame
- the result is a visual reconstruction rather than factual recovery
- the overlay is dynamic and the mask is approximate
- frame-by-frame edits may need temporal stabilization beyond this first pass
- Gemini may vary slightly frame to frame, especially on large masked regions
- Gemini mode now reports frame count, base cost estimate, and cumulative token/spend progress while running
- Gemini mode now preserves all unmasked pixels from the original frame at save time, so only masked regions are adopted from model output

## Known Limitations

Keep the risk statement simple:

- masked or covered areas are not restored reliably every time
- the result is a plausible visual cleanup, not guaranteed true recovery
- Gemini processing can be expensive, especially on longer videos or higher frame counts

## Current Reliability Notes

The current Gemini implementation uses several safeguards:

- budget estimation before processing begins
- cumulative token and spend reporting during processing
- per-frame validation and retry
- request-level retry for transient provider errors
- masked compositing that keeps all unmasked pixels from the original frame

That last safeguard is important: if the model edits the hamster, cage, or other visible scene content outside the white mask, the saved output still keeps the original unmasked pixels. This improves visual stability, but it also means all useful edits must happen inside the supplied mask.

## Output Expectations

A good result includes:

- the cleaned video path
- the chosen method: `removelogo`, `gemini-nano-banana`, or `frame-edit`
- the exact mask or presets used
- whether `GEMINI_API_KEY` was required
- the frame count that Gemini mode planned to process
- the base estimated spend before Gemini calls began
- the cumulative token and spend summary reported during processing
- any important caveats about realism, consistency, or residual artifacts

When useful, also keep the work directory so the user can inspect:

- extracted frames
- generated mask files
- rebuilt intermediate video
- job manifest

## Quality Bar

- Prefer stable, repeatable cleanup over ambitious but noisy edits
- Avoid editing untouched parts of the frame
- Use deterministic FFmpeg paths first
- Treat generative editing as a targeted fallback, not the default
- Separate `cleaner-looking` from `factually restored`
- Remind the user when a provider API key is required

## Prompt Patterns

Good invocations:

- "Use $video-overlay-cleanup to remove the top status bar from this screen recording."
- "Use $video-overlay-cleanup with Gemini Nano Banana 2 to clean the top banner from this video."
- "Use $video-overlay-cleanup to split this video into frames, clean the floating overlay, and rebuild it."

For implementation details, load:

- [references/pipeline.md](references/pipeline.md)
- [references/mask-strategies.md](references/mask-strategies.md)
- [references/gemini-provider.md](references/gemini-provider.md)
- [references/provider-integration.md](references/provider-integration.md)
