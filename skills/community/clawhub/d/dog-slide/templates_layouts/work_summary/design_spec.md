# Work Summary Template - Design Specification

> Suitable for quarterly work reports, annual summaries, project debriefings, job appraisals, and similar performance-review scenarios.

---

## I. Template Overview

| Property | Description |
|----------|-------------|
| **Template Name** | work_summary (工作总结风格) |
| **Use Cases** | 试用期总结汇报、季度工作总结、年度工作总结、项目结题报告、工作述职 |
| **Design Tone** | 正式、严谨、红色系、庄重 |
| **Theme Mode** | Light theme (white background + red accents) |

---

## II. Canvas Specification

| Property | Value |
|----------|-------|
| **Format** | Standard 16:9 |
| **Dimensions** | 1280 × 720 px |
| **viewBox** | `0 0 1280 720` |
| **Page Margins** | Left/Right 50px, Top 80px, Bottom 40px |
| **Safe Area** | x: 50-1230, y: 80-680 |

---

## III. Color Scheme

### Primary Colors

| Role | Value | Notes |
|------|-------|-------|
| **Primary Red** | `#D02300` | Titles, key borders, section number blocks, decorative bars |
| **Dark Red** | `#A01A00` | Footer backgrounds, strong emphasis, gradient dark end |
| **Warm Gray** | `#F5F0EB` | Background base, subtle blocks, card interiors |
| **Light Accent** | `#FFE0D0` | Highlight blocks, key message backgrounds |

### Text Colors

| Role | Value | Usage |
|------|-------|-------|
| **Primary Text** | `#2D2D2D` | Body text, titles |
| **White Text** | `#FFFFFF` | Text on dark backgrounds |
| **Secondary Text** | `#5A5A5A` | Descriptions, annotations |
| **Light Auxiliary** | `#999999` | Page numbers, hints |

---

## IV. Typography System

**Font Stack**: `"Microsoft YaHei", "Source Han Sans SC", "SimHei", Arial, sans-serif`

### Font Size Hierarchy

| Level | Usage | Size | Weight |
|-------|-------|------|--------|
| H1 | Cover main title | 52px | Bold |
| H2 | Page heading | 28px | Bold |
| H3 | Section title | 24px | Bold |
| P | Body content | 18px | Regular |
| High | Highlighted data | 36px | Bold |
| Sub | Supplementary text | 14px | Regular |

---

## V. Page Structure

### General Layout

| Area | Position/Height | Description |
|------|----------------|-------------|
| **Top Bar** | y=0, h=8px | Red accent bar, full width |
| **Header** | y=20, h=60px | Red left bar + page title |
| **Content Area** | y=100, h=580px | Main content area |
| **Footer** | y=680, h=40px | Page number, bottom decoration line |

---

## VI. Page Types

### 1. Cover Page (01_cover.svg)
- White background
- Top red gradient bar
- Centered main title + subtitle
- Red left accent bar decoration
- Presenter/Date/Organization info at bottom

### 2. Table of Contents (02_toc.svg)
- White background + warm gray cards
- Standard header with red left bar
- Card-style chapter listing with numbering

### 3. Chapter Page (02_chapter.svg)
- Red gradient full-screen background
- Large semi-transparent chapter number
- White chapter title
- Decorative line

### 4. Content Page (03_content.svg)
- White background
- Standard header (red top bar + red left bar)
- Flexible content area with card-based layout options
- Footer: page number

### 5. Ending Page (04_ending.svg)
- White background
- Red top bar
- Centered thank-you message
- Contact info area

---

## VII. Layout Modes

| Mode | Use Cases |
|------|-----------|
| **Single Column Centered** | Cover, ending, key points |
| **Two Columns (5:5)** | Comparative display |
| **Two Columns (4:6)** | Image-text mixed layout |
| **Card Grid** | Data display, KPI dashboard |
| **Timeline** | Project progress, milestones |
| **Table** | Data comparison |

---

## VIII. Spacing Guidelines

| Element | Value |
|---------|-------|
| Card gap | 20px |
| Content block gap | 24px |
| Card padding | 20px |
| Card border radius | 8px |

---

## IX. SVG Technical Constraints

### Mandatory Rules
1. viewBox: `0 0 1280 720`
2. Use `<rect>` for backgrounds
3. Use `<tspan>` for text wrapping (no `<foreignObject>`)
4. Use `fill-opacity` / `stroke-opacity` for transparency
5. Prohibited: `mask`, `<style>`, `class`, `foreignObject`
6. Prohibited: `textPath`, `animate*`, `script`

---

## X. Placeholder Specification

| Placeholder | Description |
|-------------|-------------|
| `{{TITLE}}` | Main title |
| `{{SUBTITLE}}` | Subtitle |
| `{{AUTHOR}}` | Presenter name |
| `{{ORGANIZATION}}` | Organization |
| `{{DATE}}` | Date |
| `{{PAGE_TITLE}}` | Page title |
| `{{CHAPTER_NUM}}` | Chapter number |
| `{{CHAPTER_TITLE}}` | Chapter title |
| `{{PAGE_NUM}}` | Page number |
| `{{CONTENT_AREA}}` | Content area |
| `{{TOC_ITEM_N_TITLE}}` | TOC item title |
| `{{TOC_ITEM_N_DESC}}` | TOC item description |
