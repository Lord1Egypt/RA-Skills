---
name: beautiful-pdf
description: Produce polished, print-ready PDFs from Markdown or HTML with Pandoc, WeasyPrint, reusable CSS, and a mandatory rendered-page review loop. Use for reports, proposals, briefs, CVs, invoices, letters, dossiers, and other documents where layout quality matters.
---

# Beautiful PDF

Turn structured content into a designed document, then inspect the rendered pages before delivery.

## Workflow

1. Choose the document pattern in [references/doc-types.md](references/doc-types.md).
2. Draft in Markdown for linear documents or HTML for custom layouts.
3. Start from [assets/default.css](assets/default.css) and select a restrained palette from [references/style-guide.md](references/style-guide.md).
4. Render:

   ```bash
   pandoc input.md --standalone --pdf-engine=weasyprint --css=assets/default.css -o output.pdf
   # Or, for hand-authored HTML:
   weasyprint input.html output.pdf
   ```

5. Rasterize every page and inspect it:

   ```bash
   python3 scripts/pdf-to-png.py output.pdf /tmp/pdf-qa --dpi 200
   ```

6. Fix overflow, weak hierarchy, widows/orphans, awkward breaks, clipped tables, low contrast, and inconsistent spacing. Render again until the pages are intentional.

## Guardrails

- Do not pass Pandoc `--metadata title` when Markdown already contains an H1; it duplicates the title.
- Keep source HTML static. WeasyPrint does not execute JavaScript.
- Use absolute or `file://` paths for local images and fonts.
- Preserve the original source alongside the PDF so later edits remain possible.
- Treat page inspection as part of completion, not an optional polish pass.
- Never silently install dependencies. If PyMuPDF, Pandoc, or WeasyPrint is missing, report the exact requirement.

## Output

Use a user-approved destination. When no convention exists, prefer:

```text
outputs/YYYY-MM-DD-descriptor.pdf
```

Before delivery, report the final page count, output path, and the visual issues checked.
