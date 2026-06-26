---
name: corporate-doc-builder
version: 1.0.0
description: Generate polished .docx documents by injecting Markdown content into an existing Word template, preserving the template's cover page, TOC, fonts, headers, and footers. Use when the user has a .docx template plus reference materials (documents, spreadsheets, slides, or source code) and wants a production-ready Word deliverable. Covers the full pipeline from template analysis through chapter drafting to python-docx injection.
metadata:
  openclaw:
    requires:
      bins:
        - python3
        - npx
    install:
      - kind: uv
        packages:
          - python-docx
          - Pillow
          - openpyxl
---

# Corporate Doc Builder

## Overview

Turning a corporate .docx template plus scattered source materials into a finished document is error-prone. Models routinely break template styles, exceed token limits, hallucinate TOC entries, and produce images that overlap with text.

This skill codifies a battle-tested 6-stage pipeline that avoids these traps:

```
1. Template Analysis  ->  Extract TOC, styles, placeholders
2. Spec               ->  Write a design spec for the document
3. Plan               ->  Break work into per-chapter tasks (optional for simple docs)
4. Research           ->  Summarize source materials into reusable notes
5. Authoring          ->  Write each chapter as an independent Markdown file
6. Injection          ->  Render diagrams + inject Markdown into the template
```

**Core principle:** Template styles are preserved via `python-docx` copy-and-inject, never via `pandoc` whole-file conversion. All diagrams use Mermaid.

## When to Trigger

Activate this skill when ANY of the following apply:

- The user asks to "write a document based on a template" or "generate a report from a template"
- A task mentions both a `.docx` template path AND source/reference materials
- The user requires "cover page / TOC / fonts / headers / footers must match the template"
- The user asks to produce a corporate design document (outline design, detailed design, database design, interface design, architecture specification, technical white paper, etc.)
- The task involves `.docx` template + `.xlsx` feature lists + `.pptx` architecture diagrams or similar mixed enterprise assets

Do NOT activate when:

- The output is a plain Markdown, README, or blog post with no template
- The user just wants to locally edit an existing `.docx` (use the `docx` skill instead)
- No fixed template is involved

## The 6-Stage Pipeline

Each stage has a pre-flight checklist and exit criteria. **Do not skip stages or run them in parallel.**

---

### Stage 1: Template Analysis

**Goal:** Understand the template structure and agree on a TOC mapping with the user.

> **Companion skill:** If `superpowers:brainstorming` is available, invoke it at the start of this stage to systematically explore user intent and requirements before committing to a TOC mapping.

#### Pre-flight Checklist

| Item | Action |
|------|--------|
| Output directory | `ls` to verify it exists; fix typos before proceeding |
| Source material paths | `ls` each path to confirm accessibility |
| Template file | `ls -la <template>.docx` to confirm it exists and is not locked |
| Historical drafts | If prior output exists, read the first chapter to verify it belongs to THIS document |

#### Extract Template TOC

```python
from docx import Document
doc = Document(template_path)
for p in doc.paragraphs:
    if p.style.name.startswith("Heading") or p.style.name.startswith("toc"):
        print(p.style.name, p.text)
```

Some templates use custom styles (e.g., `CJ1`, `CJ2`) instead of standard `Heading` styles. Scan all paragraph styles and identify which ones act as headings.

#### Extract Template Images and Tables

Templates often contain placeholder images and tables. Extract them to plan which chapters need diagrams or data tables:

```python
# Count images
print(f"Images: {len(doc.inline_shapes)}")
# Count tables
print(f"Tables: {len(doc.tables)}")
```

#### TOC Mapping Rules

Templates often say "keep titles consistent." The real meaning is:

- **Top-level chapter titles** (1, 2, 3, ...): Keep them exactly as the template defines.
- **Sub-section titles** (1.1, 1.1.1, ...): Rewrite them to match the actual product/project. Do NOT copy the template's placeholder examples.
- **Style consistency**: Match the template's tone (imperative verbs, clause-style statements, etc.)
- **Placeholder text**: Replace ALL placeholder words (e.g., "XXX System", "Oracle Database", "SOA Architecture") with the actual technology stack and business domain.

#### Exit Criteria

- TOC mapping table reviewed and confirmed by the user
- Work approach decided (write from scratch / reuse prior drafts / partial reuse)
- Output directory, source material whitelist, and module scope are all explicit

---

### Stage 2: Spec

**Goal:** Write a design spec that anchors all subsequent work.

Write to `<output>/spec/<YYYY-MM-DD>-<topic>-spec.md`. Include at minimum:

1. Goal and scope
2. Source material constraints (whitelist of allowed paths)
3. Workflow overview
4. Complete TOC (user-confirmed)
5. Writing style baseline (language, depth, terminology)
6. Token budget protection strategy
7. Deliverables list
8. Confirmed key decisions
9. Open items

**Self-check** before submitting for review: scan for leftover placeholders, internal inconsistencies, scope creep, and ambiguity.

#### Exit Criteria

- User has reviewed and approved the spec

---

### Stage 3: Plan (Optional)

**Goal:** Break the work into per-chapter tasks for complex documents.

Skip this stage for simple documents (fewer than 5 chapters). For larger documents, write to `<output>/plans/<YYYY-MM-DD>-<topic>-plan.md` with tasks grouped into:

- **Research phase**: 2-3 tasks (source code analysis, reference doc summary, feature mapping)
- **Authoring phase**: One task per chapter
- **Injection phase**: 2 tasks (Mermaid rendering, docx injection)

Each task should have bite-sized steps (2-5 minutes each). **Per-chapter independent delivery + independent review** is the key token budget protection mechanism.

---

### Stage 4: Research

**Goal:** Extract and summarize source materials into reusable research notes.

Suggested output files in `<output>/research/`:

| File | Content |
|------|---------|
| `code-architecture.md` | Top-level module structure, key packages, tech stack, critical data flows |
| `reference-docs-summary.md` | Heading outline + key table/figure index for each reference document |
| `feature-mapping.md` | Feature list (from xlsx/pptx) mapped to target TOC chapters |
| `<topic>-inventory.md` | Domain-specific inventory (e.g., interface list, data model list, API catalog) |

#### Summarization Principle

Reference documents are **fact anchors**, not **content sources**. Extract headings, table titles, and key data. **Never copy full text** into research notes.

#### Source Traceability Rule

**Every TOC entry must have a traceable source** (source code path, reference document section, or feature list row). If a TOC entry has no source, delete it from the TOC rather than drafting content without evidence.

#### Extraction Snippets

```python
# Extract headings from .docx
from docx import Document
doc = Document(path)
for p in doc.paragraphs:
    if p.style.name.startswith("Heading"):
        print(p.style.name, p.text)

# Extract structured data from .xlsx
import openpyxl
wb = openpyxl.load_workbook(path)
for sh in wb.sheetnames:
    for row in wb[sh].iter_rows(values_only=True):
        print(row)

# Bulk-extract embedded images from .docx
# unzip -j <path>.docx 'word/media/*' -d ./extracted_imgs/
```

#### Exit Criteria

- All research notes delivered and reviewed by the user
- Every TOC entry has a source annotation

---

### Stage 5: Authoring

**Goal:** Write each chapter as an independent Markdown file.

#### File Layout

```
<output>/<doc>_md/
  ch01_<topic>.md
  ch02_<topic>.md
  ch03_<topic>_p1.md      # Split large chapters into parts
  ch03_<topic>_p2.md
  ...
  chNN_<topic>.md
  appendix_a.md
  full_draft.md            # Final concatenation
```

#### Why Per-Chapter Files

- Keeps each request within token limits
- Enables per-chapter user review; problems surface early
- Rewriting one chapter does not affect others

#### Mermaid Diagrams

> **Companion skill:** If `claude-mermaid:mermaid-diagrams` is available, invoke it before writing Mermaid blocks. It provides syntax best practices, diagram type selection, and live preview tools that produce significantly higher-quality diagrams.

- Use fenced ` ```mermaid ` code blocks in Markdown
- Do not embed image placeholders; actual images are generated during injection
- Complex diagrams (deployment, sequence) should be individually numbered for easy replacement
- Do not hardcode colors or themes in Mermaid source; handle theming during rendering
- `sequenceDiagram` does NOT support `style` directives; avoid them

#### Merge

```bash
cat ch01_*.md ch02_*.md ... chNN_*.md appendix_*.md > full_draft.md
```

After merging, review once for: TOC continuity, chapter numbering consistency, and Mermaid block count.

#### Exit Criteria

- All chapters reviewed and approved by the user
- `full_draft.md` created with correct chapter order

---

### Stage 6: Injection

**Goal:** Render Mermaid diagrams to PNG, then inject Markdown into the template to produce the final `.docx`.

#### Step 1: Render Mermaid to PNG

```bash
python scripts/render_mermaid.py <full_draft.md> <images_dir>
```

This extracts all ` ```mermaid ` blocks and renders each to `diagram_1.png`, `diagram_2.png`, etc.

#### Step 2: Inject into Template

```bash
python scripts/inject_docx.py \
    --md-dir <markdown_dir> \
    --template <template.docx> \
    --output <output.docx> \
    --chapters ch01.md ch02.md ... appendix_a.md
```

The script: copies the template, clears body content after the TOC, injects Markdown as styled paragraphs, embeds Mermaid PNGs, and forces TOC field refresh.

#### Pre-Injection Template Style Audit

**This is critical.** Before running injection, check the template's paragraph styles for issues that will corrupt the output:

```python
from docx import Document
doc = Document(template_path)
normal = doc.styles['Normal']
pf = normal.paragraph_format
print(f"Normal: line_spacing_rule={pf.line_spacing_rule}, line_spacing={pf.line_spacing}")
for style in doc.styles:
    if style.name and style.name.startswith("Heading"):
        pPr = style.element.find('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}pPr')
        if pPr is not None:
            numPr = pPr.find('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}numPr')
            if numPr is not None:
                print(f"WARNING: {style.name} has numPr (auto-numbering)")
```

Check for these three issues and apply fixes:

| Issue | Symptom | Fix |
|-------|---------|-----|
| Normal style has `line_spacing_rule = EXACTLY` | Images are clipped to line height and overlap with text | Override image paragraphs with `line_spacing_rule = SINGLE` |
| Heading styles have `numPr` elements | Double numbering: "1.1.1  2.1.1 Title" | Strip `numPr` from all Heading styles before injection |
| Non-Mermaid code blocks ignored | JSON/SQL/pseudocode blocks are blank in .docx | Render code blocks as shaded monospace paragraphs |

See the [Template Style Pitfalls](#template-style-pitfalls) section for details.

#### Exit Criteria

- `.docx` opens correctly in Word/LibreOffice
- Cover page, TOC, headers, footers match the template
- All images display correctly with no text overlap
- All code blocks are rendered as monospace shaded paragraphs
- TOC updates correctly when refreshed (Ctrl+A, F9 in Word)

---

## Template Style Pitfalls

These issues were discovered across 4 production document generations. They are **universal** to any `.docx` template injection workflow.

### Pitfall 1: Image Clipping from Fixed Line Spacing

**Root cause:** Many corporate templates set the `Normal` paragraph style to `line_spacing_rule = EXACTLY` with a fixed height (e.g., 26pt). When an image is inserted into a paragraph inheriting this style, the paragraph height is locked to 26pt regardless of image size. The image overflows and overlaps subsequent text.

**Fix:** Explicitly set `line_spacing_rule = SINGLE` on every image paragraph:

```python
from docx.enum.text import WD_LINE_SPACING
from docx.shared import Pt, Cm

def add_image(doc, img_path, max_w_cm=14.0, max_h_cm=12.0):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pf = p.paragraph_format
    pf.space_before = Pt(6)
    pf.space_after = Pt(6)
    pf.line_spacing_rule = WD_LINE_SPACING.SINGLE  # Override EXACTLY
    run = p.add_run()
    w_cm, h_cm = image_size_cm(img_path, max_w_cm, max_h_cm)
    run.add_picture(img_path, width=Cm(w_cm), height=Cm(h_cm))
```

Also cap `max_h_cm` at 12 (not 18) to prevent a single image from filling the entire page.

### Pitfall 2: Double Numbering from Heading numPr

**Root cause:** Some templates configure Heading styles with `numPr` (automatic numbering at the style level). When the Markdown heading text already contains manual numbering (e.g., "2.1.1 System Architecture"), the output shows "1.1.1  2.1.1 System Architecture" - the style's auto-number prepended to the manual number.

**Fix:** Strip `numPr` from all Heading styles before injecting content:

```python
WNS = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'

def strip_heading_auto_numbering(doc):
    for style in doc.styles:
        if style.name and style.name.startswith("Heading"):
            pPr = style.element.find(f'{WNS}pPr')
            if pPr is not None:
                numPr = pPr.find(f'{WNS}numPr')
                if numPr is not None:
                    pPr.remove(numPr)
```

### Pitfall 3: Missing Code Blocks

**Root cause:** Injection scripts that only handle Mermaid fenced blocks often skip other code blocks (JSON, SQL, pseudocode, curl examples), leaving blank spaces in the output.

**Fix:** Collect non-Mermaid code block lines and render them as shaded monospace paragraphs:

```python
from docx.shared import Pt, RGBColor
from docx.oxml.ns import qn

def add_code_block(doc, lines):
    code_text = "\n".join(lines)
    p = doc.add_paragraph()
    pPr = p._element.get_or_add_pPr()
    shd = docx.oxml.OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), 'F2F2F2')
    pPr.append(shd)
    run = p.add_run(code_text)
    run.font.name = "Consolas"
    run.font.size = Pt(9)
    run.font.color.rgb = RGBColor(0x33, 0x33, 0x33)
```

### Pitfall 4: Template Placeholder Text Leaking

**Root cause:** Template headers, footers, and cover pages contain placeholder text ("XXX Project", "XXXX System"). If not replaced, the output ships with the wrong project name.

**Fix:** Scan and replace header/footer text during the injection step:

```python
for section in doc.sections:
    for header_para in section.header.paragraphs:
        for run in header_para.runs:
            if "XXX" in run.text:
                run.text = run.text.replace("XXX", actual_project_name)
```

---

## Token Budget Protection

LLM context windows have hard limits. These strategies prevent token overflow during document generation:

| Strategy | Stage |
|----------|-------|
| Per-chapter independent Markdown files | Authoring |
| Research notes are summaries, not full-text copies | Research |
| Read source code on demand (`ls` + `Read`), never dump entire directories | Research |
| Compress long lists into tables | All stages |
| Per-chapter review checkpoints | Authoring |
| Never load all chapters into a single request | Authoring / Injection |

---

## Common Pitfalls

| Symptom | Root Cause | Fix |
|---------|-----------|-----|
| Path typos or directories do not exist | No pre-flight path validation | `ls` every path in the whitelist before starting |
| Wrong draft used as starting point | Did not verify which document a prior draft belongs to | Read the first chapter to confirm the topic |
| Template placeholder text appears in output | Treated "keep titles consistent" as "keep content identical" | Keep top-level titles; rewrite sub-sections for the actual project |
| Chapter organization does not match the product | Organized by code modules instead of user-facing capabilities | Organize by product capability, not by engineering repo structure |
| Token limit errors | Too many chapters loaded at once | Per-chapter files + summarized research |
| pandoc destroys template fonts/headers/footers | Used pandoc instead of python-docx | Always use python-docx template copy + injection |
| Reference doc text copied verbatim into chapters | Treated source material as content rather than fact anchors | Research phase produces summaries only |
| TOC entries have no source evidence | Concept-level headings imported without code/doc backing | Research phase: annotate every entry with a source; delete unsupported entries |
| "1.1.1  2.1.1 Title" double numbering | Template Heading styles have `numPr` auto-numbering | Strip `numPr` before injection |
| JSON/SQL/pseudocode blocks are blank in .docx | Injection script skips non-Mermaid code blocks | Render code blocks as shaded monospace paragraphs |
| Images overlap with text or are clipped | Template Normal style uses `EXACTLY` line spacing | Set image paragraph `line_spacing_rule = SINGLE`; cap `max_h_cm` at 12 |

---

## Reference Implementation

This skill includes ready-to-use Python scripts in the `scripts/` directory:

### `scripts/render_mermaid.py`

Extracts all ` ```mermaid ` blocks from a Markdown file and renders each to `diagram_N.png` using `mmdc` (Mermaid CLI).

```bash
python scripts/render_mermaid.py <markdown_file> <output_image_dir>
```

Requirements: `npx` (Node.js), which auto-installs `@mermaid-js/mermaid-cli`.

### `scripts/inject_docx.py`

Copies a `.docx` template, clears the body after the TOC, and injects Markdown content as properly styled Word elements.

```bash
python scripts/inject_docx.py \
    --md-dir ./output/chapters_md \
    --template ./templates/design_spec.docx \
    --output ./output/design_spec.docx \
    --chapters ch01.md ch02.md ch03.md appendix_a.md \
    --header-replace "XXX=My Project Name"
```

Features:
- Heading injection (levels 1-3)
- Markdown table to Word table conversion
- Bold and inline code formatting
- Mermaid PNG image embedding with correct sizing
- Non-Mermaid code block rendering (shaded monospace)
- Heading `numPr` auto-numbering removal
- Image paragraph `SINGLE` line spacing (prevents clipping)
- TOC field auto-refresh on open
- Optional header/footer text replacement

Requirements: `python-docx`, `Pillow`.

### `scripts/puppeteer-config.json`

Disables Chromium sandboxing for `mmdc` in Linux/container environments:

```json
{ "args": ["--no-sandbox"] }
```

---

## Companion Skills (Optional Enhancements)

This skill is fully self-contained — it works without any companion skills installed. However, if the following skills are available in your environment, they significantly improve specific stages:

| Skill | Stage | Benefit |
|-------|-------|---------|
| `claude-mermaid:mermaid-diagrams` | Stage 5 (Authoring) | Provides Mermaid syntax best practices, diagram type selection guidance, and live preview/save tools (`mermaid_preview` / `mermaid_save`). Produces higher-quality diagrams than writing Mermaid from scratch. |
| `superpowers:brainstorming` | Stage 1 (Template Analysis) | Structured brainstorming workflow that explores user intent, requirements, and design alternatives before committing to a TOC mapping. Reduces rework. |
| `superpowers:writing-plans` | Stage 3 (Plan) | Structured planning workflow for multi-step implementation tasks. Helps break complex documents into well-scoped per-chapter tasks. |

**How to use them:** If a companion skill is available, invoke it via the Skill tool at the relevant stage. If it is not available, follow the inline guidance in this skill — the core instructions for each stage already cover the essential techniques.

**Example:** During Stage 5, if `claude-mermaid:mermaid-diagrams` is installed, invoke it before writing Mermaid blocks. If not, follow the Mermaid guidelines in the [Authoring](#stage-5-authoring) section directly.

---

## Pre-Flight Checklist

Use this checklist when starting any new document:

- [ ] Verify output directory exists
- [ ] Verify all source material paths are accessible
- [ ] Verify template file exists and is not locked
- [ ] Extract template TOC (headings + toc-styled paragraphs)
- [ ] Extract template images and tables to plan per-chapter visuals
- [ ] **Audit template styles**: check Normal `line_spacing_rule` and Heading `numPr`
- [ ] Confirm TOC mapping with the user (top-level fixed, sub-sections adapted)
- [ ] Write spec and get user approval
- [ ] Complete research with source traceability for every TOC entry
- [ ] Author each chapter as an independent Markdown file
- [ ] Merge into `full_draft.md` and review
- [ ] Render Mermaid diagrams to PNG
- [ ] Run injection script
- [ ] Open output `.docx` and verify: cover page, TOC refresh, image layout, code blocks
