---
name: video-downloader
description: Download videos from YouTube and other video platforms. Use when user needs to download videos for offline viewing, extract audio from videos, or save video metadata.
---

# Video Downloader

Download videos from YouTube and other platforms.

## Quick Start

```bash
# Download video
python scripts/download.py https://youtube.com/watch?v=xxx
```

## Usage

```bash
python scripts/download.py URL [OPTIONS]

Options:
  --output PATH     Output directory
  --format FORMAT   Video format (mp4, webm)
  --quality QUALITY Quality (best, 1080p, 720p, 480p)
  --audio-only     Extract audio only
  --list-formats   List available formats
```

## Examples

```bash
# Download video
python scripts/download.py "https://youtube.com/watch?v=xxx"

# Download as MP4
python scripts/download.py "URL" --format mp4

# Audio only
python scripts/download.py "URL" --audio-only

# List formats
python scripts/download.py "URL" --list-formats
```

## Supported Platforms

- YouTube
- Vimeo
- Twitter/X
- And more...

## Features

- Video downloading
- Audio extraction
- Quality selection
- Format conversion
- Metadata extraction
