---
name: drawio-to-html
description: Convert drawio/diagrams.net flowchart and diagram files into self-contained HTML pages with embedded SVG rendering. Use when the user uploads or mentions a .drawio file and wants to convert it to HTML, view it in a browser, or share it as a web page. Triggers on phrases like "drawio转html", "流程图转网页", "把drawio转成html", "drawio to html".
---

# Drawio to HTML

Convert drawio/diagrams.net XML files into standalone HTML pages with embedded SVG.

## Supported Input

- `.drawio` files (diagrams.net / draw.io native format)
- Files containing `mxGraphModel` XML structure

## Supported Output

- Self-contained `.html` files with embedded SVG
- No external dependencies — open directly in any browser
- Preserves original colors, shapes, rounded corners, diamonds, arrows, edge labels

## Workflow

### Step 1: Locate the drawio file

Get the file path from the user or workspace context.

### Step 2: Run the conversion script

Execute the bundled Python script:

```bash
python3 scripts/drawio2html.py <input.drawio> [output.html]
```

If `output.html` is omitted, the script defaults to `<input>.html` in the same directory.

### Step 3: Report results

Tell the user:
- Output file path
- File size
- Diagram name extracted from the XML
- Any nodes/edges that could not be rendered (if applicable)

## Node Shape Support

| drawio Style | SVG Output |
|-------------|-----------|
| `rounded=1` / `arcSize` | Rounded rectangle (pill or soft rounded) |
| `rhombus` | Diamond (decision nodes) |
| default | Rectangle with slight corner radius |

## Edge Support

- Orthogonal connectors with waypoints
- Solid and dashed lines
- Arrow markers
- Edge labels ("是"/"否" branch annotations)

## Limitations

- Does not render: swimlanes, images, complex gradient fills, custom shapes
- Text inside nodes is centered; multi-line text supported
- Only the first `<diagram>` element is rendered if multiple exist

## Script Reference

The conversion logic lives in `scripts/drawio2html.py`. It is a pure-Python script with no external dependencies beyond the standard library (`xml.etree`, `re`, `sys`, `os`).
