# Style Contract - Academic Literature Presentation

Extracted from reference PPTX artifact. Blue academic theme, **strictly minimalist** design.

## Core Design Principle: Clean and Minimal

The reference style is **text-on-white-background** with a blue left sidebar. It does NOT use card-based layouts, colored containers, decorative icons, status badges, or visual embellishments. Content is presented as plain text paragraphs and bullet points directly on the white background.

## Color Palette (Strictly Limited)

| Role | Color | Hex | Usage |
|------|-------|-----|-------|
| Primary (sidebar bg) | Deep blue | #003B6F | Left navigation sidebar background only |
| Accent (active nav) | Red/Crimson | #C00000 | Active navigation section text ONLY; highlighted keywords in body text ONLY |
| Title text (on white) | Dark blue | #003B6F | Slide titles on white background |
| Title text (on blue) | White | #FFFFFF | Navigation labels on blue sidebar; cover/thank-you title text |
| Body text | Black/Dark gray | #333333 | Main body text |
| Background | White | #FFFFFF | Main content area background — ALWAYS white, no exceptions |
| Cover band | Deep blue | #003B6F | Horizontal title band on cover slide |
| Thank-you band | Deep blue | #003B6F | Horizontal band on thank-you slide |

**CRITICAL**: The white content area must NEVER have colored backgrounds, card fills, gradient fills, or container borders. The only colors in the main content area are: dark blue for titles, black/dark gray for body text, and red for occasional keyword emphasis.

## Typography

| Element | Font | Size | Color | Weight |
|---------|------|------|-------|--------|
| Slide title | Microsoft YaHei | 22pt | #003B6F | Bold |
| Body text | Microsoft YaHei | 20pt | #333333 | Regular |
| Navigation active | Microsoft YaHei | 18pt | #C00000 | Bold |
| Navigation inactive | Microsoft YaHei | 16pt | #FFFFFF | Regular |
| Cover title (EN) | Microsoft YaHei | 28pt | #FFFFFF | Bold |
| Cover title (CN) | Microsoft YaHei | 26pt | #FFFFFF | Bold |
| Author info | Microsoft YaHei | 18pt | #333333 | Regular |
| TOC item | Microsoft YaHei | 24pt | #003B6F | Bold |
| Table caption | Microsoft YaHei | 16pt | #333333 | Regular |
| Figure caption | Microsoft YaHei | 16pt | #333333 | Regular |

- Font family: Microsoft YaHei (微软雅黑) for ALL text
- Fallback CJK fonts: PingFang SC, Noto Sans CJK SC, Source Han Sans SC
- All text elements use the same font family consistently

## Anti-Patterns (MUST AVOID)

The following patterns from the previous rollout caused style mismatch and MUST be avoided:

1. **NO card-based layouts** — Do NOT place content inside rectangles with colored borders, colored backgrounds, or shadow effects
2. **NO decorative icons** — Do NOT use heart, brain, checkmark, or any other emoji/icon elements
3. **NO status badges** — Do NOT create colored SUPPORTED/REJECTED labels. Use simple inline text like "假设得到支持" or "假设未获支持"
4. **NO colored section headers** — Do NOT put section titles inside colored boxes or bars within the content area
5. **NO multi-color accents** — Red (#C00000) is the ONLY accent color and is used sparingly for: (a) active navigation text, (b) occasional keyword emphasis in body text
6. **NO gradient fills** anywhere in the content area
7. **NO rounded corner containers** for text content
8. **NO numbered items with colored circles** — use simple bullet points or plain numbers

## Text Overflow Prevention (Critical)

Text overflow was the #1 quality issue. Follow these strict rules:

### Maximum Content per Slide

| Element | Maximum |
|---------|---------|
| Body text lines per slide | 12 lines at 20pt |
| Body characters per slide | ~600 Chinese characters |
| Bullet points per slide | 6 items |
| Paragraphs per slide | 2-3 short paragraphs |
| Table rows per slide | 10 rows (including header) |
| Figures per slide | 1-2 (depending on size) |

### Content Splitting Rules

When content exceeds limits, split across multiple slides:
- **Long literature review**: Split into "综述 (1)", "综述 (2)", etc.
- **Long results section**: Split by sub-topic or by figure/table
- **Long discussion**: Split into "讨论 (1)", "讨论 (2)", etc.
- **Multiple studies**: Each study gets its own set of slides

### Text Density Check

Before finalizing each slide, verify:
- [ ] Text does NOT extend beyond 90% of content area width
- [ ] Text does NOT extend beyond 85% of content area height
- [ ] Title does NOT overlap with body content (minimum 20pt gap)
- [ ] No body text overlaps with sidebar navigation
- [ ] Figures/images do NOT overlap with text

## Element Spacing Rules (Prevent Occlusion and Drift)

### Minimum Gaps Between Elements

| Between | Minimum Gap |
|---------|-------------|
| Title and body content | 20pt |
| Body paragraphs | 12pt |
| Bullet items | 8pt |
| Text and image | 15pt |
| Image and caption | 8pt |
| Content and slide edge | At least 5% of slide width |

### Alignment Rules

- All text blocks must be left-aligned (not center-aligned, not justified)
- Title must align with the left edge of the body content area
- Bullet point indentation must be consistent across all slides
- Images must be positioned with clear margins from text
- Tables must be centered within the content area if narrower than content width

## Slide Layout Patterns

### 1. Cover Slide (Title Slide)

```
+----------------------------------------------------------+
|                    [Institution Badge]                     |
|                      (top center)                        |
|                                                          |
+======== Deep Blue Horizontal Band =======================+
|                                                          |
|     English Paper Title (large, bold, white)             |
|     中文论文标题 (large, bold, white)                     |
|                                                          |
+==========================================================+
|                                                          |
|     作者： Author Names                                  |
|                                                          |
|     Journal Name (Year)                        IF: x.x   |
|                                                          |
+----------------------------------------------------------+
```

- White background above and below the blue band
- A subtle institutional badge/logo at top center (generic academic icon if none provided)
- Paper title in both English and Chinese inside the blue band
- Author names, journal name, and impact factor below the band

### 2. Table of Contents (TOC) Slide

```
+----------------------------------------------------------+
|  [Logo]    |                                             |
|            |  01. 研究背景                                |
|  CONTENTS  |                                             |
|            |  02. 实验设计                                |
|  (left     |                                             |
|   blue     |  03. 结果与讨论                              |
|   panel    |                                             |
|   ~30%)    |  04. 启示和思考                              |
|            |                                             |
+----------------------------------------------------------+
```

- Left panel: deep blue background with logo and "CONTENTS" in white
- Right area: white background with numbered section titles in dark blue
- Section numbers as "01.", "02.", etc.
- Each section title on its own line with generous vertical spacing

### 3. Section Navigation Sidebar (All Content Slides)

```
+---------+------------------------------------------------+
|  [Logo] |  Section Title (top, dark blue, bold)          |
|         |                                                |
| ACTIVE  |  Body content area (white background)          |
| SECTION |                                                |
| (red    |  - Plain text paragraphs                       |
|  text)  |  - Bullet points                               |
|         |  - Images positioned to right or below         |
| other   |                                                |
| section |                                                |
| (white) |                                                |
+---------+------------------------------------------------+
  ~18%              ~82%
```

- Sidebar width: approximately 18-20% of slide width
- Sidebar background: deep blue (#003B6F)
- Active section: red text (#C00000), bold
- Inactive sections: white text, regular weight
- Section labels separated by thin horizontal lines
- Main content area: ALWAYS white background, no exceptions

### 4. Content Slide - Text Focus (Primary Pattern)

The most common slide type. Simple text directly on white background:

- Section title at top-left of content area in dark blue, bold
- Body text below title, left-aligned, black/dark gray
- Standard bullet markers (simple dots or dashes)
- Key phrases highlighted in red (#C00000) sparingly — only 1-2 phrases per slide
- Generous line spacing (1.4-1.5x)
- NO containers, NO cards, NO colored backgrounds behind text

### 5. Content Slide - With Image

- Same sidebar navigation
- Image positioned on the RIGHT side of content area, occupying ~30-40% width
- Text flows on the LEFT side of the image
- Or: Image placed below text, spanning full content width
- Image must maintain original aspect ratio
- Caption below image if needed (16pt, gray)

### 6. Content Slide - Full Figure/Table

- For large figures or tables needing maximum space
- Minimize surrounding text to title + brief caption only
- Figure/table occupies most of content area
- Table text minimum 14pt for readability
- NO colored table headers — use simple black borders or light gray (#F0F0F0) header fill

### 7. Model/Diagram Slide

- For theoretical model diagrams and hypothesis frameworks
- Use simple boxes with thin black/gray borders on white background
- Arrow style: solid lines with arrowheads
- Variable names inside boxes
- NO colored box fills, NO gradient fills on diagram elements
- Mediation/indirect effect paths clearly shown

### 8. Thank You / End Slide

```
+----------------------------------------------------------+
|                    [Institution Badge]                     |
|                      (top center)                        |
|                                                          |
+======== Deep Blue Horizontal Band =======================+
|                                                          |
|                     谢 谢！                              |
|                  (large white text)                      |
|                                                          |
+==========================================================+
|                                                          |
|                    (white background)                    |
|                                                          |
+----------------------------------------------------------+
```

- Same layout as cover slide with "谢谢！" in the blue band

## Image and Figure Handling

1. **Preserve all original figures** from the literature — no figure should be omitted
2. **Preserve all original tables** — recreate with same data, format for slide readability
3. **Figure/table numbering**: Keep original numbering or translate labels to Chinese
4. **Statistical annotations**: Preserve all significance markers exactly
5. **Image quality**: Ensure extracted images are high resolution
6. **Image borders**: Use thin light gray borders (#CCCCCC) if needed, no colored frames

## Layout Density and Rhythm

- One main idea per slide
- Text should not fill more than 70% of the content area
- Leave generous margins (at least 5% of slide width on all sides)
- Vertical spacing between paragraphs: at least 1.4x line height
- Consistent spacing between title and body content
- Each content slide should take 1-3 minutes to present
- When in doubt, use MORE slides with LESS content per slide rather than cramming
