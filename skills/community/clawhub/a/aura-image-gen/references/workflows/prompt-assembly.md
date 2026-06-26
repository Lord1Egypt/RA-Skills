# Prompt Assembly Guide

## Base Prompt Structure

```
Create a Xiaohongshu style card following these guidelines:

## Image Specifications
- Type: Infographic Card
- Orientation: Portrait (vertical)
- Aspect Ratio: 3:4 (1080×1440px)

## Core Principles
- Hand-drawn / illustration quality — NO photorealistic elements
- Keep information concise, highlight keywords
- Use ample whitespace for easy scanning
- Maintain clear visual hierarchy
- Slight imperfections for human feel (not AI-perfect)

## Text Style
- ALL text must match the style aesthetic
- Main titles: prominent and eye-catching
- Key text: bold and enlarged
- DO NOT use generic computer fonts

## Language
- Match the content language
- Chinese: use ""，。！punctuation

---

{STYLE_SECTION}

---

{LAYOUT_SECTION}

---

{CONTENT_SECTION}
```

## Style Section

Load from `presets/{style}.md`, extract:
- Color palette (primary, accent, background, text)
- Visual elements (decorations, frames, emphasis)
- Typography rules

## Layout Section

Load from `elements/canvas.md`, extract:
- Information density
- Whitespace percentage
- Structure description

## Content Section

```
## Content
**Position**: {Cover / Content / Ending}
**Core Message**: {main point}

**Text Content**:
- Title: {title text}
- Points: {bullet points}

**Visual Concept**:
{describe what the image should look like}
```

## Reference Image Chain

For series (multiple cards):
1. Image 1 (cover): generate WITHOUT --ref
2. Images 2+: generate WITH --ref image-01.png
3. This ensures character/style/color consistency

## Checklist Before Generation

- [ ] Style section loaded?
- [ ] Layout matches content type?
- [ ] Content accurate?
- [ ] Language correct?
- [ ] No conflicting instructions?
- [ ] Anti-AI imperfections included?
