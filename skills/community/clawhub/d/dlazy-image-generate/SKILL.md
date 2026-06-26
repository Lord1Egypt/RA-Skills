---
name: dlazy-image-generate
version: 1.2.0
description: Image generation skill. Automatically selects the best dlazy CLI image model based on the prompt.
metadata:
  {
    'clawdbot':
      {
        'emoji': '🤖',
        'requires': { 'bins': ['npm', 'npx'] },
        'install': 'npm install -g @dlazy/cli@latest',
        'installAlternative': 'npx @dlazy/cli@latest',
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

# dlazy-image-generate

[English](./SKILL.md) · [中文](./SKILL-cn.md)

Image generation skill. Automatically selects the best dlazy CLI image model based on the prompt.

## Trigger Keywords

- generate image
- draw picture
- text to image

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
npx @dlazy/cli@latest <command>
```

Or, if you prefer a global install, the skill's `metadata.clawdbot.install` field declares the exact pinned version (`npm install -g @dlazy/cli@latest`). Review the GitHub source before installing.

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

This skill handles all image generation requests by selecting the best `dlazy` image model.

### Available Image Models

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

**CRITICAL INSTRUCTION FOR AGENT**:

1. Select the most appropriate image model.
2. Run `dlazy <model_name> -h` to check parameters.
3. Execute the command.

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
