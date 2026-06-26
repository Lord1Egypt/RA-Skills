# Frontend CV

A Claude Code skill for creating professional, print-ready HTML resumes from any input format — PDF, Word, Markdown, or plain text.

## What This Does

**Frontend CV** transforms your existing resume into a polished HTML document that exports cleanly to PDF. No design skills required. Just provide your resume in any format, pick a visual style, and get a professional result.

### Key Features

- **Universal Input** — Accepts PDF, DOCX, Markdown, or plain text. Extracts and structures your data automatically.
- **Visual Style Selection** — Preview 5 professional themes with your actual content before choosing.
- **Print-First Design** — Every theme is optimized for PDF export via browser print (Cmd+P → Save as PDF).
- **Zero Dependencies** — Single HTML files with inline CSS. Works offline, no build tools needed.
- **Structured Data** — Converts unstructured resumes into clean YAML format for easy editing.

## Installation

### For Claude Code Users

Copy the skill files to your Claude Code skills directory:

```bash
# Create the skill directory
mkdir -p ~/.claude/skills/frontend-cv/scripts

# Copy all files
cp SKILL.md theme-presets.md html-template.md print-styles.css ~/.claude/skills/frontend-cv/
cp scripts/extract_resume.py scripts/render_html.py ~/.claude/skills/frontend-cv/scripts/
```

Or clone directly:

```bash
git clone https://github.com/your-repo/frontend-cv.git ~/.claude/skills/frontend-cv
```

Then use it by typing `/frontend-cv` in Claude Code.

## Usage

### Convert an Existing Resume

```
/frontend-cv

> "Convert my resume.pdf to HTML"
```

The skill will:
1. Extract text and structure from your document
2. Convert it to clean YAML format for review
3. Generate 5 visual previews with your real data
4. Create the final HTML in your chosen style
5. Open it in your browser for PDF export

### Build from Scratch

```
/frontend-cv

> "Help me create a resume"
```

The skill will guide you through an interactive conversation to gather your information and structure it properly.

### From Structured Data

```
/frontend-cv

> "Generate a resume from this YAML file"
```

If you already have structured data, skip straight to style selection.

## Included Themes

- **Classic** — Centered header with blue accents, stable and versatile
- **ModernCV** — Left-aligned header with side date column, contemporary feel
- **Sb2nov** — Academic serif typography, scholarly aesthetic
- **Engineering Classic** — Light blue engineering style, technical and clean
- **Engineering Resumes** — Black and white compact layout, maximum density

Each theme is designed to look professional in both screen and print formats.

## Architecture

This skill follows a phased workflow with on-demand file loading:

| File | Purpose | Loaded When |
|------|---------|-------------|
| `SKILL.md` | Core workflow and phases | Always (skill invocation) |
| `theme-presets.md` | 5 professional theme specs | Phase 2 (style selection) |
| `html-template.md` | HTML structure reference | Phase 3 (generation) |
| `print-styles.css` | Print CSS fallback reference | Phase 3 (generation) |
| `scripts/extract_resume.py` | Document text extraction | Phase 1 (extraction) |
| `scripts/render_html.py` | Theme renderer | Phase 2-4 (preview/generation) |

The bundled renderer (`render_html.py`) handles all theme generation, ensuring consistent output.

## Philosophy

This skill is built on these principles:

1. **Your content matters most.** The design should enhance, not distract from, your experience and skills.

2. **Print is the target.** A resume that looks great on screen but prints poorly is useless. PDF export is a first-class concern.

3. **Structure enables flexibility.** Clean YAML data means you can regenerate your resume in any style without starting over.

4. **Self-contained is sustainable.** A single HTML file will work forever. No dependencies to break, no frameworks to update.

## Requirements

- [Claude Code](https://claude.ai/claude-code) CLI
- Python 3.7+ with libraries: `PyPDF2`, `python-docx`, `pyyaml`, `jinja2`

Install Python dependencies:

```bash
pip install PyPDF2 python-docx pyyaml jinja2
```

## Export to PDF

After generating your HTML resume:

1. Open the file in any modern browser
2. Press **Cmd+P** (Mac) or **Ctrl+P** (Windows)
3. Select "Save as PDF" as the destination
4. Adjust margins if needed (usually "Default" works)
5. Save

The print styles are optimized for standard letter/A4 paper.

## License

MIT — Use it, modify it, share it.
