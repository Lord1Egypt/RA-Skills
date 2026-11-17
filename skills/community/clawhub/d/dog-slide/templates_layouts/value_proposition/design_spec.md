# Value Proposition Template - Design Specification

> Suitable for business proposals, product launches, client solution presentations, marketing introductions, and investment pitches.

---

## I. Template Overview

| Property | Description |
|----------|-------------|
| **Template Name** | value_proposition (产品价值传递风格) |
| **Use Cases** | 商业招投标、产品发布会、客户解决方案、营销方案介绍、合作洽谈 |
| **Design Tone** | 标准、商务、蓝色系、专业 |
| **Theme Mode** | Light theme (white background + blue accents) |

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
| **Primary Blue** | `#5B9BD5` | Titles, key borders, decorative elements |
| **Dark Blue** | `#2E75B6` | Chapter backgrounds, strong emphasis |
| **Light Blue** | `#DEEBF7` | Card backgrounds, highlight blocks |
| **Warm Gray** | `#F2F2F2` | Background base |
| **Accent Orange** | `#ED7D31` | Call-to-action, key data highlights |

### Text Colors

| Role | Value | Usage |
|------|-------|-------|
| **Primary Text** | `#333333` | Body text |
| **White Text** | `#FFFFFF` | Text on dark backgrounds |
| **Secondary Text** | `#666666` | Descriptions, annotations |
| **Blue Text** | `#2E75B6` | Emphasized titles, links |

---

## IV. Typography System

**Font Stack**: `"Microsoft YaHei", "Source Han Sans SC", "PingFang SC", Arial, sans-serif`

### Font Size Hierarchy

| Level | Usage | Size | Weight |
|-------|-------|------|--------|
| H1 | Cover main title | 50px | Bold |
| H2 | Page heading | 28px | Bold |
| H3 | Section title | 22px | Semi-Bold |
| P | Body content | 18px | Regular |
| High | Highlighted data | 38px | Bold |
| Sub | Supplementary text | 14px | Regular |

---

## V. Page Structure

### General Layout

| Area | Position/Height | Description |
|------|----------------|-------------|
| **Header Bar** | y=0, h=6px | Blue gradient accent, full width |
| **Logo Area** | y=15, h=40px | Top-right logo space |
| **Title Bar** | y=60, h=50px | Blue number block + page title |
| **Divider** | y=110 | Light gray line |
| **Content Area** | y=120, h=530px | Main content area |
| **Footer** | y=680, h=40px | Organization, page number |

---

## VI. Page Types

### 1. Cover Page (01_cover.svg)
- Blue gradient background
- White centered main title
- Orange accent bar decoration
- Subtitle + presenter info
- Decorative geometric circles

### 2. Table of Contents (02_toc.svg)
- White background + light blue cards
- Standard header with blue number block
- Numbered chapter listing with descriptions

### 3. Chapter Page (02_chapter.svg)
- Blue gradient full background
- White large chapter number
- Chapter title + decorative bar
- Subtle geometric pattern overlay

### 4. Content Page (03_content.svg)
- Warm gray background
- Blue top accent bar
- Blue number block + page title
- Orange accent for key data
- Flexible content area

### 5. Ending Page (04_ending.svg)
- Blue gradient background
- Centered thank-you message
- Contact info area
- Decorative elements

---

## VII. Layout Modes

| Mode | Use Cases |
|------|-----------|
| **Centered** | Cover, ending, value statement |
| **Two Columns (5:5)** | Problem/Solution, Before/After |
| **Two Columns (4:6)** | Product + description, case study |
| **Three-Column Cards** | Feature comparison, service packages |
| **Timeline** | Roadmap, implementation phases |
| **Table** | Pricing, specifications, ROI comparison |

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
| `{{AUTHOR}}` | Presenter / organization |
| `{{DATE}}` | Date |
| `{{PAGE_TITLE}}` | Page title |
| `{{CHAPTER_NUM}}` | Chapter number |
| `{{CHAPTER_TITLE}}` | Chapter title |
| `{{PAGE_NUM}}` | Page number |
| `{{CONTENT_AREA}}` | Content area |
| `{{TOC_ITEM_N_TITLE}}` | TOC item title |
| `{{TOC_ITEM_N_DESC}}` | TOC item description |
