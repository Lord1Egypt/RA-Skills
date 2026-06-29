---
name: codia-campaign-assets
description: Use when the user asks for campaign posters, marketing visuals, launch graphics, social creative sets, hero images, banners, or multi-size creative variants.
---

# codia-campaign-assets

Create campaign visuals and adapt the strongest direction into multiple variants and delivery sizes using Codia image generation, reference-based generation, remix, reframe, upscale, and optional editable design extraction.

## When To Use

Use this skill for:

- Posters, covers, hero images, banners, and launch graphics
- Social creative sets across several aspect ratios
- Multiple campaign directions from one brief or reference image
- Final asset adaptation for 1:1, 4:5, 9:16, 16:9, or banner placements

For a single prompt-to-image request, use `codia-image-generate`. For a single resize/adaptation, use `codia-image-reframe`.

## Inputs To Collect

- Campaign brief or prompt
- Reference image paths or URLs, if any
- Target placements or aspect ratios
- Desired number of variants
- Output directory
- Visual constraints, such as subject, style, brand colors, text restrictions, or negative constraints

## Workflow

1. Use `codia-design` setup/auth guidance if the CLI is missing or not authenticated.
2. Generate the first campaign direction with `codia-image-generate`, or use `codia-image-image-to-image` when the user provides references.
3. Keep the first prompt focused on subject, composition, lighting, style, output intent, and negative constraints. Avoid embedding important text in the bitmap unless the user explicitly asks for text.
4. Run `codia-image-describe` on the strongest candidate to capture the visual language before creating variants.
5. Use `codia-image-remix` for controlled alternatives, such as mood, audience, season, colorway, or copy-safe composition variants.
6. Use `codia-image-reframe` to adapt the selected visual into target ratios and placements.
7. Use `codia-image-upscale` for final delivery files.
8. Use `codia-image-to-design` when the user needs editable design data for the final poster, hero, or key adapted size.

## Output

Return a compact delivery table with:

- Asset name
- Variant or placement
- Aspect ratio or size
- Local file path
- Remote URL when available
- Notes about prompt, model, or important constraints

If the user asked for multiple creative directions, briefly identify the recommended direction and why it best fits the brief.
