---
name: dlazy-detect
version: 1.0.5
description: "Detect whether an image, video, or audio file is AI-generated — including visual deepfakes and the likely generator model (Midjourney, Stable Diffusion, Sora, etc.). Returns confidence scores you can threshold. 检测图片、视频或音频是否由 AI 生成：包含人脸 deepfake 识别与疑似生成模型归因，返回可用于判定的置信度分数。"
metadata:
  {
    'clawdbot':
      {
        'emoji': '🔍',
        'requires': { 'bins': ['npm', 'npx'] },
        'install': 'npm install -g @dlazy/cli@1.2.3',
        'installAlternative': 'npx @dlazy/cli@1.2.3',
        'homepage': 'https://github.com/dlazy-ai/cli',
        'source': 'https://github.com/dlazy-ai/cli',
        'author': 'dlazyai',
        'license': 'see-repo',
        'npm': 'https://www.npmjs.com/package/@dlazy/cli',
        'configLocation': '~/.dlazy/config.json',
        'apiEndpoints': ['api.dlazy.com', 'files.dlazy.com'],
      },
    'openclaw': { 'systemPrompt': 'When invoking this skill, use dlazy detect -h for help.' },
  }
---

# AI 内容检测 AI Detect

[English](./SKILL.md) · [中文](./SKILL-cn.md)

Detect whether an image, video, or audio file is AI-generated — including visual deepfakes and the likely generator model (Midjourney, Stable Diffusion, Sora, etc.). Returns confidence scores you can threshold.

## Trigger Keywords

- detect
- ai-detect
- ai-generated
- deepfake
- is this AI

## What It Detects

- **Image / Video**: whether the visual is AI-generated (`ai_generated` score), whether it contains a **deepfake** (face swap), and the **likely generator** (Midjourney, Stable Diffusion, DALL·E, etc.).
- **Audio** (audio-only files, or the audio track of a video): whether the audio is AI-generated (`ai_generated_audio` score).
- **Text is NOT supported** by this model — image, video, and audio only.

> Recommended decision threshold: treat as AI-generated when the score is **≥ 0.9**. The skill already applies this to the `is_ai_generated` / `is_deepfake` booleans.
>
> Note: the underlying provider (Hive V3 Playground) has a default rate limit of **100 requests/day**.

## Authentication

All requests require a dLazy API key. The recommended way to authenticate is:

```bash
dlazy login
```

This runs a device-code flow (also works in remote shells) and **automatically saves your API key** to the local CLI config — no manual copy/paste required.

### Alternative: Set the Key Manually

```bash
dlazy auth set YOUR_API_KEY
```

The CLI saves the key in your user config directory (`~/.dlazy/config.json` on macOS/Linux, `%USERPROFILE%\.dlazy\config.json` on Windows). You can also supply the key per-invocation via the `DLAZY_API_KEY` environment variable.

### Getting Your API Key Manually

1. Sign in or create an account at [dlazy.com](https://dlazy.com)
2. Go to [dlazy.com/dashboard/organization/api-key](https://dlazy.com/dashboard/organization/api-key)
3. Copy the key shown in the API Key section

## How It Works

This skill is a thin client over the dLazy hosted API. When you invoke it:

- **Each `--image_url` / `--video_url` / `--audio_url` accepts EITHER a local file path OR a public URL — the CLI detects which automatically.** No need to upload first or convert anything; just pass whatever you have.
  - **Local file** (e.g. `./photo.jpg`, `C:\clip.mp4`): the CLI uploads it to dLazy's media storage (`files.dlazy.com`) and forwards the resulting URL.
  - **Public URL** (e.g. `https://example.com/a.png`): passed through as-is. The URL must be publicly reachable — links behind login/auth or on a private network can't be fetched by the detection service.
- The media is analyzed and a structured verdict (AI-generated confidence, deepfake confidence, likely generator) is returned.

## Usage

**CRITICAL INSTRUCTION FOR AGENT**:
Run `dlazy detect` with exactly ONE of `--image_url`, `--video_url`, or `--audio_url`.

```bash
dlazy detect -h

Options:
  --image_url [image_url]              Image to check (local path or public URL)
  --video_url [video_url]              Video to check (local path or public URL)
  --audio_url [audio_url]              Audio to check (local path or public URL)
  --dry-run                            Print payload + cost estimate without calling API
  --no-wait                            Return generateId immediately for async tasks
  --timeout <seconds>                  Max seconds to wait for async completion (default: "1800")
  -h, --help                           display help for command
```

> Any flag also accepts pipe references — `-` (auto-pick from upstream stdin), `@N` (n-th output), `@N.path` (jsonpath into output), `@*` (all primary values), `@stdin` / `@stdin:path` (whole envelope). See `dlazy --help` for details.

## Output Format

```json
{
  "ok": true,
  "result": {
    "tool": "detect",
    "modelId": "detect",
    "outputs": [
      {
        "type": "json",
        "id": "o_xxxxxxxx",
        "value": {
          "media_type": "image",
          "is_ai_generated": true,
          "ai_generated_score": 0.98,
          "not_ai_generated_score": 0.02,
          "is_deepfake": false,
          "deepfake_score": 0.03,
          "top_generator": "midjourney",
          "top_generator_score": 0.91,
          "ai_generated_audio_score": 0.0,
          "frames_analyzed": 1
        }
      }
    ]
  }
}
```

A human-readable summary is also returned in the task's `texts`, e.g. `疑似 AI 生成（AI 置信度 98%，疑似 midjourney）；未检出 deepfake`.

> Async tasks (when `--no-wait` is passed) return `outputs: []` and a `task: { generateId, status }` field instead. Use `dlazy status <generateId> --wait` to poll.

## Examples

```bash
# Check a local image
dlazy detect --image_url ./photo.jpg

# Check a video (AI-generation + deepfake)
dlazy detect --video_url ./clip.mp4

# Check an audio clip (AI voice)
dlazy detect --audio_url ./voice.mp3

# Check by public URL
dlazy detect --image_url https://example.com/a.png
```

## Error Handling

| Code | Error Type                         | Example Message                                                                                                          |
| ---- | ---------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| 401  | Unauthorized (No API Key)          | `ok: false, code: "unauthorized", message: "API key is missing or invalid"`                                              |
| 501  | Missing required parameter         | `Provide one of image_url, video_url, or audio_url`                                                                      |
| 502  | Local file read error              | `Error: Image file/Video file not found: C:\path\to\your\file`                                                           |
| 503  | API request failed (no balance)    | `ok: false, code: "insufficient_balance"`                                                                                |
| 503  | API request failed (rate limited)  | `HTTP status code error (429 too many requests)` — Hive V3 allows 100 requests/day                                       |
| 504  | Asynchronous task execution failed | `=== Generation Failed ===` / `{Specific error reason returned by backend}`                                              |

> **AGENT CRITICAL INSTRUCTION**:
>
> 1. If the result returns `code: "insufficient_balance"`, you MUST tell the user their credits are insufficient and guide them to recharge: [https://dlazy.com/dashboard/organization/settings?tab=credits](https://dlazy.com/dashboard/organization/settings?tab=credits)
> 2. If the result returns `code: "unauthorized"` or indicates a missing API key, you MUST tell the user to get their API key from [https://dlazy.com/dashboard/organization/api-key](https://dlazy.com/dashboard/organization/api-key) and save it with `dlazy auth set <key>`, then resume the task.

## Tips

Visit https://dlazy.com for more information.
