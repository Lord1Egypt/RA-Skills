---
name: video-resizer
description: Resize video outputs for social, ecommerce, ads, and platform uploads without stretching the subject or breaking compatibility. Use when a video needs new dimensions, aspect ratio handling, or size-specific exports.
---

# Video Resizer

Resize videos for the platform they actually need to fit.

## Problem it solves
One video rarely fits every platform. Teams need the same source adapted for vertical short-form, square ads, storefront slots, review links, and lightweight previews. This skill turns one source into correctly sized outputs without careless stretching or amateur-looking results.

## Use when
- A video needs to fit TikTok, Reels, Shorts, Shopify, Amazon, PDP, ads, or internal review formats
- A user needs 9:16, 1:1, 4:5, 16:9, or platform-specific dimensions
- A team wants quick resized variants from one source

## Do not use when
- The user needs intelligent reframing of moving subjects beyond simple resize/crop strategy
- The source composition is fundamentally wrong and needs manual editing

## Inputs
- Source video file
- Target aspect ratio or platform
- Whether to pad, crop, or scale to fit
- Optional output resolution and file size constraints
- Priority area to preserve: face, product, subtitles, or full frame

## Workflow
1. Clarify the target platform and dimension requirement.
2. Decide whether scale, pad, or crop is the right strategy.
3. Preserve the most important visual area.
4. Export one or multiple platform-ready sizes.
5. Explain any framing tradeoffs.

## Output
Return:
1. Chosen resize strategy
2. Output dimensions
3. Framing notes
4. Compatibility notes
5. Optional additional recommended sizes

## Quality bar
- Never stretch people or products unnaturally
- Preserve readable text whenever possible
- Prefer platform-safe dimensions over custom vanity sizes
- Make crop vs pad tradeoffs obvious

## Resource
See `references/output-template.md`.
