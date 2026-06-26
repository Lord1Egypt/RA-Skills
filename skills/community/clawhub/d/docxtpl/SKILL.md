---
name: docxtpl
description: Generate Word (.docx) documents from Jinja2 templates. Uses python-docx (read/write) + Jinja2 (template engine). Design templates in Microsoft Word, then populate with Python variables.
version: 0.0.1
homepage: https://docxtpl.readthedocs.io/en/latest/
pip: docxtpl
metadata:
  openclaw:
    requires:
      bins: ["python3"]
---

# docxtpl Skill

Use a `.docx` file as a Jinja2 template, then fill it with Python data at runtime.

## Installation

```bash
pip install docxtpl
# For subdocuments support:
pip install "docxtpl[subdoc]"
```

## Quick Start

```python
from docxtpl import DocxTemplate

doc = DocxTemplate("my_template.docx")
context = {"name": "Alice", "department": "Cardiology"}
doc.render(context)
doc.save("output.docx")
```

**Workflow:**
1. Design a `.docx` in Word with Jinja2 tags (`{{ var }}`, `{%p if ... %}`)
2. Load the template with `DocxTemplate(path)`
3. Build a Python context dict
4. Call `doc.render(context)` then `doc.save(path)`

## Tag Reference

| Tag | Scope | Purpose |
|-----|-------|---------|
| `{{ var }}` | inline string | Display a variable |
| `{{r var }}` | inline styled | Display a `RichText` object |
| `{%p ... %}` | paragraph | Control full paragraphs (if/for) |
| `{%tr ... %}` | table row | Control table rows |
| `{%tc ... %}` | table column | Control table columns |
| `{%r ... %}` | run | Control styled runs |
| `{%p if cond %}` / `{%p endif %}` | paragraph | Conditional paragraph |
| `{%p for x in list %}` / `{%p endfor %}` | paragraph | Loop over paragraphs |
| `{% colspan N %}` | table cell | Horizontal cell spanning |
| `{% hm %}` | table cell | Horizontal merge in for-loop |
| `{% vm %}` | table cell | Vertical merge in for-loop |
| `{% cellbg color %}` | table cell | Set cell background color |
| `{ #p comment #}` | paragraph | Comment |
| `{%- -%}` | text merge | Merge split lines |
| `{ _%`, `%_ }`, `{ _{`, `}_ }` | escape | Display literal `{%`, `%}`, `{{`, `}}` |

**Important:** Always put spaces around delimiters: `{{ var }}` not `{{var}}`.

## CLI Usage

```bash
python -m docxtpl template.docx data.json output.docx
python -m docxtpl -o template.docx data.json output.docx  # overwrite
```

## Key Classes

- **`DocxTemplate(path)`** — Load a `.docx` template. Methods: `.render(context)`, `.save(path)`, `.get_undeclared_template_variables(context=None)`
- **`RichText(text, ...)` / `R(text)`** — Styled text with `.add()` for multi-style concatenation
- **`InlineImage(tpl, img_path, width, height)`** — Dynamic image insertion (use `Mm()`, `Inches()`, or `Pt()` for dimensions)
- **`Listing(text)`** — Escaped text preserving `\n`/`\a`/`\f` without losing style
- **`RichTextParagraph()` / `RP()`** — Paragraph-level properties (use with `{{p var }}`)
- **`Subdoc`** — `tpl.new_subdoc(path)` to merge existing `.docx` files

## Media Replacement

For headers/footers where dynamic tags aren't supported:

```python
tpl.replace_pic("dummy.jpg", "real.jpg")      # pictures
tpl.replace_media("dummy.mp3", "real.mp3")     # any media
tpl.replace_embedded("dummy.docx", "real.docx") # embedded docs
tpl.replace_zipname("path/in/zip.xlsx", "real.xlsx") # raw zip entry
```

## Escaping

By default, no auto-escaping. Use one of:
- `RichText` for safe content
- `{{ var|e }}` in template
- `escape("text")` in Python context
- `tpl.render(context, autoescape=True)`

## Tips

- `\n` → newline, `\a` → new paragraph, `\t` → tab, `\f` → page break (in strings and `RichText`)
- To render a template multiple times, call `tpl.reset_replacements()` before each `render()` if using media replacements
- Pass a custom `jinja_env` to `render()` for custom Jinja2 filters
- Preview `get_undeclared_template_variables()` to warn about missing keys

📖 **Full API reference:** [references/official-docs.md](references/official-docs.md)

## CLI Scripts

Convenience scripts in `scripts/` (use `{baseDir}/scripts/` path):

```bash
# Render with inline key=value pairs
python scripts/docxtpl-render.py template.docx out.docx name="Alice" age="30"

# Render from JSON file
python scripts/docxtpl-render-json.py template.docx data.json out.docx

# Render from JSON string
python scripts/docxtpl-render.py template.docx out.docx --json '{"name":"Bob"}'

# List missing template variables
python scripts/docxtpl-list-vars.py template.docx

# Batch render from CSV (one .docx per row, named by id column)
python scripts/docxtpl-render-batch.py patients.csv ./reports/ template.docx \
  --id-column patient_id --suffix _report --summary
```
