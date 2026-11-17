---
description: Convert an existing PPTX presentation into a reusable page layout template (design_spec.md + SVG skeleton files) for future PPT generation sessions.
---

# Create From PPT — Template Creation Workflow

> Convert an existing PPTX presentation into a reusable page layout template

## Overview

This workflow takes a user-provided PPTX file, analyzes its design, and creates a complete layout template (`design_spec.md` + SVG skeleton files) that can be reused in future PPT generation sessions.

**Output location**: `templates/layouts/<template_id>/`

> **Companion workflow**: Full multi-source template creation (type A/B/C/D, fidelity/mirror modes, pptx_template_import.py) is handled by [`create-template.md`](./create-template.md). This workflow is a streamlined path specifically for the "I have a PPTX, make a template from it" case — it uses `ppt_to_md.py` for content extraction and manual design analysis instead of the full `pptx_template_import.py` pipeline.

---

## Prerequisites

- User provides a path to an existing `.pptx` file
- Python environment with `ppt_to_md.py` available (under `scripts/source_to_md/`)

---

## Workflow Steps

### Step 1: Extract Content Structure

Run `ppt_to_md.py` on the source PPTX to get a Markdown representation of all slides' text content and structure:

```bash
python3 skills/dog-slide/scripts/source_to_md/ppt_to_md.py <path_to_pptx>
```

This produces a structured Markdown document covering:

- Per-slide text content (titles, body text, tables, lists)
- Slide hierarchy and ordering
- Any speaker notes (if present)

Review the output to understand the original deck's narrative flow and content density. Flag any slides that use unusual layouts (e.g., full-bleed images, data-heavy dashboards, mixed media) for closer attention during the design analysis.

---

### Step 2: Analyze Design Style

From the `ppt_to_md.py` output and the user's description of the source deck, analyze the following design dimensions:

#### Visual Structure

- **Slide master colors and accent palette** — identify dominant HEX values used across slides for backgrounds, headers, accents, and text
- **Font usage** — note the font families for headings and body text, plus any non-standard / decorative fonts
- **Page layout patterns** — header position and height, footer location, left/right margins, content area splits (single column, two-column, grid zones), safe area boundaries
- **Signature visual elements** — recurring decorative motifs such as top bars, side panels, ribbons, corner accents, geometric frames, gradient overlays
- **Image / icon usage** — whether images are full-bleed, framed, or used as backgrounds; icon style (outline, filled, branded)
- **Overall design tone** — formal / creative / minimalist / information-dense / tech-forward / authoritative, etc.

#### User Clarification Questions

Ask the user about:

1. **Template name / ID** — alphanumeric + underscores only (e.g., `client_branding_2026`)
2. **Design generalization** — which aspects of the original design to preserve exactly and which to generalize for broader reuse (e.g., "keep the gold accent bar but make the background neutral")
3. **Brand assets** — whether any logos, watermarks, or brand images should be included in the template package
4. **Page type preferences** — which original slide types should become template pages (cover, chapter, content, ending, etc.)

---

### Step 3: Output `design_spec.md`

Write `design_spec.md` following the standard I–XI chapter structure (see existing templates for reference):

```markdown
# [Template Name] — Design Specification

> One-line description of applicable scenarios

## I. Template Overview

| Property | Description |
|----------|-------------|
| **Template Name** | <template_id> |
| **Use Cases** | <applicable scenarios> |
| **Design Tone** | <tone summary> |
| **Theme Mode** | <light / dark / hybrid> |

## II. Canvas Specification (1280x720)

| Property | Value |
|----------|-------|
| **Format** | Standard 16:9 |
| **Dimensions** | 1280 x 720 px |
| **viewBox** | `0 0 1280 720` |

## III. Color Scheme

| Role | HEX | Usage |
|------|-----|-------|
| <role> | <#HEX> | <where to use> |

## IV. Typography System

| Level | Usage | Size | Weight |
|-------|-------|------|--------|
| <H1> | <usage> | <px> | <weight> |

## V. Page Structure

| Area | Position | Description |
|------|----------|-------------|
| <area> | <y/height> | <description> |

## VI. Page Types

### 1. Cover Page
### 2. Table of Contents (optional)
### 3. Chapter Page
### 4. Content Page
### 5. Ending Page

## VII. Layout Modes (Recommended)

| Mode | Use Cases |
|------|-----------|
| Single Column | <description> |

## VIII. Spacing Specification

| Element | Value |
|---------|-------|
| <element> | <px> |

## IX. SVG Technical Constraints

### Mandatory Rules
1. viewBox: `0 0 1280 720`
2. Use `<rect>` for backgrounds
3. Use `<tspan>` for text wrapping
4. Use `fill-opacity` / `stroke-opacity` for transparency
5. Prohibited: `mask`, `<style>`, `class`, `foreignObject`
6. Prohibited: `textPath`, `animate*`, `script`

## X. Placeholder Specification

| Placeholder | Description |
|-------------|-------------|
| `{{TITLE}}` | Main title |

## XI. Usage Guide (Recommended)

General guidance for using this template effectively, including recommended content density per page, pairing suggestions, and style tips.
```

> **Placeholder convention templates** use `{{PLACEHOLDER}}` format. See the [canonical placeholder table](../templates/layouts/README.md#placeholder-specification) for the full reference of standard placeholders by page type.

---

### Step 4: Write SVG Skeleton Files

Based on the `design_spec.md`, create SVG skeleton files in the template directory. Each SVG must be a standalone, self-contained file with the correct `viewBox` and placeholder slots.

#### Required Files

| File | Required | Purpose |
|------|----------|---------|
| `01_cover.svg` | Yes | Cover page with {{TITLE}}, {{SUBTITLE}}, {{DATE}}, {{AUTHOR}} placeholders |
| `02_toc.svg` | No | Table of contents with {{TOC_ITEM_N_TITLE}} / {{TOC_ITEM_N_DESC}} placeholders |
| `02_chapter.svg` | Yes | Chapter divider with {{CHAPTER_NUM}}, {{CHAPTER_TITLE}} |
| `03_content.svg` | Yes | Content page with {{PAGE_TITLE}}, {{CONTENT_AREA}}, {{PAGE_NUM}} |
| `04_ending.svg` | Yes | Ending page with {{THANK_YOU}}, {{CONTACT_INFO}}, {{PAGE_NUM}} |

#### SVG Compliance Rules

All SVGs must follow these constraints:

| Rule | Requirement |
|------|-------------|
| **viewBox** | `0 0 1280 720` |
| **Backgrounds** | Use `<rect>` elements |
| **Text wrapping** | Use `<tspan>` |
| **Transparency** | Use `fill-opacity` / `stroke-opacity` |
| **Gradients** | Use `<defs>` with `<linearGradient>` |

**Forbidden elements** (PPT-incompatible):

| Banned | Alternative |
|--------|-------------|
| `<foreignObject>` | `<text>` + `<tspan>` |
| `<clipPath>` on shapes | Draw geometry directly with native elements (`<rect rx>`, `<circle>`, `<path>`, etc.) |
| `<mask>` | `fill-opacity` |
| `<style>` / `class` | Inline styles |
| `textPath` | Plain `<text>` |
| `animate*` / `script` | Static design only |
| `rgba()` | HEX + `fill-opacity` |
| `<g opacity="...">` | Set opacity on each child individually |
| HTML named entities (`&nbsp;`, `&mdash;`, `&copy;`, etc.) | Write the raw Unicode character directly (`---`, `--`, `(c)`, etc.) |
| Bare `&` `<` `>` in text | Escape as `&amp;` `&lt;` `&gt;` |

#### Placeholder Format

Use `{{PLACEHOLDER}}` format for all replaceable content. The canonical placeholders by page type are:

| Page | Standard Placeholders |
|------|----------------------|
| `01_cover.svg` | `{{TITLE}}`, `{{SUBTITLE}}`, `{{DATE}}`, `{{AUTHOR}}` |
| `02_toc.svg` | `{{TOC_ITEM_1_TITLE}}` … `{{TOC_ITEM_N_TITLE}}`, `{{TOC_ITEM_1_DESC}}` … `{{TOC_ITEM_N_DESC}}` |
| `02_chapter.svg` | `{{CHAPTER_NUM}}`, `{{CHAPTER_TITLE}}` |
| `03_content.svg` | `{{PAGE_TITLE}}`, `{{CONTENT_AREA}}`, `{{PAGE_NUM}}`, `{{SOURCE}}` |
| `04_ending.svg` | `{{THANK_YOU}}`, `{{CONTACT_INFO}}`, `{{PAGE_NUM}}` |

---

### Step 5: Register Template

Register the new template in the library index. This updates `layouts_index.json` and refreshes the Quick Index in the templates README:

```bash
python3 skills/dog-slide/scripts/register_template.py <template_id>
```

The registrar derives the index entry (`summary`, `keywords`) from the `design_spec.md` content. After registration, the template becomes discoverable via the library index.

> **Note**: Registration is optional for use — a template directory works as long as the user supplies its explicit path. Registration only makes it discoverable in listings.

---

### Step 6: Verify

Validate the template directory against all compliance rules:

```bash
python3 skills/dog-slide/scripts/svg_quality_checker.py skills/dog-slide/templates/layouts/<template_id> --format ppt169
```

Checklist before declaring completion:

- [ ] `design_spec.md` follows the I–XI chapter structure
- [ ] All required SVG files exist (`01_cover.svg`, `02_chapter.svg`, `03_content.svg`, `04_ending.svg`)
- [ ] Optional `02_toc.svg` is present if the original deck has a table of contents
- [ ] Every SVG uses `viewBox="0 0 1280 720"`
- [ ] No forbidden elements (foreignObject, clipPath on shapes, masks, style tags, etc.)
- [ ] All replaceable text uses `{{PLACEHOLDER}}` format
- [ ] Color values match the `design_spec.md` color scheme
- [ ] Fonts use system-available families only
- [ ] Template is registered via `register_template.py` (Step 5)

---

## Important Rules

1. **Font licensing** — Do not copy any proprietary or third-party fonts. Use only system-available fonts such as `Microsoft YaHei`, `SimHei`, `PingFang SC`, `Source Han Sans SC`, `Arial`, `sans-serif`.

2. **Color generalization** — Slightly generalize colors from the original deck. A library template should work across multiple presentations, not be a perfect replica of one source deck. For branded templates, keep the signature accent color but make base backgrounds neutral.

3. **SVG minimalism** — SVG skeleton files should be clean and minimal. Every decorative element should serve the design system. Avoid redundant groups or unnecessary `defs`.

4. **Placeholder completeness** — Every dynamic text slot must use a `{{PLACEHOLDER}}`. Do not hardcode sample text in template SVGs.

5. **Directory convention** — The `template_id` directory goes under `skills/dog-slide/templates/layouts/`. File naming follows the `NN_page_type.svg` convention exactly.

6. **Existing template reference** — When in doubt about a design_spec section or SVG pattern, cross-reference an existing template in the library (e.g., `project_review`, `academic_defense`, `value_proposition`).

---

## Output Confirmation

After all steps complete, confirm to the user with a summary:

```markdown
**Template Creation Complete**

- **Template ID**: <template_id>
- **Path**: `skills/dog-slide/templates/layouts/<template_id>/`
- **Files Created**:
  - `design_spec.md`
  - `01_cover.svg`
  - `02_chapter.svg`
  - `03_content.svg`
  - `04_ending.svg`
- **Registered**: Yes / No
- **Validation**: Passed
```

The template is now ready for use. It can be referenced by path in future PPT generation requests: "Use `skills/dog-slide/templates/layouts/<template_id>/` as the template for this deck."
