# corporate-doc-builder

A Claude Code skill for generating polished `.docx` documents by injecting Markdown content into Word templates.

## What It Does

Given a `.docx` template and reference materials, this skill guides a 6-stage pipeline:

1. **Template Analysis** — Extract TOC, audit styles, plan chapter visuals
2. **Spec** — Write a design spec anchoring scope, sources, and style
3. **Plan** — Break work into per-chapter tasks (optional for simple docs)
4. **Research** — Summarize source materials with traceability annotations
5. **Authoring** — Draft each chapter as an independent Markdown file
6. **Injection** — Render Mermaid diagrams to PNG, inject Markdown into the template

## Key Features

- Preserves template cover page, TOC, fonts, headers, and footers
- All diagrams via Mermaid (rendered to PNG, embedded as inline shapes)
- Per-chapter Markdown files for token budget control
- Built-in fixes for common `.docx` template pitfalls:
  - Fixed line spacing clipping images
  - Heading auto-numbering causing double numbers
  - Non-Mermaid code blocks being silently dropped

## Files

```
corporate-doc-builder/
  SKILL.md                      # Main skill (install this)
  scripts/
    inject_docx.py              # Markdown -> .docx injection
    render_mermaid.py           # Mermaid -> PNG rendering
    puppeteer-config.json       # mmdc --no-sandbox for Linux
```

## Requirements

- Python 3.8+ with `python-docx` and `Pillow`
- Node.js with `npx` (for Mermaid CLI)

```bash
pip install python-docx Pillow
```

## Quick Start

```bash
# 1. Render Mermaid diagrams
python scripts/render_mermaid.py full_draft.md ./images

# 2. Inject into template
python scripts/inject_docx.py \
    --md-dir ./chapters \
    --template ./template.docx \
    --output ./output.docx \
    --chapters ch01.md ch02.md ch03.md appendix.md \
    --header-replace "XXX=My Project Name"
```

## Publishing to ClawHub

The skill directory is already in ClawHub-compatible format (folder slug `corporate-doc-builder`, `SKILL.md` with semver frontmatter, text-only supporting files).

```bash
# Install the ClawHub CLI if you haven't
npm install -g clawhub

# Publish from the skill directory
cd corporate-doc-builder
clawhub publish
```

All published skills are licensed under MIT-0.
