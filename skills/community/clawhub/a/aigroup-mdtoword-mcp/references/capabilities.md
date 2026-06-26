# Markdown to Word MCP Capabilities

## Core operations

- `markdown_to_docx`: convert Markdown content or a Markdown file into a Word document
- `table_data_to_markdown`: convert structured table data into Markdown before document generation

## Feature coverage from the packaged server

- Native `.docx` output
- Styling system and reusable templates/resources
- Mathematical formulas
- Enhanced table support
- Headers, footers, and page numbers
- Local relative image fixes
- Stdio and HTTP transports in the upstream MCP package

## Task mapping

- Existing Markdown file:
  - Run `markdown_to_docx`.
- Notes plus tabular data:
  - Convert the table first with `table_data_to_markdown`, then generate the document.
- Technical or academic report:
  - Call out formulas and headings before conversion.
- Client-ready business memo:
  - Favor a concise structure, stable heading hierarchy, and polished page layout.

## Dependency

- MCP server name: `aigroup-mdtoword-mcp`
- Local launch pattern in this workspace: `npx -y aigroup-mdtoword-mcp`
- Upstream package metadata includes both `stdio` and `http` transports
