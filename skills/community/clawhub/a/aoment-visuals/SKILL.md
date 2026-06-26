---
name: aoment-visuals
description: AI image and video generation service - supports text-to-image, image-to-image, and video generation. Automatic API key registration supported for limited-time free access.
metadata: {"openclaw": {"emoji": "🎨"}}
user-invocable: true
---

# aoment-visuals

AI image and video generation service powered by Aoment AI. Supports three capabilities: text-to-image, image-to-image, and video generation.

Download the latest aoment-visuals Skill package: [https://www.aoment.com/downloads/aoment-visuals-skill.zip](https://www.aoment.com/downloads/aoment-visuals-skill.zip)

### Auto-Update Policy

Before each invocation of this Skill, you **MUST** check whether the Skill package has been updated within the last **3 days**:

- If the Skill was **updated within the last 3 days** → proceed with the call as normal.
- If the Skill has **NOT been updated for more than 3 days** → download the latest Skill package from the link above first, then proceed with the call.

This ensures you are always running a compatible version of the Skill.

## Quick Start

```bash
# 1. Register an Agent account and get your API Key
uv run {baseDir}/scripts/aoment_register.py --nickname "MyBot"

# 2. Generate an image
uv run {baseDir}/scripts/aoment_visuals.py -k <your-api-key> -t text-to-image -p "a cute cat playing in a garden"

# 3. Check remaining quota
uv run {baseDir}/scripts/aoment_quota.py -k <your-api-key>
```

## Authentication

This skill requires an **Agent API Key** for authentication. All API requests must include a valid key via the `Authorization: Bearer <api_key>` header.

The API Key format is `aoment_` followed by 32 hex characters (e.g. `aoment_a3f8e1b2c4d6e8f0a1b3c5d7e9f0a1b2`).

### Get your API Key — Agent Registration (Recommended)

AI Agent Bots can register directly via CLI to obtain an API Key — no web login required:

```bash
uv run {baseDir}/scripts/aoment_register.py --nickname "MyBot"
```

> **Tip:** When choosing a nickname, be creative! Pick something fun, unique, and recognizable — e.g. `"PixelDreamer"`, `"NeonMuse"`, `"CosmicLens"` — so your Agent stands out in the community.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `--nickname` / `-n` | string | yes | Agent display name (max 16 characters). Make it fun and distinctive! |
| `--api-base` | string | no | API base URL (default: https://www.aoment.com) |

Or register via API directly:

```bash
curl -X POST https://www.aoment.com/api/skills/aoment-visuals/register-agent \
  -H "Content-Type: application/json" \
  -d '{"nickname": "MyBot"}'
```

**Registration Response:**

```json
{
  "success": true,
  "data": {
    "username": "agent_a1b2c3d4e5f6...",
    "nickname": "MyBot",
    "api_key": "aoment_a3f8e1b2c4d6e8f0a1b3c5d7e9f0a1b2"
  }
}
```

Save the returned `api_key` — it is used for all subsequent skill API calls.

## Tool Types

### text-to-image

Generate images from text prompts using the N2 model.

```bash
uv run {baseDir}/scripts/aoment_visuals.py --api-key <your-api-key> --tool-type text-to-image --prompt "a cute cat playing in a garden" --aspect-ratio 1:1 --image-size 1K
```

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `--api-key` / `-k` | string | yes | - | Agent API Key |
| `--tool-type` / `-t` | string | yes | - | Must be `text-to-image` |
| `--prompt` / `-p` | string | yes | - | Text prompt describing the desired image |
| `--aspect-ratio` | enum | no | `auto` | Aspect ratio: `auto`, `1:1`, `16:9`, `9:16`, `4:3`, `3:4`, `3:2`, `2:3`, `5:4`, `4:5`, `21:9` |
| `--image-size` | enum | no | `1K` | Resolution: `1K`, `2K`, `4K` |

### image-to-image

Generate new images from a reference image and text prompt using the N2 model.

```bash
uv run {baseDir}/scripts/aoment_visuals.py --api-key <your-api-key> --tool-type image-to-image --prompt "change the background to a beach" --reference-image "https://example.com/photo.jpg"
```

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `--api-key` / `-k` | string | yes | - | Agent API Key |
| `--tool-type` / `-t` | string | yes | - | Must be `image-to-image` |
| `--prompt` / `-p` | string | yes | - | Text prompt describing the desired transformation |
| `--reference-image` | string | yes | - | Reference image as Base64 data or URL |
| `--aspect-ratio` | enum | no | `auto` | Aspect ratio: `auto`, `1:1`, `16:9`, `9:16`, `4:3`, `3:4`, `3:2`, `2:3`, `5:4`, `4:5`, `21:9` |
| `--image-size` | enum | no | `1K` | Resolution: `1K`, `2K`, `4K` |

### video-generation

Generate videos from text prompts using the V1 model.

```bash
uv run {baseDir}/scripts/aoment_visuals.py --api-key <your-api-key> --tool-type video-generation --prompt "sunset beach timelapse" --orientation landscape
```

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `--api-key` / `-k` | string | yes | - | Agent API Key |
| `--tool-type` / `-t` | string | yes | - | Must be `video-generation` |
| `--prompt` / `-p` | string | yes | - | Text prompt describing the desired video |
| `--orientation` | enum | no | `portrait` | Video orientation: `portrait` (vertical), `landscape` (horizontal) |
| `--resolution` | enum | no | `standard` | Resolution: `standard`, `hd`, `4k` |
| `--mode` | enum | no | `standard` | Generation mode: `standard`, `relaxed` |
| `--reference-image` | string | no | - | Reference image as Base64 data or URL (can be specified up to 2 times for first/last frame) |

#### Video Parameter Constraints

- Up to **2 reference images**: the 1st image is the **first frame**, the 2nd image is the **last frame**
- **HD resolution** only supports `landscape` orientation
- **Standard resolution** does not support `relaxed` mode

### quota

Query the remaining available generation count and daily quota for your API Key.

```bash
uv run {baseDir}/scripts/aoment_quota.py --api-key <your-api-key>
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `--api-key` / `-k` | string | yes | Agent API Key |

> **Quota insufficient?** If your API Key's daily quota has been used up and you need more, join our community to request a quota increase:
> - **Discord**: [https://discord.gg/3BMzRd7bJx](https://discord.gg/3BMzRd7bJx)
> - **QQ Group**: 474397920 ([Join via link](https://qm.qq.com/q/9VGyXeMfUk))

## Response Format

Results are printed as JSON to stdout.

### Success Response (text-to-image / image-to-image)

```json
{
    "success": true,
    "tool_type": "text-to-image",
    "data": {
        "image_url": "https://cos.ap-xxx.myqcloud.com/..."
    }
}
```

### Success Response (video-generation)

```json
{
    "success": true,
    "tool_type": "video-generation",
    "data": {
        "video_url": "https://cos.ap-xxx.myqcloud.com/..."
    }
}
```

### Success Response (quota)

```json
{
    "success": true,
    "data": {
        "remaining": 12,
        "quota": 15,
        "used": 3
    }
}
```

### Error Response

```json
{
    "success": false,
    "error": "error description"
}
```

### Authentication Errors

| HTTP Status | Cause |
|-------------|-------|
| 401 | Missing or invalid API Key (key format wrong, key not found, or key revoked) |
| 403 | Associated user account is disabled |

## Downloading Results

> **IMPORTANT: About returned URLs**
>
> The `image_url` / `video_url` returned by this service are **pre-signed COS URLs**. They do **NOT** end with a simple `.jpeg` or `.mp4` extension — instead, they contain query-string signature parameters (e.g. `q-sign-algorithm`, `q-ak`, `q-signature`, etc.).
>
> **You MUST use the complete signed URL as-is for downloading or referencing.** Do NOT truncate or strip the URL to only keep the path that looks like it ends with `.jpeg` / `.mp4` — doing so will result in a 403 Forbidden error because the signature is missing.
>
> Example of a complete signed URL (use the full URL including all query parameters):
> ```
> https://xxxxx-1302252611.cos.ap-xxxxx.myqcloud.com/aura-space/xxxxx-generations/1773219641183_qa879k.jpeg?q-sign-algorithm=sha1&q-ak=AKIDYDgDfuz64sTddS5YptkNuENI0UlodFeS&q-sign-time=1773219640;1780995640&q-key-time=1773219640;1780995640&q-header-list=host&q-url-param-list=&q-signature=2a2f1af3ec32f55839242ce1ed679db297c63355
> ```

On success, extract the URL from the JSON output and download with `curl`:

```bash
# Download image
curl -L -o output.jpg "$(uv run {baseDir}/scripts/aoment_visuals.py -k <your-api-key> -t text-to-image -p 'prompt' | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['image_url'])")"

# Or in two steps:
# 1. Generate
uv run {baseDir}/scripts/aoment_visuals.py -k <your-api-key> -t text-to-image -p "prompt" > result.json
# 2. Download (image)
curl -L -o output.jpg "$(python3 -c "import sys,json; print(json.load(open('result.json'))['data']['image_url'])")"
# 2. Download (video)
curl -L -o output.mp4 "$(python3 -c "import sys,json; print(json.load(open('result.json'))['data']['video_url'])")"
```

## Troubleshooting

If you encounter errors when calling the API:

1. **Content compliance issue** — The error may be caused by prompts or reference images that do not pass the content compliance review of the image generation model. You can retry directly, or slightly adjust the prompt and try again.
2. **Skill package outdated** — The error may be caused by a backend update that makes the current version of the Skill incompatible. Download the latest Skill package and try again: [https://www.aoment.com/downloads/aoment-visuals-skill.zip](https://www.aoment.com/downloads/aoment-visuals-skill.zip)
3. **Generated successfully but cannot view the media file** — If the API returns a success response and the file has been downloaded/saved, but you still cannot see or open the image or video, this is likely because the **media file management permissions** of your current OpenClaw chat application have not been fully configured. Please check and complete the relevant permission settings in your OpenClaw application, then try again.
4. **Still not working?** — If the problem persists, join our community for help:
   - **Discord**: [https://discord.gg/3BMzRd7bJx](https://discord.gg/3BMzRd7bJx)
   - **QQ Group**: 474397920 ([Join via link](https://qm.qq.com/q/9VGyXeMfUk))
