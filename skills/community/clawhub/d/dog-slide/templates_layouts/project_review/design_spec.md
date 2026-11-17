# Project Review Template - Design Specification

> Suitable for technical solution presentations, product proposal reviews, project initiation applications, architecture design reviews, and related decision-making scenarios.

---

## I. Template Overview

| Property | Description |
|----------|-------------|
| **Template Name** | project_review (方案评审/项目立项风格) |
| **Use Cases** | 技术方案汇报、产品方案介绍、项目立项申请、架构设计评审、技术选型报告 |
| **Design Tone** | 专业、高端、金色系、技术化 |
| **Theme Mode** | Dark-light hybrid (deep navy + gold accents) |

---

## II. Canvas Specification

| Property | Value |
|----------|-------|
| **Format** | Standard 16:9 |
| **Dimensions** | 1280 × 720 px |
| **viewBox** | `0 0 1280 720` |
| **Page Margins** | Left/Right 60px, Top 80px, Bottom 40px |
| **Safe Area** | x: 60-1220, y: 80-680 |

---

## III. Color Scheme

### Primary Colors

| Role | Value | Notes |
|------|-------|-------|
| **Primary Gold** | `#CFAC6A` | Titles, key accents, decorative elements |
| **Deep Navy** | `#1A2744` | Header backgrounds, chapter page backgrounds |
| **Warm White** | `#FAF8F5` | Background base |
| **Light Gold** | `#F0E6D0` | Highlight blocks, card backgrounds |
| **Dark Navy** | `#0F1A2E` | Footer, strong emphasis blocks |

### Text Colors

| Role | Value | Usage |
|------|-------|-------|
| **Primary Text** | `#1A1A2E` | Body text |
| **White Text** | `#FFFFFF` | Text on dark backgrounds |
| **Gold Text** | `#CFAC6A` | Emphasis, decorative title text |
| **Secondary Text** | `#6B7280` | Annotations, page numbers |
| **Muted Text** | `#9CA3AF` | Hints, auxiliary info |

---

## IV. Typography System

**Font Stack**: `"Source Han Sans SC", "Microsoft YaHei", "PingFang SC", Arial, sans-serif`

### Font Size Hierarchy

| Level | Usage | Size | Weight |
|-------|-------|------|--------|
| H1 | Cover main title | 48px | Bold |
| H2 | Page heading | 32px | Bold |
| H3 | Section title | 24px | Semi-Bold |
| P | Body content | 18px | Regular |
| High | Highlighted data | 40px | Bold |
| Sub | Supplementary text | 14px | Regular |

---

## V. Page Structure

### General Layout

| Area | Position/Height | Description |
|------|----------------|-------------|
| **Top Accent** | y=0, h=6px | Gold line, full width |
| **Header** | y=25, h=55px | Navy section number + gold title |
| **Divider** | y=85 | Gold dashed line |
| **Content Area** | y=105, h=575px | Main content area |
| **Footer** | y=690, h=30px | Page number, gold dot |

---

## VI. Page Types

### 1. Cover Page (01_cover.svg)
- Deep navy gradient background
- Gold geometric frame decoration
- Large centered main title + subtitle
- Gold decorative lines and dots

### 2. Table of Contents (02_toc.svg)
- Warm white background
- Navy left panel with gold numbering
- Card-style chapter listing with gold accents

### 3. Chapter Page (02_chapter.svg)
- Full dark navy background
- Gold left accent bar
- Large semi-transparent chapter number (gold stroke)
- Chapter title in white + gold English subtitle

### 4. Content Page (03_content.svg)
- Warm white background
- Navy top header with gold section number block
- Gold dashed separator
- Flexible content area supporting technical diagrams, architecture charts

### 5. Ending Page (04_ending.svg)
- Deep navy gradient background
- Centered gold thank-you message
- Contact information in white

---

## VII. Layout Modes

| Mode | Use Cases |
|------|-----------|
| **Single Column** | Title, section intro, key messages |
| **Two Columns (5:5)** | Comparison, pro/con analysis |
| **Two Columns (6:4)** | Image-text mixed; architecture + description |
| **Card Grid** | Feature lists, module overview |
| **Process Flow** | Implementation plans, roadmaps |
| **Table** | Technical comparison, specification lists |

---

## VIII. Spacing Guidelines

| Element | Value |
|---------|-------|
| Card gap | 24px |
| Content block gap | 28px |
| Card padding | 24px |
| Card border radius | 8px |

---

## IX. SVG Technical Constraints

### Mandatory Rules
1. viewBox: `0 0 1280 720`
2. Use `<rect>` for backgrounds
3. Use `<tspan>` for text wrapping
4. Use `fill-opacity` / `stroke-opacity` for transparency
5. Prohibited: `mask`, `<style>`, `class`, `foreignObject`
6. Prohibited: `textPath`, `animate*`, `script`

---

## X. Placeholder Specification

| Placeholder | Description |
|-------------|-------------|
| `{{TITLE}}` | Main title |
| `{{SUBTITLE}}` | Subtitle |
| `{{AUTHOR}}` | Presenter / team |
| `{{DATE}}` | Date |
| `{{PAGE_TITLE}}` | Page title |
| `{{CHAPTER_NUM}}` | Chapter number |
| `{{CHAPTER_TITLE}}` | Chapter title |
| `{{CHAPTER_TITLE_EN}}` | Chapter English subtitle |
| `{{PAGE_NUM}}` | Page number |
| `{{CONTENT_AREA}}` | Content area |
| `{{TOC_ITEM_N_TITLE}}` | TOC item title |
| `{{TOC_ITEM_N_DESC}}` | TOC item description |
