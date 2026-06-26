# Ark Video API Notes

Endpoint:

`POST https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks`

## What this reference is for

Use this file to document the exact request payload, required headers, auth method, and response parsing once they are finalized.

## Minimum details to fill before production use

- Authorization method
- Required headers
- Request body schema
- Required model field: `"model": "doubao-seedance-1-5-pro-251215"`
- Required content field, for example:
  ```json
  "content": [{"type": "text", "text": "your prompt here"}]
  ```
- Required ratio field, currently defaulted to `"16:9"`
- Required duration field, currently validated with `5`
- Optional / recommended watermark field, currently defaulted to `false`
- Image reference field names (when user provides reference images, they appear as local file paths in the conversation; upload to a CDN or use base64 data URI, then reference in `content` array as `{"type": "image", "image": "<url>"}`)
- Response path for task ID
- Retry / backoff rules

## Execution rule

Submit each segment sequentially and store the returned task identifier for each segment.

## Query Task Result

GET `https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks/{id}`

Example response fields used by this skill:
- `status`
- `content.video_url`
- `id`

This skill only needs the final `video_url` once the task reaches `succeeded`.

## Recommended Full Flow

1. If images are provided, first confirm the role of each image with the user
2. Confirm storyboard and prompts with the user
3. Ask for explicit execution approval if the user has not already requested direct generation
4. Submit the current segment generation task
5. Check whether submission returned a valid task ID
6. If submission fails or no task ID is returned, immediately surface the error to the user and stop
7. If submission succeeds, continue silently to the next segment by default
8. Only after all segments are successfully submitted should you notify the user that generation is underway
9. Poll task status until `succeeded`
10. Extract `content.video_url`
11. **Download the video to `~/.openclaw/media/YYYYMMDDHHMMSS/`** (one directory per video task)
12. Only after the current segment was successfully submitted should you continue to the next segment

## API Key Source

Current script fallback order:
1. Environment variable `ARK_API_KEY`
2. `~/.openclaw/openclaw.json` → `skills.entries.ark-video-storyboard.apiKey`
3. Backward-compatible old format: `skills.ark-video-storyboard.apiKey`

## Video Download Behavior

When extracting `video_url` from a succeeded task, **automatically download** the video:

- Output directory: `~/.openclaw/media/YYYYMMDDHHMMSS/`
- Example: `~/.openclaw/media/20260318152844/`
- Each video task gets its own timestamped directory
- Files are named sequentially: `seg1.mp4`, `seg2.mp4`, ..., or use meaningful names

Use the script:
```bash
python3 scripts/download_video.py "<video_url>" --output "seg1.mp4"
```

The script automatically creates the dated directory. Use `--dir` to specify a shared output directory for all segments so they end up in the same folder (important when submitting multiple segments in parallel):

```bash
# First create the shared directory (once per task)
OUTDIR=$(date +%Y%m%d%H%M%S)
mkdir -p ~/.openclaw/media/$OUTDIR

# Then pass it to every download call
python3 scripts/download_video.py "$VIDEO_URL" --output "seg1.mp4" --dir ~/.openclaw/media/$OUTDIR
python3 scripts/download_video.py "$VIDEO_URL" --output "seg2.mp4" --dir ~/.openclaw/media/$OUTDIR
python3 scripts/download_video.py "$VIDEO_URL" --output "seg3.mp4" --dir ~/.openclaw/media/$OUTDIR
``` The download will be placed at:
`~/.openclaw/media/{timestamp}/seg{N}.mp4`
