---
name: alibaba-super-resolution
description: "Enhance video resolution using Alibaba Cloud Super Resolution API. Use when the user wants to: (1) upscale low-res videos to higher resolution, (2) improve video quality before publishing, or (3) convert 480p videos to 1080p."
version: 1.0.0
category: media-processing
argument-hint: "[input video] [output video]"
license: MIT
---

# Alibaba Cloud Super Resolution (阿里云视频超分辨率)

Enhance video resolution using Alibaba Cloud's video super resolution API, converting low-resolution videos to higher resolution (e.g., 480p → 960p).

## Prerequisites

Set the following environment variables for authentication:

```bash
export ALIBABA_CLOUD_ACCESS_KEY_ID="your-access-key-id"
export ALIBABA_CLOUD_ACCESS_KEY_SECRET="your-access-key-secret"
```

### Optional OSS Configuration (for large files)

For files larger than 2GB or when using OSS directly:

```bash
export ALIYUN_OSS_BUCKET="your-bucket-name"
export ALIYUN_OSS_ENDPOINT="oss-cn-shanghai.aliyuncs.com"
```

## Execution (Python CLI Tool)

A Python CLI tool is provided at `~/.openclaw/workspace/skills/alibaba-super-resolution/alibaba_super_resolve.py`.

### Quick Examples

```bash
# Basic usage: local file → local HD file
python3 ~/.openclaw/workspace/skills/alibaba-super-resolution/alibaba_super_resolve.py \
  --input videos/input-480p.mp4 \
  --output videos/output-960p.mp4

# Custom bit rate (higher = better quality, larger file)
python3 ~/.openclaw/workspace/skills/alibaba-super-resolution/alibaba_super_resolve.py \
  --input videos/input-480p.mp4 \
  --output videos/output-960p.mp4 \
  --bit-rate 8

# Do not wait for completion (return job ID immediately)
python3 ~/.openclaw/workspace/skills/alibaba-super-resolution/alibaba_super_resolve.py \
  --input videos/input-480p.mp4 \
  --no-wait

# Check status of an existing job
python3 ~/.openclaw/workspace/skills/alibaba-super-resolution/alibaba_super_resolve.py \
  --status <JOB_ID>

# Wait for an existing job and download result
python3 ~/.openclaw/workspace/skills/alibaba-super-resolution/alibaba_super_resolve.py \
  --wait <JOB_ID> \
  --output videos/output-960p.mp4
```

## Input Requirements

### Video Files

- **Formats**: MP4, MOV, AVI, MKV
- **Max Size**: 2GB (direct upload) / No limit (OSS URL)
- **Max Duration**: 30 minutes
- **Input Resolutions**: 480p, 720p

### Output Resolutions

| Input | Output |
|-------|--------|
| 480p | 960p (2x upscale) |
| 720p | 2K (2x upscale) |

## Bit Rate Settings

| Bit Rate | Quality | File Size | Processing Time | Use Case |
|----------|---------|-----------|-----------------|----------|
| 1-3 | Low | Small | Fast | Preview/Testing |
| 4-6 | Medium | Medium | Medium | Social Media |
| 7-10 | High | Large | Slow | HD Publishing |

## Rules

1. **Always check** that credentials are configured before making API calls.
2. **Files over 2GB** must use OSS URL instead of direct upload.
3. **Default bit rate**: 5 (balanced quality/size).
4. **Default timeout**: 1200 seconds (20 minutes).
5. **Download immediately** - output URLs expire after 24 hours.
6. **Handle errors gracefully** - display clear error messages.

## Troubleshooting

### VideoTooLarge

**Error**: `File exceeds 2GB limit`

**Fix**: Use OSS URL instead of direct upload

### Timeout

**Error**: `Task timed out`

**Fix**: Increase timeout parameter: `--timeout 1800` (30 minutes)

### OSSAccessDenied

**Error**: `OSSAccessDenied`

**Fix**: Verify RAM permissions for the access key, ensure it has OSS read/write access.

## Related Documents

- [Alibaba Cloud Super Resolution Docs](https://help.aliyun.com/zh/viapi/developer-reference/api-w2n4j6)
