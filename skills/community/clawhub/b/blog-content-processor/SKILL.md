---
name: blog-content-processor
description: Process blog content to extract videos and generate GIF previews. Works with blogwatcher, video-frames, and gifgrep skills.
tags: ['blog', 'video', 'gif', 'content', 'processing']
---

# Blog Content Processor

Extracts video content from blog/RSS feeds and generates GIF preview clips.

## Features

- Parses RSS/Atom feeds via `rss-parser`
- Extracts embedded video URLs from blog entries
- Generates GIF previews from video segments using `ffmpeg-static`
- Integrates with blogwatcher, video-frames, and gifgrep skills

## Usage

```bash
node index.js --feed <rss-url> --output ./gifs
```

## Dependencies

- `rss-parser` ^3.12.0
- `ffmpeg-static` ^5.1.0
