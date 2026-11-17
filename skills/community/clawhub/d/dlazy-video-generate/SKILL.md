---
name: dlazy-video-generate
version: 1.4.6
description: "视频生成技能，AI 视频生成，文生视频、图生视频、图片转视频、首尾帧生成视频。根据提示词自动选择最佳视频生成模型（即梦、可灵、Veo、Seedance、万相、PixVerse、数字人、对口型）。Video generation skill that automatically selects the best dlazy CLI video model based on the prompt."
metadata: {"clawdbot":{"emoji":"🤖","requires":{"bins":["npm","npx"]},"install":"npm install -g @dlazy/cli@1.2.3","installAlternative":"npx @dlazy/cli@1.2.3","homepage":"https://github.com/dlazy-ai/cli","source":"https://github.com/dlazy-ai/cli","author":"dlazyai","license":"see-repo","npm":"https://www.npmjs.com/package/@dlazy/cli","configLocation":"~/.dlazy/config.json","apiEndpoints":["api.dlazy.com","files.dlazy.com"]},"openclaw":{"systemPrompt":"When this skill is called, use dlazy <subcommand>."}}
---

# 视频生成 Video Generate

[English](./SKILL.md) · [中文](./SKILL-cn.md)




Video generation skill. Automatically selects the best dlazy CLI video model based on the prompt.

## 中文说明 / Chinese Overview

视频生成技能：根据提示词自动选择最佳的视频生成模型并产出视频。支持文生视频、图生视频、图片转视频、首尾帧生成视频、参考图生成视频、数字人视频、视频对口型。

**中文触发关键词**：视频生成、AI 视频生成、文字生成视频、文生视频、图生视频、图片变视频、让图片动起来、一键生成视频、短视频生成、视频模型、即梦视频、可灵视频、Veo 视频、Seedance 视频、通义万相视频、PixVerse 视频、数字人视频、对口型、唇形同步。

## Trigger Keywords

- generate video
- text to video
- animate image

## Authentication

All requests require a dLazy API key. The recommended way to authenticate is `dlazy login`:

```bash
dlazy login
```

This runs a device-code flow (also works in remote shells) and **automatically saves your API key** to the local CLI config — no manual copy/paste required.

### Alternative: Set the Key Manually

If you already have an API key, you can save it directly:

```bash
dlazy auth set YOUR_API_KEY
```

The CLI saves the key in your user config directory (`~/.dlazy/config.json` on macOS/Linux, `%USERPROFILE%\.dlazy\config.json` on Windows), with file permissions restricted to your OS user account. You can also supply the key per-invocation via the `DLAZY_API_KEY` environment variable.

### Getting Your API Key Manually

1. Sign in or create an account at [dlazy.com](https://dlazy.com)
2. Go to [dlazy.com/dashboard/organization/api-key](https://dlazy.com/dashboard/organization/api-key)
3. Copy the key shown in the API Key section

Each key is scoped to your dLazy organization and can be **rotated or revoked at any time** from the same dashboard.




## About & Provenance

- **CLI source code**: [github.com/dlazy-ai/cli](https://github.com/dlazy-ai/cli)
- **Maintainer**: dlazyai
- **npm package**: `@dlazy/cli` (pinned to `1.2.3` in this skill's install spec)
- **Homepage**: [dlazy.com](https://dlazy.com)

You can install on demand without persisting a global binary by running:

```bash
npx @dlazy/cli@1.2.3 <command>
```

Or, if you prefer a global install, the skill's `metadata.clawdbot.install` field declares the exact pinned version (`npm install -g @dlazy/cli@1.2.3`). Review the GitHub source before installing.

## How It Works

This skill is a thin client over the dLazy hosted API. When you invoke it:

- Prompts and parameters you provide are sent to the dLazy API endpoint (`api.dlazy.com`) for inference.
- Any local file paths you pass to image / video / audio fields are uploaded to dLazy's media storage (`files.dlazy.com`) so the model can read them — the same flow as any cloud-based generation API.
- Generated output URLs returned by the API are hosted on `files.dlazy.com`.

This is the standard SaaS pattern; the skill itself does not access network or filesystem resources beyond what the dLazy CLI already handles. See [dlazy.com](https://dlazy.com) for the full service terms.

## Piping Between Commands

Every `dlazy` invocation prints a JSON envelope on stdout. Any flag value can be a **pipe reference** that pulls from the upstream command's envelope, so you can chain steps without copying URLs by hand.

| Reference          | Resolves to                                                     |
| ------------------ | --------------------------------------------------------------- |
| `-`                | Upstream's natural value for this field (scalar or array)       |
| `@N`               | The N-th output's primary value (e.g. `@0` = first output url)  |
| `@N.<jsonpath>`    | Drill into the N-th output (`@0.url`, `@1.meta.fps`)            |
| `@*`               | All outputs' primary values as an array                         |
| `@stdin`           | The whole upstream JSON envelope                                |
| `@stdin:<jsonpath>` | Jsonpath into the whole envelope (`@stdin:result.outputs[0].url`) |

### Examples

```bash
# Generate an image and feed its url straight into image-to-video
dlazy seedream-4.5 --prompt "a red fox in snow" \
  | dlazy kling-v3 --image - --prompt "fox starts running"

# Generate an image, then add TTS narration over a still
dlazy seedream-4.5 --prompt "lighthouse at dawn" \
  | dlazy qwen-tts --text "Welcome to the coast." --image @0.url

# Fan-out: pass every upstream output url into a batch step
dlazy seedream-4.5 --prompt "city skyline" --n 4 \
  | dlazy superres --images @*
```

> Required flags can be entirely sourced from the pipe — `--field -` satisfies the requirement when an upstream value exists. If stdin is empty, the CLI fails with `code: "no_stdin"`.

## Usage

This skill handles all video generation requests by selecting the best `dlazy` video model.

### Available Video Models

- `dlazy happyhorse-1.0`: Happy Horse 1.0 video model — one model covers text-to-video (t2v), first-frame-to-video (i2v), reference-to-video (r2v), and video editing (edit). The selected mode is automatically routed to the matching sub-model.
- `dlazy heygen-lipsync-speed`: HeyGen Lipsync Speed: Fast lip-sync model, ideal for scenarios requiring rapid generation.
- `dlazy jimeng-dream-actor`: Jimeng character/action-driven video model, supports reference image and video input, suitable for character acting, action transfer, and style-consistent generation.
- `dlazy jimeng-i2v-first`: Jimeng first-frame-to-video model, uses first frame + text to generate video. Suitable for single-shot scenes that naturally animate static images.
- `dlazy jimeng-i2v-first-tail`: Jimeng first/last-frame video model; constrains shot start/end frames. Good for transitions and clearly resolved action.
- `dlazy jimeng-omnihuman-1.5`: Jimeng digital human model: combines any-ratio character/subject image with audio to generate high-quality digital human videos.
- `dlazy kling-v3`: Kling V3 general video model. Supports text-to-video, first-frame, and first/last-frame generation. Suitable for stable short video clips and daily creative workflows.
- `dlazy kling-v3-omni`: Kling Omni video model, supports multiple reference images, duration, mode (std/pro), and optional audio. Suitable for highly controlled video synthesis tasks.
- `dlazy minimax-h3`: MiniMax Hailuo omni-modal video model with native stereo audio, producing 5-15 second clips at up to 2K. Supports text-to-video, first/last frame transitions and multi-asset references for character and scene consistency.
- `dlazy pixverse-c1`: PixVerse C1 video model (strong on action, VFX, and high-motion scenes) — one model covers text-to-video, image-to-video, first/last-frame-to-video, and reference-to-video: t2v when no images, i2v with first frame only, kf2v with first+last frames, r2v with reference images.
- `dlazy seedance-2.0`: ByteDance's latest video generation model. Supports multi-modal reference (images, video, audio) to generate videos, as well as first/last frame and text-to-video modes.
- `dlazy seedance-2.0-fast`: Fast version of ByteDance's Seedance 2.0. Generates videos faster with support for multi-modal references, first/last frame, and text-to-video.
- `dlazy seedance-2.5`: ByteDance's next-generation video model: up to 30 seconds per clip with native 4K, substantially better instruction following and long-form narrative. Supports multi-modal references (image + video + audio) and first/last frame control.
- `dlazy sync-lipsync-3`: fal.ai sync-lipsync v3 — given an input video and audio, generate a new video where the speaker's lip movement matches the audio. Good for dubbing, localization, and re-syncing virtual presenters.
- `dlazy veo-3.1`: High-quality video generation model, supports text-to-video and single-image-driven video. Suitable for ad shorts and cinematic sequences (slower speed, higher quality).
- `dlazy veo-3.1-fast`: Fast video generation model, supports text-to-video and single/multi-image/first-last frame driven. Suitable for time-sensitive previews and rapid iterations.
- `dlazy video-replicate`: Video replicate tool: extracts the first frame and audio from the source video, runs video understanding for a prompt, and returns a Seedance 2.0 replicate bundle (first frame + audio + video).
- `dlazy videoretalk`: Tongyi VideoRetalk lip sync / lip-sync (mouth sync, dubbing) video model — takes a talking-person video plus a voice audio track and regenerates the video so the speaker's mouth/lips match the new audio. Use this for lip syncing a person video to new speech. Optionally provide a reference face image to pick the target person when the video contains multiple faces.
- `dlazy videoseg`: Video human segmentation tool: invokes Aliyun's async SegmentVideoBody and returns a same-length black/white mask video, suitable for downstream compositing or matting.
- `dlazy viduq2-i2v`: Vidu image-to-video model, supports reference image-driven video, duration/resolution/ratio, and audio settings, suitable for image animation and short clips.
- `dlazy wan2.7`: Tongyi Wanxiang 2.7 video model — one model covers text-to-video, first/last-frame-to-video, and reference-to-video: uses text-to-video when no images are provided, first/last-frame-to-video when frames are provided, and reference-to-video when reference images are supplied.

**CRITICAL INSTRUCTION FOR AGENT**:

1. Select the most appropriate video model.
2. Run `dlazy <model_name> -h` to check parameters.
3. Execute the command.


## Error Handling

| Code | Error Type                         | Example Message                                                                                                          |
| ---- | ---------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| 401  | Unauthorized (No API Key)          | `ok: false, code: "unauthorized", message: "API key is missing or invalid"`                                                              |
| 501  | Missing required parameter         | `error: required option '--prompt <prompt>' not specified`                                                              |
| 502  | Local file read error              | `Error: Image file/Video file not found: C:\path\to\your\file`                                                          |
| 503  | API request failed (no balance)    | `ok: false, code: "insufficient_balance"` |
| 503  | API request failed (server error)  | `HTTP status code error (500 server crash)`                                                                             |
| 504  | Asynchronous task execution failed | `=== Generation Failed ===` / `{Specific error reason returned by backend, for example "Prompt violates safety policy"}` |

> **AGENT CRITICAL INSTRUCTION**: 
> 1. If the execution result returns `code: "insufficient_balance"`, you MUST explicitly inform the user that their credits are insufficient and guide them to recharge: [https://dlazy.com/dashboard/organization/settings?tab=credits](https://dlazy.com/dashboard/organization/settings?tab=credits)
> 2. If the execution result returns `code: "unauthorized"` or indicates missing API key, you MUST inform the user to get their API key from [https://dlazy.com/dashboard/organization/api-key](https://dlazy.com/dashboard/organization/api-key) and save it using `dlazy auth set <key>` and resume the task.

## Tips

Visit https://dlazy.com for more information.