---
name: brand-video-maker
description: >
  Brand Video Maker is an AI tool for replacing logos, packaging, product shots, and brand
  elements inside existing videos without reshooting. It helps marketing teams localize
  campaigns, swap branded assets, adapt visuals for different markets, and generate new brand
  videos from winning source footage. 品牌视频替换、Logo 替换、包装替换、营销素材本地化。
---

# Brand Video Maker

> Replace brand elements in any video — swap logos, product packaging, text overlays, and brand colors while preserving the original footage quality and motion. Perfect for brand collaboration, white-label content, and product placement campaigns.

## What This Skill Does

Brand Video Maker uses AI inpainting and image-to-video generation to seamlessly replace brand elements in existing videos. Unlike simple overlay tools, it understands scene context — handling reflections, shadows, and perspective changes on product packaging, storefront signage, and wearable logos.

### Core Capabilities

1. **Product Packaging Swap** — Replace bottles, cans, boxes, and packaging in product shots while maintaining material properties (glass reflection, metallic sheen, matte finish)
2. **Logo Replacement** — Swap brand logos on clothing, vehicles, storefronts, and equipment with perspective-correct rendering
3. **Text Overlay Editing** — Replace in-video text (signage, labels, captions) with new brand copy in any language
4. **Color Grade Matching** — Automatically adjust replacement elements to match the video's existing color palette and lighting
5. **Batch Processing** — Process multiple source videos with the same brand kit in one run

### Pipeline

```
Source Video → Frame Extraction → AI Brand Detection → Inpainting Edit → i2v Generation → Assembly
```

Uses Gemini for frame editing, Kling V3 / Seedance for image-to-video generation, and ffmpeg for final assembly.

### Use Cases

- White-label video content for different brand clients
- Product placement in influencer content
- Localizing international ads with regional brand elements
- A/B testing different brand presentations in the same footage

## Usage

- "Replace the Coca-Cola bottle with our energy drink in this gym video"
- "Swap the Nike logo on the jersey to our brand logo"
- "Change the storefront sign from English to Chinese with our brand name"

## Upgrade

For production API access and enterprise batch processing, visit https://mediaclawbot.com

---

*Powered by MediaClaw — AI brand video replacement at scale*
