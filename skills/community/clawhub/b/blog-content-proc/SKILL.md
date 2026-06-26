---
name: blog-content-processor
description: Process blog content to extract videos and generate GIF previews. Works with blogwatcher, video-frames, and gifgrep skills.
---

# Blog Content Processor

Extracts videos from blog/RSS feeds and generates GIF previews for quick scanning.

## Usage

1. Feed a blog URL or RSS feed
2. The processor extracts embedded video URLs
3. Generates lightweight GIF previews from video frames

## Dependencies

- `rss-parser` — parse RSS/Atom feeds
- `ffmpeg-static` — video frame extraction and GIF generation

## Compatible Skills

- **blogwatcher** — feed monitoring
- **video-frames** — frame extraction
- **gifgrep** — GIF search and sharing
