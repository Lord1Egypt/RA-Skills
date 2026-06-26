---
name: creator-video-compressor
description: Compress videos for creators, ecommerce teams, and ad operators while balancing file size, upload compatibility, and visual quality. Use when a video is too large to upload, send, publish, or archive efficiently.
---

# Creator Video Compressor

Reduce video file size without turning the result into blurry garbage.

## Problem it solves
Creators and ecommerce teams constantly hit upload limits, slow sending, bloated storage, and platform rejection because video files are too large or encoded poorly. This skill turns oversized videos into smaller, platform-ready outputs while preserving practical clarity.

## Use when
- A video is too large for TikTok, Reels, Shorts, Shopify, Amazon, email, or chat upload
- A team needs lighter exports for review, handoff, or archive
- You want to shrink batch exports before publishing or sharing
- Upload speed matters and the original file is overkill

## Do not use when
- The goal is cinematic mastering or premium final delivery
- The user needs frame-by-frame restoration or AI enhancement
- The source is already heavily compressed and visibly degraded

## Inputs
- Source video file
- Target platform or use case
- Preferred balance: smaller size, better quality, or balanced
- Optional target cap: max file size, resolution, bitrate, duration
- Whether to preserve audio quality or reduce aggressively

## Workflow
1. Identify the real constraint: upload limit, transfer speed, archive, or platform compatibility.
2. Pick a compression profile based on platform and quality tolerance.
3. Reduce bitrate, adjust resolution only if needed, and keep codecs widely compatible.
4. Preserve clarity where it matters most: face, product, text, subtitles, demo motion.
5. Return the compressed output with clear size/quality tradeoff notes.

## Output
Return:
1. Recommended compression approach
2. Output file profile
3. File size reduction summary
4. Quality-risk notes
5. Best next step if further reduction is needed

## Quality bar
- Prioritize practical watchability over technical perfection
- Avoid over-compressing text, captions, faces, and product detail
- Keep exports platform-safe and easy to upload
- Make tradeoffs explicit instead of hiding quality loss

## Resource
See `references/output-template.md`.
