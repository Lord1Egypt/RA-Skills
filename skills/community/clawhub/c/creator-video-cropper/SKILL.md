---
name: video-cropper
description: Crop videos to focus on the most important area for social, ecommerce, ads, and storefront use without making the result look clumsy. Use when the frame includes wasted space, wrong composition, or unnecessary edges.
---

# Video Cropper

Crop the frame so attention stays on what matters.

## Problem it solves
A video can be technically fine but compositionally wrong for the job: too much empty space, distracting edges, irrelevant background, or a subject that needs to fill the frame better. This skill helps tighten framing for platform use and better viewer focus.

## Use when
- The subject is too small in frame
- The edges contain distracting or unnecessary information
- The user wants a tighter product, face, or demo crop
- The same source needs cleaner framing for social or ecommerce placement

## Do not use when
- The subject moves too much for static crop logic
- Intelligent motion tracking is required
- Resize or compression is the real problem, not framing

## Inputs
- Source video file
- Area to preserve: face, hands, product, subtitles, full object, etc.
- Target use case or platform
- Desired framing style: tight, balanced, or conservative

## Workflow
1. Identify what should remain in frame.
2. Remove wasted or distracting space.
3. Keep the crop useful for platform context and subject readability.
4. Export the tighter composition.
5. Flag when a static crop may fail because subject motion is too large.

## Output
Return:
1. Chosen crop focus
2. Framing rationale
3. Output fit for the target use case
4. Risks if motion may leave the crop area

## Quality bar
- Preserve the true subject, not just the geometric center
- Avoid awkward amputations of hands, products, or subtitles
- Prefer useful framing over maximum zoom-in
- Warn when static crop is likely to break on motion-heavy footage

## Resource
See `references/output-template.md`.
