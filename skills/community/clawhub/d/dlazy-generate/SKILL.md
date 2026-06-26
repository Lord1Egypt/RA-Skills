---
name: dlazy-generate
version: 1.2.0
description: A comprehensive generation skill. Can generate images, videos, and audio by automatically selecting the appropriate dlazy CLI model.
metadata:
  {
    'clawdbot':
      {
        'emoji': '🤖',
        'requires': { 'bins': ['npm', 'npx'] },
        'install': 'npm install -g @dlazy/cli@1.2.0',
        'installAlternative': 'npx @dlazy/cli@1.2.0',
        'homepage': 'https://github.com/dlazyai/cli',
        'source': 'https://github.com/dlazyai/cli',
        'author': 'dlazyai',
        'license': 'see-repo',
        'npm': 'https://www.npmjs.com/package/@dlazy/cli',
        'configLocation': '~/.dlazy/config.json',
        'apiEndpoints': ['api.dlazy.com', 'files.dlazy.com'],
      },
    'openclaw': { 'systemPrompt': 'When this skill is called, use dlazy <subcommand>.' },
  }
---

# dlazy-generate

[English](./SKILL.md) · [中文](./SKILL-cn.md)

A comprehensive generation skill. Can generate images, videos, and audio by automatically selecting the appropriate dlazy CLI model.

## Trigger Keywords

- generate
- create image, video, audio
- multimodal generation

## Authentication

All requests require a dLazy API key. The recommended way to authenticate is:

````bash

This runs a device-code flow (also works in remote shells) and **automatically saves your API key** to the local CLI config — no manual copy/paste required.

### Alternative: Set the Key Manually

If you already have an API key, you can save it directly:

```bash
dlazy auth set YOUR_API_KEY
````

The CLI saves the key in your user config directory (`~/.dlazy/config.json` on macOS/Linux, `%USERPROFILE%\.dlazy\config.json` on Windows), with file permissions restricted to your OS user account. You can also supply the key per-invocation via the `DLAZY_API_KEY` environment variable.

### Getting Your API Key Manually

1. Sign in or create an account at [dlazy.com](https://dlazy.com)
2. Go to [dlazy.com/dashboard/organization/api-key](https://dlazy.com/dashboard/organization/api-key)
3. Copy the key shown in the API Key section

Each key is scoped to your dLazy organization and can be **rotated or revoked at any time** from the same dashboard.

## About & Provenance

- **CLI source code**: [github.com/dlazyai/cli](https://github.com/dlazyai/cli)
- **Maintainer**: dlazyai
- **npm package**: `@dlazy/cli` (pinned to `1.0.9` in this skill's install spec)
- **Homepage**: [dlazy.com](https://dlazy.com)

You can install on demand without persisting a global binary by running:

```bash
npx @dlazy/cli@1.2.0 <command>
```

Or, if you prefer a global install, the skill's `metadata.clawdbot.install` field declares the exact pinned version (`npm install -g @dlazy/cli@1.2.0`). Review the GitHub source before installing.

## How It Works

This skill is a thin client over the dLazy hosted API. When you invoke it:

- Prompts and parameters you provide are sent to the dLazy API endpoint (`api.dlazy.com`) for inference.
- Any local file paths you pass to image / video / audio fields are uploaded to dLazy's media storage (`files.dlazy.com`) so the model can read them — the same flow as any cloud-based generation API.
- Generated output URLs returned by the API are hosted on `files.dlazy.com`.

This is the standard SaaS pattern; the skill itself does not access network or filesystem resources beyond what the dLazy CLI already handles. See [dlazy.com](https://dlazy.com) for the full service terms.

## Piping Between Commands

Every `dlazy` invocation prints a JSON envelope on stdout. Any flag value can be a **pipe reference** that pulls from the upstream command's envelope, so you can chain steps without copying URLs by hand.

| Reference           | Resolves to                                                       |
| ------------------- | ----------------------------------------------------------------- |
| `-`                 | Upstream's natural value for this field (scalar or array)         |
| `@N`                | The N-th output's primary value (e.g. `@0` = first output url)    |
| `@N.<jsonpath>`     | Drill into the N-th output (`@0.url`, `@1.meta.fps`)              |
| `@*`                | All outputs' primary values as an array                           |
| `@stdin`            | The whole upstream JSON envelope                                  |
| `@stdin:<jsonpath>` | Jsonpath into the whole envelope (`@stdin:result.outputs[0].url`) |

### Examples

```bash
# Generate an image and feed its url straight into image-to-video
dlazy seedream-4.5 --prompt "a red fox in snow" \
  | dlazy kling-v3 --image - --prompt "fox starts running"

# Generate an image, then add TTS narration over a still
dlazy seedream-4.5 --prompt "lighthouse at dawn" \
  | dlazy keling-tts --text "Welcome to the coast." --image @0.url

# Fan-out: pass every upstream output url into a batch step
dlazy seedream-4.5 --prompt "city skyline" --n 4 \
  | dlazy superres --images @*
```

> Required flags can be entirely sourced from the pipe — `--field -` satisfies the requirement when an upstream value exists. If stdin is empty, the CLI fails with `code: "no_stdin"`.

## Usage

This is a comprehensive skill that routes generation requests to the appropriate `dlazy` model based on the user's intent.

### Available Models by Category

**Image Generation:**

- `dlazy banana-pro`: High-quality text-to-image model (optional 1 reference image). Good for detailed key visuals, product shots, and brand-style imagery.
- `dlazy banana2`: General text-to-image model (optional 1 reference image), prioritizing speed and cost. Good for quick drafts, social posts, and multi-ratio generation.
- `dlazy gpt-image-2`: GPT Image 2 model for text-to-image and image editing. Supports generating images from text as well as editing and synthesizing images with reference inputs.
- `dlazy grok-4.2`: Minimalist text-to-image model, prompt-only. Good for quick concept validation or undemanding instant generation.
- `dlazy image-replicate`: Image replicate tool: analyzes the source's composition, color, lighting, and style, then uses Seedream 4.5 to generate a new image in the same style.
- `dlazy imageseg`: Image matting tool: separates foreground and returns a transparent-background URL. Good for product images, cutouts, and compositing.
- `dlazy jimeng-t2i`: Jimeng high-res text-to-image model with multi-ratio ultra-HD output and reference-image constraints. Good for commercial visuals and refined output.
- `dlazy kling-image-o1`: Kling image model, supports '<image_1>' placeholder in prompt for reference image binding. Suitable for multi-image constraints and high-fidelity generation.
- `dlazy mj-imagine`: Midjourney style generation, supports aspect ratio, Bot type, and output position (grid/U1-U4). Suitable for artistic and strongly stylized creative generation.
- `dlazy qwen-image-2-pro`: Alibaba Bailian qwen-image-2.0-pro general image generation. Excels at complex text rendering, multi-line layout, photorealistic detail, and strong semantic adherence — great for mixed text/image designs.
- `dlazy recraft-v4`: 1MP raster image generation with refined design judgment. Suitable for everyday creative work and fast iteration.
- `dlazy recraft-v4-pro`: 4MP high-resolution raster image generation. Suitable for print-ready assets and large-scale use.
- `dlazy recraft-v4-pro-vector`: High-fidelity text-to-vector model, 4MP-tier quality. Good for production SVG assets and detailed illustrations.
- `dlazy recraft-v4-vector`: Text-to-vector model that outputs SVG results. Suitable for logos, icons, and scalable design assets.
- `dlazy seedream-4.5`: High-quality text-to-image/image-to-image model, suitable for posters, realism, and creative scenes. Supports prompt + multiple reference images, outputting single high-res images (2K/4K).
- `dlazy seedream-5.0-lite`: Lightweight high-speed image generation model, suitable for batch generation, sketches, and low-cost iteration. Supports prompt + reference images, outputting 2K/3K images.
- `dlazy superres`: Image super-resolution tool: enhances image clarity and details, returning enhanced URL, suitable for low-res asset restoration and upscaling.
- `dlazy viduq2-t2i`: Vidu image model with text + reference image, ratio, and resolution control. Good for character art, covers, and high-res output.

**Video Generation:**

- `dlazy happyhorse-1.0`: Happy Horse 1.0 video model — one model covers text-to-video (t2v), first-frame-to-video (i2v), reference-to-video (r2v), and video editing (edit). The selected mode is automatically routed to the matching sub-model.
- `dlazy heygen-lipsync-speed`: HeyGen Lipsync Speed: Fast lip-sync model, ideal for scenarios requiring rapid generation.
- `dlazy jimeng-dream-actor`: Jimeng character/action-driven video model, supports reference image and video input, suitable for character acting, action transfer, and style-consistent generation.
- `dlazy jimeng-i2v-first`: Jimeng first-frame-to-video model, uses first frame + text to generate video. Suitable for single-shot scenes that naturally animate static images.
- `dlazy jimeng-i2v-first-tail`: Jimeng first/last-frame video model; constrains shot start/end frames. Good for transitions and clearly resolved action.
- `dlazy jimeng-omnihuman-1.5`: Jimeng digital human model: combines any-ratio character/subject image with audio to generate high-quality digital human videos.
- `dlazy kling-v3`: Kling V3 general video model, supports text + up to 4 reference images, suitable for stable short video clips and daily creative workflows.
- `dlazy kling-v3-omni`: Kling Omni video model, supports multiple reference images, duration, mode (std/pro), and optional audio. Suitable for highly controlled video synthesis tasks.
- `dlazy pixverse-c1`: PixVerse C1 video model (strong on action, VFX, and high-motion scenes) — one model covers text-to-video, image-to-video, first/last-frame-to-video, and reference-to-video: t2v when no images, i2v with first frame only, kf2v with first+last frames, r2v with reference images.
- `dlazy seedance-2.0`: ByteDance's latest video generation model. Supports multi-modal reference (images, video, audio) to generate videos, as well as first/last frame and text-to-video modes.
- `dlazy seedance-2.0-fast`: Fast version of ByteDance's Seedance 2.0. Generates videos faster with support for multi-modal references, first/last frame, and text-to-video.
- `dlazy sync-lipsync-3`: fal.ai sync-lipsync v3 — given an input video and audio, generate a new video where the speaker's lip movement matches the audio. Good for dubbing, localization, and re-syncing virtual presenters.
- `dlazy veo-3.1`: High-quality video generation model, supports text-to-video and single-image-driven video. Suitable for ad shorts and cinematic sequences (slower speed, higher quality).
- `dlazy veo-3.1-fast`: Fast video generation model, supports text-to-video and single/multi-image/first-last frame driven. Suitable for time-sensitive previews and rapid iterations.
- `dlazy video-replicate`: Video replicate tool: extracts the first frame and audio from the source video, runs video understanding for a prompt, and returns a Seedance 2.0 replicate bundle (first frame + audio + video).
- `dlazy videoretalk`: Tongyi VideoRetalk lip sync / lip-sync (mouth sync, dubbing) video model — takes a talking-person video plus a voice audio track and regenerates the video so the speaker's mouth/lips match the new audio. Use this for lip syncing a person video to new speech. Optionally provide a reference face image to pick the target person when the video contains multiple faces.
- `dlazy videoseg`: Video human segmentation tool: invokes Aliyun's async SegmentVideoBody and returns a same-length black/white mask video, suitable for downstream compositing or matting.
- `dlazy viduq2-i2v`: Vidu image-to-video model, supports reference image-driven video, duration/resolution/ratio, and audio settings, suitable for image animation and short clips.
- `dlazy wan2.7`: Tongyi Wanxiang 2.7 video model — one model covers text-to-video, first/last-frame-to-video, and reference-to-video: uses text-to-video when no images are provided, first/last-frame-to-video when frames are provided, and reference-to-video when reference images are supplied.

**Audio Generation:**

- `dlazy doubao-tts`: ByteDance Doubao speech synthesis model. Supports multiple languages, voices, and highly natural streaming audio output, suitable for news broadcasts and audiobooks.
- `dlazy elevenlabs-dialogue`: ElevenLabs eleven_v3 multi-voice dialogue: assign a different voice per line (up to 10) and render the whole conversation in one shot. Supports audio tags like [giggling], [whispers] — great for character dialogue, podcasts, and short skits. Before picking a voice, you can search for the right one via elevenlabs-search.
- `dlazy elevenlabs-music`: ElevenLabs music_v1 model — generates 10–300s original music from a natural-language prompt. Good for BGM, ads, and short-video soundtracks.
- `dlazy elevenlabs-search`: Search the ElevenLabs voice library by keyword, source, and category. Returns a playable preview for each matched voice so you can pick the right one before running TTS.
- `dlazy elevenlabs-sfx`: ElevenLabs text-to-sound model — generates 1–22s short sound effects from a description. Suitable for foley, ambience, alerts, and game SFX.
- `dlazy elevenlabs-tts`: ElevenLabs eleven_v3 text-to-speech with 12 curated multilingual voices and stability/similarity/style controls. Great for dubbing, audiobooks, and character dialog. Before picking a voice, you can search for the right one via elevenlabs-search.
- `dlazy elevenlabs-voice-clone`: ElevenLabs Instant Voice Cloning (IVC). Upload a clean voice sample to clone a custom voice usable with ElevenLabs TTS.
- `dlazy gemini-2.5-tts`: Gemini-powered high-quality text-to-speech. Supports bilingual (EN/CN) and various emotional voices.
- `dlazy keling-sfx`: Sound effect generation model: supports text-to-SFX and matching SFX/BGM for reference videos. Suitable for foley, ambient sounds, and short video audio completion.
- `dlazy keling-tts`: Text-to-speech model (TTS), supports language, voice, speed, and output format settings. Suitable for dubbing, audiobooks, and voice broadcasts.
- `dlazy kling-audio-clone`: Custom voice (Kling), cloned voice used for dubbing or binding to subjects.
- `dlazy qwen-audio-clone`: Alibaba Bailian qwen3-tts voice cloning. Upload a clean voice sample to clone a custom voice usable in subsequent TTS calls.
- `dlazy qwen-tts`: Alibaba Bailian qwen3-tts text-to-speech. Choose from curated system voices (including dialects) or design a custom voice from a natural-language description.
- `dlazy suno-music`: Suno V5.5 music generation. Inspiration mode (auto lyrics) or custom mode (manual style/title/lyrics). Generates music with or without vocals, with fine-grained controls over style weight, weirdness and audio weight.
- `dlazy vidu-audio-clone`: Clone a real human voice and use it to read the specified text.

**CRITICAL INSTRUCTION FOR AGENT**:

1. Determine the media type (image, video, or audio) requested by the user.
2. Select the most appropriate model from the list above.
3. Run `dlazy <model_name> -h` to check the required parameters for that specific model.
4. Execute the command (e.g., `dlazy seedream-4.5 --prompt "..."`).

## Error Handling

| Code | Error Type                         | Example Message                                                                                                          |
| ---- | ---------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| 401  | Unauthorized (No API Key)          | `ok: false, code: "unauthorized", message: "API key is missing or invalid"`                                              |
| 501  | Missing required parameter         | `error: required option '--prompt <prompt>' not specified`                                                               |
| 502  | Local file read error              | `Error: Image file/Video file not found: C:\path\to\your\file`                                                           |
| 503  | API request failed (no balance)    | `ok: false, code: "insufficient_balance"`                                                                                |
| 503  | API request failed (server error)  | `HTTP status code error (500 server crash)`                                                                              |
| 504  | Asynchronous task execution failed | `=== Generation Failed ===` / `{Specific error reason returned by backend, for example "Prompt violates safety policy"}` |

> **AGENT CRITICAL INSTRUCTION**:
>
> 1. If the execution result returns `code: "insufficient_balance"`, you MUST explicitly inform the user that their credits are insufficient and guide them to recharge: [https://dlazy.com/dashboard/organization/settings?tab=credits](https://dlazy.com/dashboard/organization/settings?tab=credits)
> 2. If the execution result returns `code: "unauthorized"` or indicates missing API key, you MUST inform the user to get their API key from [https://dlazy.com/dashboard/organization/api-key](https://dlazy.com/dashboard/organization/api-key) and save it using `dlazy auth set <key>` and resume the task.

## Tips

Visit https://dlazy.com for more information.
