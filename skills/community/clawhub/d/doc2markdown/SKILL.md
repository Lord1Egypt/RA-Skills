---
name: doc2markdown
description: Lightweight document utility designed to convert files to Markdown (MD), built specifically for intelligent agents (e.g., OpenClaw, ClaudeCode) to read and process content. Requires no external dependencies and accurately preserves document structure and formatting. Supported formats include docx, doc, pdf, ppt, pptx, xls, xlsx, jpg, jpeg, png, ceb, teb, caj, odt, ofd, cebx, odp, ott, wps, ods, et, dps, epub, chm, sdc, sdd, sdw, mobi
homepage: https://lab.hjcloud.com/llmdoc
metadata: {"openclaw":{"emoji":"📄","requires":{"bins":["node"]}}}
---
# doc2markdown

Document conversion assistant that automatically converts documents to Markdown (MD), saving output to the same directory as the source file. Designed to help intelligent agents read and process document content in various formats.

## Quick Start

```bash
# Convert document (auto-polls for 60s, downloads if complete, returns doc ID if timeout)
node scripts/doc2markdown.js convert <file_path>     # Downloads MD package
node scripts/doc2markdown.js convert <file_path> --md  # Downloads single MD file

# Check status and download (for documents that exceeded timeout)
node scripts/doc2markdown.js check <doc_id> <original_file_path>     # Downloads MD package
node scripts/doc2markdown.js check <doc_id> <original_file_path> --md  # Downloads single MD file
```

## Capabilities

- Supported formats: docx, doc, pdf, ppt, pptx, xls, xlsx, jpg, jpeg, png, ceb, teb, caj, odt, ofd, cebx, odp, ott, wps, ods, et, dps, epub, chm, sdc, sdd, sdw, mobi, etc.
- Preserves document structure, tables, and images
- No API Key or account required, zero external dependencies
- Downloaded ZIP files are extracted to `{doc_id}_{filename}/` under the source file's parent directory; single MD files are saved directly there

## When to Use

- User requests to "read", "extract", "convert", or "view" a document
- User provides a document path and asks about its content
- User needs to summarize or analyze a document
- User needs to convert document content to Markdown package

## Download Modes

This tool supports two download modes:

- **`--md` mode**: Downloads a single merged MD file to the source file's parent directory. Images are not included
- **MD package**: Downloads and extracts a ZIP package to `{doc_id}_{filename}/` in the source file's parent directory. Includes image files and tables, tables are rendered in HTML format

### Choosing the Right Mode

| User Intent | Example Phrases | Mode to Use |
|---|---|---|
| Read / view / analyze a document | "read this file", "what's in this doc", "summarize this PDF" | `--md` (single MD file) |
| Explicitly convert to MD | "convert to MD", "export as markdown", "转成MD" | MD package (default, no `--md`); use `--md` only if user specifically asks for a single file |

## Workflow

### convert — Convert Document
1. Invoke file parsing service
2. Auto-poll conversion status (up to 60 seconds)
3. **Completes within 60s** → Auto-download to source file directory
4. **Exceeds 60s** → Return doc ID for subsequent `check` query

### check — Query and Download
1. Provide the previously returned doc ID
2. Download if complete, otherwise continue polling for 60 seconds
3. Prompt to retry later if still not complete

## Data & Privacy

- `convert` uploads files to the docchain cloud service (`lab.hjcloud.com`) for parsing. Results are returned as a ZIP archive and extracted locally.
- All transfers use HTTPS encryption.
- Users should ensure that documents do not contain sensitive or confidential information unless they have verified the service's data handling practices.
- Service endpoint: https://lab.hjcloud.com/llmdoc

## Feedback & Support

For parsing errors, format issues, or other problems, please submit an issue on GitHub:
https://github.com/wct-lab/docchain-skills