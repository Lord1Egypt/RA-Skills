---
name: fast-image
description: Quickly send local images to channel. Auto-compress large images, copy small images directly.
metadata:
  {
    "openclaw": {
      "keywords": ["image", "send image", "media", "photo", "send"],
    },
  }
---

# fast-image

Quickly send local images to specified channel. Auto-handles image copy/compress and send.

## Usage

```
node {baseDir}/send_image.mjs "<image_path>" <channel> <target> [message]
```

## Parameters

| Parameter | Description | Required |
|-----------|-------------|----------|
| `image_path` | Full path to image | Yes |
| `channel` | Target channel name | Yes |
| `target` | Target user/group | Yes |
| `message` | Optional message | No |

## Features

1. Image processing
   - File < 10MB: Copy directly to `~/.openclaw/media/browser/`
   - File >= 10MB: Compress with sharp then copy

2. Send: Use `openclaw message send --media` to send

3. Cleanup: Auto-delete temp file after sending

## Examples

```
node {baseDir}/send_image.mjs "~/Pictures/photo.png" telegram @chatname
node {baseDir}/send_image.mjs "~/Downloads/large.jpg" telegram @chatname "landscape"
```

## Dependencies

- Node.js
- sharp: `npm install sharp`
- openclaw CLI
