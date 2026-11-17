---
name: markdown-to-minimal-image
description: >
  Read an attached Markdown document, analyze and summarize it, then generate a
  minimalist image from the summary using the default image model. Ask the user
  for aspect ratio when needed, and support social-banner formats such as 5:2
  and 5:4. Use when the user wants a document turned into a simple tutorial-style
  visual with handwritten whiteboard aesthetics.
version: 1.0.0
author: Jeff Yang (https://github.com/j3ffyang)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [image-generation, markdown, summary, whiteboard, social-banner]
    requires_toolsets: [file]
    requires_tools: []
    required_environment_variables: []
---

# Markdown to Minimal Image

## When to Use

Use this skill when the user provides a Markdown document and wants:
- A concise summary of the document.
- One generated image based on that summary.
- A specific aspect ratio for social media or hero banners.
- A minimalist, handwritten, whiteboard-like visual style.

## When NOT to Use

Do NOT use this skill for:
- Generating photorealistic images or detailed illustrations.
- Creating multi-image documents or slide decks.
- Processing non-Markdown file formats (PDF, Word, plain text without conversion).
- Tasks where the user explicitly requests a different visual style (photography, 3D rendering, oil painting).
- Generating images without a source document to summarize.

## Inputs

- `document` — Attached Markdown file to read and analyze.
  - Required: yes
  - Type: file (`.md`)
- `aspect_ratio` — Desired image aspect ratio, e.g. `5:2`, `5:4`, `16:9`, `1:1`.
  - Required: no
  - Type: string
  - Default: none (user will be prompted)
- `color_scheme` — Color scheme for the image, e.g. `black-and-white`, `blue accent`, `warm beige`, `pastel`.
  - Required: no
  - Type: string
  - Default: neutral minimalist palette

## Outputs

- `summary` — String. 3–5 bullet points or one short paragraph summarizing the document.
- `image` — Generated image object. Exactly one image in the requested aspect ratio and color scheme.
- `image_path` — String. File path where the image is saved: `$HOME/.hermes/cache/{date}-{subject}.png`.
- `aspect_ratio` — String. The aspect ratio used for generation (resolved from input or user prompt).
- `color_scheme` — String. The color scheme used for generation (resolved from input or default).

## Procedure

1. Read the attached Markdown document using file tools.
2. Detect the document language. If the document is in Simplified Chinese, all output (summary, image text) must be in Simplified Chinese. If English, all output must be in English.
3. Identify the core topic, key ideas, and actionable points.
4. Summarize the document in 3–5 short bullets or one short paragraph.
5. If `aspect_ratio` is missing, ask the user for it before proceeding. Accept only valid ratios (5:2, 5:4, 16:9, 1:1, or a custom ratio the user specifies).
6. If `color_scheme` is missing, ask the user or default to a neutral minimalist palette.
7. Build an image prompt from the summary that incorporates the aspect ratio, color scheme, and whiteboard-tutorial style.
8. Generate exactly one image using the default image generation model.
9. Save the generated image to `$HOME/.hermes/cache/{date}-{subject}.png`.
10. Call `present_files` to surface the saved image to the user.
11. Return the summary alongside the image.

## Verification

- The summary must be non-empty and accurately reflect the source document.
- The generated image must match the requested aspect ratio exactly.
- The generated image must use the requested color scheme (or default).
- The image style must be minimalist, whiteboard-like, with handwritten text — not photorealistic or cluttered.
- The language of the image text must match the source document language (English or Simplified Chinese).

## Error Handling

- **Missing document:** If no Markdown file is attached, inform the user and halt.
- **Invalid aspect ratio:** If the user provides an unsupported ratio, list valid options and ask again.
- **Image generation failure:** If the model fails to produce an image, retry once with a simplified prompt. If still failing, report the error and suggest a different model or lower resolution.
- **Unreadable document:** If the file cannot be parsed as Markdown, inform the user and request a valid `.md` file.

## Style Notes

- Handwritten tutorial on whiteboard.
- Minimalist composition with clean layout.
- Simple color palette matching the requested scheme.
- Low resolution acceptable for social media or hero-banner use.
- Prefer simple diagrams, arrows, boxes, labels, and short notes.
- Avoid heavy detail, photorealism, or decorative clutter.

## Supported Aspect Ratios

- 5:2 — social banner
- 5:4 — social banner
- 16:9 — hero / widescreen
- 1:1 — square / social post
- Custom ratios accepted on request