---
name: auto-video-creator
description: AI-powered video generator using XLXAI Sora2 API. Create professional videos from text prompts or images in seconds.
---

# Auto Video Creator - XLXAI Video Generation Skill

Generate professional videos from text prompts or images using the XLXAI Sora2 API.

## Scope

This skill focuses exclusively on video generation:
- ✅ Calls XLXAI Sora2 API to generate videos
- ✅ Returns task/result JSON with video URL upon completion
- ✅ Supports text-to-video and image-to-video generation
- ❌ Does NOT upload, post, or proxy videos to TikTok or other platforms
- ❌ Does NOT handle social media publishing

For upload/post functionality, use a separate skill (e.g., post-to-tiktok-getlate) or downstream workflow.

## Quick Start

### 1. Setup Environment

```bash
cp skills/xlxai-video/.env.example skills/xlxai-video/.env
# Edit skills/xlxai-video/.env and set XLXAI_API_KEY
export XLXAI_API_KEY="$YOUR_KEY"
```

### 2. Generate Video

```bash
python3 skills/xlxai-video/scripts/generate_video.py "Your video prompt here" --model sora2-portrait-4s
```

The script loads the API key from the XLXAI_API_KEY environment variable, handles task creation and polling, and returns JSON with the video URL when complete.

## API Response Examples

### Task Creation Response (no-wait)

```json
{
  "task_id": "task_Ue8FsGswnj3fCaY91yAj84m8AA8lLVpm",
  "status": "pending",
  "model": "sora2-portrait-4s",
  "created_at": "2026-03-03T18:19:30Z"
}
```

### Completed Task Response

```json
{
  "task_id": "task_Ue8FsGswnj3fCaY91yAj84m8AA8lLVpm",
  "status": "completed",
  "video_url": "https://api.xlxai.store/video2-proxy/base/video/79193b56b4792daec07c5564bff412f193a6c20e5ee7ca0a323ab753da2420a9.mp4",
  "progress": 100,
  "duration": 38,
  "message": "Generation complete",
  "created_at": "2026-03-03T18:19:30Z",
  "completed_at": "2026-03-03T18:20:08Z"
}
```

**Notes:**
- Field names depend on XLXAI API version; inspect raw JSON for actual fields
- video_url may point to third-party CDN; download and self-host if needed

## Video Models

Choose based on your needs:

### Portrait Models (Vertical Videos)
- `sora2-portrait-4s` — 4-second vertical video (default)
- `sora2-portrait-8s` — 8-second vertical video
- `sora2-portrait-12s` — 12-second vertical video

### Landscape Models (Horizontal Videos)
- `sora2-landscape-4s` — 4-second horizontal video
- `sora2-landscape-8s` — 8-second horizontal video
- `sora2-landscape-12s` — 12-second horizontal video

**Default:** `sora2-portrait-4s`

## Usage Patterns

### Text-to-Video Generation

Generate videos from text descriptions:

```bash
python3 scripts/generate_video.py "A 30-year-old American man in a suit presenting to camera" \
  --model sora2-landscape-8s
```

### Image-to-Video Generation

Create videos from images with motion (local images auto-converted to data URI):

```bash
python3 scripts/generate_video.py "Man showcasing the suit, saying it's well-made and affordable" \
  --model sora2-portrait-4s \
  --image "/path/to/local/image.jpg"
```

Or use image URLs directly:

```bash
python3 scripts/generate_video.py "Man showcasing the suit, saying it's well-made and affordable" \
  --model sora2-portrait-4s \
  --image "http://example.com/image.jpg"
```

### Non-blocking Task Creation

Get task ID immediately without waiting for completion:

```bash
python3 scripts/generate_video.py "Your prompt" --no-wait
```

Check status later:

```bash
python3 scripts/generate_video.py --check-status task_abc123
```

## Script Options

| Option | Description | Default |
|--------|-------------|---------|
| `--model` | Video model (portrait/landscape, 4s/8s/12s) | sora2-portrait-4s |
| `--image` | Image URL or local file path | — |
| `--no-wait` | Return task ID immediately | false |
| `--poll-interval` | Seconds between status checks | 10 |
| `--timeout` | Max seconds to wait for completion | 600 |
| `--check-status` | Check status of existing task | — |

## Output Format

On success, the script returns JSON with:
- `status`: "completed"
- `video_url`: Download link for the generated video
- `progress`: 100
- `duration`: Generation time in seconds
- `task_id`: Unique task identifier
- `created_at`: Task creation timestamp
- `completed_at`: Task completion timestamp

## Error Handling

The script handles:
- ✅ API request failures with retry logic
- ✅ Timeout after 600 seconds (configurable)
- ✅ Progress reporting during generation
- ✅ Clear error messages for failed tasks
- ✅ HTTP status code validation

## Important Notes

- **Copyright & Rights**: Verify copyright and portrait rights before publishing generated content
- **API Key Security**: Keep your API key secret; use environment variables in production
- **Video URL**: May point to third-party CDN; download and self-host if needed
- **Rate Limits**: Check XLXAI API documentation for rate limiting

---

## 日本語ガイド

### セットアップ

```bash
cp skills/xlxai-video/.env.example skills/xlxai-video/.env
export XLXAI_API_KEY="$YOUR_KEY"
```

### ビデオ生成

```bash
python3 skills/xlxai-video/scripts/generate_video.py "あなたのプロンプト" --model sora2-portrait-4s
```

### 画像からビデオを生成

```bash
python3 skills/xlxai-video/scripts/generate_video.py "シーンの説明" --image "/path/to/image.jpg"
```

---

## 한국어 가이드

### 설정

```bash
cp skills/xlxai-video/.env.example skills/xlxai-video/.env
export XLXAI_API_KEY="$YOUR_KEY"
```

### 비디오 생성

```bash
python3 skills/xlxai-video/scripts/generate_video.py "당신의 프롬프트" --model sora2-portrait-4s
```

### 이미지에서 비디오 생성

```bash
python3 skills/xlxai-video/scripts/generate_video.py "장면 설명" --image "/path/to/image.jpg"
```

---

## Contact / 連絡先 / 연락처

- **Email**: yefl2064@gmail.com
- **Telegram**: [@kuajintontu](https://t.me/kuajintontu)