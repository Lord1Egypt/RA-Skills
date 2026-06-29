---
name: codia-product-assets
description: Use when the user asks for ecommerce or product launch asset packs, product listing images, store banners, catalog tiles, marketplace visuals, or multiple product marketing images from product photos.
---

# codia-product-assets

Create a coherent product or ecommerce asset set by orchestrating Codia image analysis, cleanup, background replacement, variation, reframing, upscaling, and optional editable design extraction.

## When To Use

Use this skill for:

- Product launch image sets
- Ecommerce listing images
- Store banners and catalog tiles
- Product scene variations from one source product photo
- Marketplace-ready product assets across several ratios

For a single background removal, use `codia-remove-bg`. For a single generated image with no product source, use `codia-image-generate`.

## Inputs To Collect

- Source product image path or URL
- Target channels or ratios, such as square tile, 4:5 card, 9:16 story, 16:9 banner, or marketplace-specific size
- Desired background directions, such as white studio, lifestyle scene, seasonal campaign, or transparent
- Output directory
- Any product details that must stay unchanged

## Workflow

1. Use `codia-design` setup/auth guidance if the CLI is missing or not authenticated.
2. Run `codia-image-describe` on the source product image to capture product identity, materials, colors, visible text, and constraints to preserve.
3. Use `codia-remove-bg` for transparent or isolated product assets.
4. Use `codia-image-object-erase` only for user-owned or authorized cleanup, such as removing dust, props, clutter, or defects.
5. Use `codia-image-replace-bg` for white studio, lifestyle, seasonal, and campaign backgrounds.
6. Use `codia-image-remix` when the user wants several campaign directions while preserving the product.
7. Use `codia-image-reframe` for each target channel or aspect ratio.
8. Use `codia-image-upscale` on final selected assets.
9. Use `codia-image-to-design` or `codia-image-layering` if the user needs editable downstream design data.

## Output

Return a compact manifest with:

- Asset name
- Intended use
- Aspect ratio or size
- Local file path
- Remote URL when available
- Model or important parameter choices

Also report any skipped asset, failed task, or user decision that still needs confirmation.
