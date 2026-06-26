---
name: ppt-presenter
description: Create professional HTML presentations with complete word-for-word speaker scripts (逐字稿) and presenter view. Use when user asks to create a presentation, PPT, slides, tech sharing, keynote, or talk. Core feature: every slide comes with a full speaker script (150-300 words) visible in presenter view (press S) — so you can present confidently without memorizing anything. Full pipeline: (1) content planning and outline, (2) per-slide content with three-audience-layer explanations, (3) AI-generated whiteboard illustrations via Gemini API, (4) reveal.js HTML assembly with lightbox, (5) word-for-word 逐字稿 in presenter view. Also use when asked to add speaker notes, generate slide images, or convert markdown notes into a presentation.
---

# PPT Presenter — 带逐字稿的演讲级PPT生成器

为每一页生成完整演讲逐字稿 + 演讲者视图，让你自信上台不怯场。

## Pipeline Overview

```
User Topic/Notes
     ↓
1. Content Planning (outline + page count)
     ↓
2. Per-Slide Content (title, board description, speaker notes)
     ↓
3. Image Generation (Gemini 3 Pro Image, one per slide)
     ↓
4. HTML Assembly (reveal.js + lightbox + presenter view)
     ↓
5. Speaker Scripts (word-for-word 逐字稿 in <aside class="notes">)
```

## Step 1: Content Planning

From user's topic, notes, or markdown files, produce an outline:

- Determine audience (technical level, mixed audiences)
- Plan 15-25 slides grouped into 4-7 sections
- Each section gets a divider slide (colored section number + title)
- Structure: Opening hook → Sections → Quick Start → Takeaway + Q&A

If user provides existing markdown/text content, read it and restructure into slide outline. Ask user to confirm page count and structure before proceeding.

## Step 2: Per-Slide Content

For each slide, define:
- **Page title** — concise, with emoji prefix
- **Visual description** — what to draw on a whiteboard (colors, layout, diagrams)
- **Key content** — bullet points, tables, code blocks, comparison charts
- **Speaker script** — 150-300 words per slide, conversational tone, can be read aloud directly

For mixed audiences, write three-layer explanations:
- 编程小白 (beginners): metaphors, daily-life analogies
- 职场白领 (business): ROI, efficiency, practical scenarios  
- 开发人员 (developers): architecture, code, protocols

Write content to a markdown file first for user review, then proceed to image generation.

## Step 3: Image Generation

Generate one whiteboard-style illustration per slide using Gemini API.

Use the script: `scripts/generate_slide_images.py`

```bash
python3 scripts/generate_slide_images.py \
  --prompts-file prompts.json \
  --output-dir ./images \
  --api-key "$GEMINI_API_KEY"
```

### Prompt Guidelines

- Style: "whiteboard marker drawing, hand-drawn educational style, colorful markers (red, blue, green, orange)"
- Include Chinese text in prompts when audience is Chinese
- Describe specific visual elements: diagrams, flowcharts, comparison tables, icons
- Keep prompts under 500 chars for best results

### API Details

- Model: `gemini-3-pro-image-preview` (preferred) or `imagen-4.0-generate-001`
- Endpoint: `https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent`
- Request body for Gemini 3:
  ```json
  {
    "contents": [{"parts": [{"text": "Generate this image: {prompt}"}]}],
    "generationConfig": {"responseModalities": ["IMAGE", "TEXT"]}
  }
  ```
- Response: `candidates[0].content.parts[].inlineData.data` (base64)
- Rate limit: add 2-3 second delay between requests
- Retry on network errors (SSL EOF, connection reset)

### Finding API Key

Check TOOLS.md for `Gemini Image Generation` section, or ask user for API key.

## Step 4: HTML Assembly

Use the template: `assets/reveal-template.html`

### Structure

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <!-- reveal.js 5.1.0 from CDN -->
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/reveal.css">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/theme/black.css">
  <!-- Custom styles (see template) -->
</head>
<body>
<div class="reveal"><div class="slides">
  <!-- Section dividers: colored background gradient + section number -->
  <section data-background-gradient="...">
    <div class="section-num">1</div>
    <h2>Section Title</h2>
  </section>
  
  <!-- Content slides -->
  <section>
    <h2>Slide Title</h2>
    <!-- Content: .two-col, .three-col, .card, table, .code-block, .timeline -->
    <aside class="notes">Speaker script here...</aside>
  </section>
</div></div>

<!-- Lightbox overlay (see template) -->
<!-- reveal.js init + lightbox JS (see template) -->
</body>
</html>
```

### Key CSS Classes (defined in template)

| Class | Use |
|-------|-----|
| `.card` | Dark rounded content box |
| `.two-col` / `.three-col` | Flex column layouts |
| `.code-block` | Styled code with `.comment`, `.cmd`, `.flag` |
| `.warning-box` | Red-border alert box |
| `.slide-img` | Clickable image (max-height 420px) |
| `.flow-box` + `.flow-arrow` | Horizontal flow diagrams |
| `.timeline` + `.timeline-item` | Vertical timeline with colored dots |
| `.tag-blue/green/red/orange/purple` | Colored pill tags |
| `.accent/.green/.red/.blue/.purple/.yellow/.pink` | Text colors |
| `.checklist` | Checkbox-style list |
| `.photo-row` | Horizontal image gallery |
| `.gradient-text` | Gradient colored heading |

### Lightbox Feature

All images with `.slide-img`, `.slide-img-large`, `.slide-img-full`, or inside `.photo-row` are clickable. Clicking opens fullscreen lightbox with:
- Left/right navigation (arrows + keyboard)
- Counter (current/total)
- Close button + ESC key
- Pauses reveal.js keyboard while open

The lightbox JS is included in the template.

### reveal.js Configuration

```javascript
Reveal.initialize({
  hash: true,
  slideNumber: 'c/t',
  transition: 'slide',
  width: 1280,
  height: 720,
  margin: 0.06,
  plugins: [RevealHighlight, RevealNotes]
});
```

Keyboard hints shown at bottom: `← → 翻页 · S 演讲者视图 · F 全屏 · O 总览`

## Step 5: Speaker Scripts

Add `<aside class="notes">` to every content slide (not section dividers).

### Script Guidelines

- **Length**: 150-300 words per slide (1-2 minutes speaking time)
- **Tone**: Conversational, as if speaking to audience directly
- **Structure**: Hook → explain visual → key points → transition to next
- **Language**: Match audience language (Chinese for Chinese audience)
- **Include**: Analogies, real examples, audience engagement ("大家看...")
- **Avoid**: Reading bullet points verbatim; scripts should expand on slide content

### Presenter View

User presses `S` to open presenter view showing:
- Current slide (left)
- Speaker notes/script (right)  
- Next slide preview
- Timer

## Output Checklist

Before delivering, verify:
- [ ] All slides have titles with emoji prefixes
- [ ] All content slides have `<aside class="notes">` with full scripts
- [ ] All slide images generated and saved to `images/` directory
- [ ] Images use `.slide-img` class (clickable lightbox)
- [ ] Section dividers have colored backgrounds and section numbers
- [ ] Lightbox JS is included and functional
- [ ] reveal.js loads from CDN (no local dependencies)
- [ ] File opens correctly in browser (`open index.html`)
