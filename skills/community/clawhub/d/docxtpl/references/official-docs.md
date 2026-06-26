# Official docxtpl Documentation Reference

> Source: https://docxtpl.readthedocs.io/en/latest/
> Version: 0.20.x

## Introduction

This package uses 2 major packages:
- **python-docx** for reading, writing and creating sub documents
- **jinja2** for managing tags inserted into the template docx

**Workflow:**
1. Create an example of the document you want to generate with Microsoft Word (pictures, tables, headers, footers, etc.)
2. Insert Jinja2-like tags directly in the document while editing
3. Save as `.docx` (xml format) — this is your template
4. Use python-docx-template to generate as many Word documents from this template

## Jinja2-like Syntax

As the Jinja2 package is used, one can use all jinja2 tags and filters inside the word document.

### Restrictions

The usual jinja2 tags are only to be used inside the **same run** of a same paragraph. They cannot be used across several paragraphs, table rows, or runs.

A "run" for Microsoft Word is a sequence of characters with the same style. If you put bold text in the middle of a paragraph, Word splits it into 3 runs (normal - bold - normal).

### Extensions

Special syntax for paragraphs, table rows, table columns, and runs:

- `{%p jinja2_tag %}` — paragraphs
- `{%tr jinja2_tag %}` — table rows
- `{%tc jinja2_tag %}` — table columns
- `{%r jinja2_tag %}` — runs

These tags tell python-docx-template to put real Jinja2 tags in the right XML location and **remove** the paragraph/row/column/run containing the tag.

**IMPORTANT:** Always put spaces after opening delimiter and before closing:
- Correct: `{%p if display_paragraph %}`
- Wrong: `{%pif display_paragraph %}`

**IMPORTANT:** Do not use `{%p`, `{%tr`, `{%tc` or `{%r` twice in the same paragraph, row, column or run:
- Wrong: `{%p if display_paragraph %} Here is my paragraph {%p endif %}`
- Correct:
  ```
  {%p if display_paragraph %}
  Here is my paragraph
  {%p endif %}
  ```

### Display Variables

- `{{ var }}` — if `var` is a string, `\n`, `\a`, `\t` and `\f` are translated to newlines, new paragraphs, tabs, and page breaks
- `{{r var }}` — if `var` is a `RichText` object (note the `r` right after opening braces)
- If `var` is a `RichText` object, you must use `{{r var }}`

**VERY IMPORTANT:** Variables must not contain `<`, `>` and `&` unless using Escaping.

**IMPORTANT:** Always put space after opening var delimiter and before closing:
- Wrong: `{{myvariable}}`, `{{rmyrichtext}}`
- Correct: `{{ myvariable }}`, `{{ r myrichtext }}`

### Comments

- `{#p this is a comment as a paragraph #}`
- `{#tr this is a comment as a table row #}`
- `{#tc this is a comment as a table cell #}`

### Split and Merge Text

Use `{%-` to merge with previous line and `-%}` to merge with next line.

Example:
```
My house is located
{%- if living_in_town -%}
in urban area
{%- else -%}
in countryside
{%- endif -%}
and I love it.
```

**IMPORTANT:** Use an **unbreakable space** (CTRL+SHIFT+SPACE) when a space is wanted at line beginning or ending.

### Escaping Delimiters

- `{_%` → `{%`
- `%_}` → `%}`
- `{_{` → `{{`
- `}_}` → `}}`

## Tables

### Spanning

- `{% colspan var %}` — Horizontal cell spanning (var = integer)
- `{% hm %}` — Horizontal merge within a for-loop
- `{% vm %}` — Vertical merge within a for-loop

### Cell Color

`{% cellbg var %}` — Must be at the very beginning of a cell. `var` = hexadecimal color code without `#`.

## RichText

When you use `{{ var }}`, the variable keeps the current style. To add dynamically changeable style, use `{{r var }}` tag AND a `RichText` object.

```python
from docxtpl import RichText, R

# RichText(text, bold, italic, size, font, color, highlight, underline, strike, ...)
rt = RichText('Hello', bold=True, color='FF0000', size=24)
rt.add(' World', italic=True, font='Arial')  # concatenate

# Shortcut
rt = R('Hello', bold=True)
```

Features:
- `\n`, `\a`, `\t`, `\f` for newline, new paragraph, tab, page break
- Font region prefix: `ch = RichText('测试TEST', font='eastAsia:微软雅黑')`
- `.add()` method to concatenate multiple styles

**Important:** `{{r }}` removes current character styling. If no style specified in `RichText()`, it falls back to Word default style.

**Important:** Do not use `{{r` twice in the same run. Use `RichText.add()` instead.

**Important:** `RichText` objects are rendered into XML before filters. You cannot use `{{r var|lower }}`. Filter in Python when creating the `RichText` object.

### Hyperlink with RichText

```python
tpl = DocxTemplate('your_template.docx')
rt = RichText('You can add an hyperlink, here to ')
rt.add('google', url_id=tpl.build_url_id('http://google.com'))
```

Then use `{{r rt}}` in template.

### RichTextParagraph

```python
from docxtpl import RichTextParagraph, RP

rp = RP(align='center', space_before=Mm(10), space_after=Mm(5))
```

Use with `{{p var }}` in template.

## InlineImage

```python
from docxtpl import InlineImage
from docx.shared import Mm, Inches, Pt

myimage = InlineImage(tpl, 'python_logo.png', width=Mm(20), height=Mm(10))
```

Use as `{{ myimage }}` in template.

## Sub-documents

**Requires:** `pip install "docxtpl[subdoc]"`

```python
# Merge existing .docx as subdoc
sd = tpl.new_subdoc('templates/merge_docx_subdoc.docx')
context = {'mysubdoc': sd}

# Build from scratch using python-docx
subdoc = tpl.new_subdoc()
subdoc.add_paragraph('Built from scratch')
```

Use with `{{p mysubdoc }}` in template.

## Escaping

By default, **no escaping is done**. 4 ways to handle special chars (`<`, `>`, `&`):

1. `context = {'var': R('my text')}` + `{{r var }}` in template
2. `{{ var|e }}` in template
3. `context = {'var': escape('my text')}` (import from docxtpl)
4. `tpl.render(context, autoescape=True)`

### Listing

```python
from docxtpl import Listing

context = {
    'mylisting': Listing('the listing\nwith\nsome\nlines\aand some paragraph\aand special chars: <>&')
}
```

Use `{{ mylisting }}` in template. Keeps current character styling (except after `\a` which starts new paragraph).

## Replace Pictures

For headers/footers where dynamic tags don't work:

```python
tpl.replace_pic('dummy_header_pic.jpg', 'header_pic_i_want.jpg')
```

Replaces in headers, footers, and body. Aspect ratio is preserved. Specify only the basename (not full path).

## Replace Medias

```python
tpl.replace_media('dummy_header_pic.jpg', 'header_pic_i_want.jpg')
```

**WARNING:** Unlike `replace_pic()`, the dummy file **MUST exist** in the template directory at render/save time and must be the same file as the one inserted manually.

## Replace Embedded Objects

```python
tpl.replace_embedded('embedded_dummy.docx', 'embedded_docx_i_want.docx')

# Or for non-docx embedded objects using zip path:
tpl.replace_zipname(
    'word/embeddings/Feuille_Microsoft_Office_Excel1.xlsx',
    'my_excel_file.xlsx'
)
```

## Get Undeclared Template Variables

```python
tpl = DocxTemplate('your_template.docx')
tpl.render(context_dict)
missing = tpl.get_undeclared_template_variables(context=context_dict)
```

If context is omitted, returns a set of ALL keys needed (useful for prompting users or writing to a file).

## Multiple Rendering

Since v0.15.0, you can reuse a `DocxTemplate`:

```python
for ctx in contexts:
    if ctx.get('use_replacements'):
        tpl.reset_replacements()
    tpl.render(ctx)
    tpl.save(f"output_{ctx['id']}.docx")
```

## MS Word 2016 Special Cases

- `\t` tabulations are ignored in MS Word 2016 (LibreOffice/Wordpad work fine)
- Spaces at line beginnings after Jinja2 tags are ignored
- **Solution:** Use `RichText`:
  ```python
  tpl.render({
      'test_space_r': RichText(' '),
      'test_tabs_r': RichText(5 * '\t'),
  })
  ```
  Use `{{r test_space_r }}` and `{{r test_tabs_r }}` in template.

## Custom Jinja2 Filters

```python
import jinja2

def multiply_by(value, by):
    return value * by

doc = DocxTemplate("my_template.docx")
jinja_env = jinja2.Environment()
jinja_env.filters['multiply_by'] = multiply_by
doc.render(context, jinja_env)
```

Template: `Euros price: {{ price_dollars | multiply_by(0.88) }}`

## Command-line Execution

```
usage: python -m docxtpl [-h] [-o] [-q] template_path json_path output_filename

positional arguments:
  template_path   Path to the template docx file
  json_path       Path to the json file with the data
  output_filename Filename to save the generated docx

optional arguments:
  -h, --help      Show help and exit
  -o, --overwrite Overwrite existing output without confirmation
  -q, --quiet     Suppress unnecessary messages
```

## Examples

The best way to understand is to run the test suite:

```bash
cd tests/
python runtests.py
```

Generated files are in `tests/output/`. Docx templates are in `tests/templates/`.
