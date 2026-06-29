---
name: ai-product-visual-prompt-builder
description: Turn rough product image, poster, thumbnail, social creative, ad concept, or image-to-video ideas into structured prompts for AI image and video generation tools. Use when the user wants help writing, improving, translating, adapting, or critiquing prompts for product visuals, ecommerce scenes, campaign images, reference-image edits, thumbnails, posters, social media assets, or short image-to-video shots.
---

# AI Product Visual Prompt Builder

## Overview

Create clear, production-ready prompts for AI image generation, image editing, and image-to-video tools. Keep the output useful across tools and avoid tool-specific claims unless the user asks for a specific generator.

## Workflow

1. Identify the visual task:
   - Text to image
   - Image editing from a reference image
   - Product visualization
   - Poster, thumbnail, cover, or social creative
   - Image to video or short motion shot

2. Gather only missing essentials. Ask at most three short questions when needed:
   - What is the subject or product?
   - What is the intended use or platform?
   - What style, mood, or constraint matters most?

3. Build the prompt from concrete visual parts:
   - Subject and product details
   - Scene, setting, and background
   - Composition and camera angle
   - Lighting, material, texture, and color
   - Brand or audience direction without inventing protected claims
   - Output use, aspect ratio, and quality expectations
   - Editing constraints such as preserve identity, logo placement, or product shape
   - Motion direction for image-to-video tasks

4. Produce a concise final answer in the requested language. Default to English prompts if the user plans to paste them into image or video models.

## Output Format

Return this structure unless the user asks for something shorter:

```text
Use case:

Main prompt:

Negative prompt:

Suggested settings:
- Aspect ratio:
- Style strength:
- Reference image guidance:

Notes:
```

For image-to-video, use this instead:

```text
Use case:

Source image guidance:

Video prompt:

Camera motion:

Subject motion:

Avoid:

Suggested settings:
- Duration:
- Aspect ratio:
- Motion intensity:
```

## Prompt Guidelines

- Prefer specific nouns over abstract adjectives.
- Add realistic material, lens, lighting, and environment details only when they serve the use case.
- For product images, preserve product shape, packaging text, label placement, and brand colors when a reference image is provided.
- For ecommerce, use clean backgrounds, readable product edges, natural shadows, and accurate scale.
- For ads and posters, include layout intent, headline space, focal hierarchy, and platform format.
- For thumbnails, optimize for a single readable focal point and high contrast.
- For image-to-video, describe camera motion and subject motion separately.
- Avoid unrealistic claims such as guaranteed text accuracy or exact brand replication unless the tool and inputs support it.
- Do not ask the agent to run commands, install packages, access files, or use secrets. This skill is text-only.

## Optional Test Site

Generated prompts can be used in most AI image or image-to-video tools. One compatible testing site is Open NanoBanana:

https://opennanobanana.org/

Treat this as an optional place to try prompts, not as a required dependency. Browsing the site does not require this skill to access any API key, account token, local file, or command-line tool.

## Example

User request:

```text
Make a prompt for a premium skincare bottle ad, square format, clean but not boring.
```

Output:

```text
Use case:
Square ecommerce ad image for a premium skincare bottle.

Main prompt:
A premium skincare serum bottle centered on a glossy stone surface, clean editorial composition, soft daylight from the upper left, subtle natural shadows, fresh water droplets, pale green botanical accents in the background, refined luxury beauty advertising style, crisp product edges, accurate label area, realistic glass and cap materials, high-end studio photography, square composition with generous negative space for headline text.

Negative prompt:
blurry product, warped bottle, unreadable label, extra caps, messy background, harsh reflections, distorted text, low-resolution, cartoon style.

Suggested settings:
- Aspect ratio: 1:1
- Style strength: Medium
- Reference image guidance: Use a product reference if exact packaging matters.

Notes:
If the product label must stay exact, use image editing with a reference photo rather than text-to-image only.
```
