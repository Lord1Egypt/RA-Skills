---
name: aigroup-mdtoword-mcp
description: Use `aigroup-mdtoword-mcp` to convert Markdown into `.docx`. Route Markdown file conversion, generated Markdown conversion, table-to-Markdown preprocessing, formula handling, table handling, and page-layout requests here.
homepage: https://github.com/jackdark425/aigroup-mdtoword-mcp
---

# Markdown to Word MCP

Use `aigroup-mdtoword-mcp` for Markdown-to-`.docx` conversion.

## Route

1. Confirm the deliverable:
   - existing Markdown file to convert
   - Markdown content generated in the session
   - tabular data that should become Markdown before conversion
2. Choose the right operation:
   - `markdown_to_docx` for primary conversion
   - `table_data_to_markdown` when the raw input is structured table data
3. Ask or infer the output style only when it matters:
   - technical memo
   - business report
   - academic-style document
   - minimal document
4. If formulas, tables, headers, footers, or local images are important, mention that explicitly before conversion.
5. Return the path to the generated `.docx` and summarize any formatting assumptions.

## Requests

- Convert a finished Markdown note, report, or memo into `.docx`.
- Produce a polished Word deliverable from generated Markdown in the same run.
- Preserve formulas, structured tables, and page furniture such as headers or page numbers.
- Turn extracted or CSV-like table data into Markdown and then into Word.

## References

- Read [capabilities.md](./references/capabilities.md) for the server features and delivery checklist.
