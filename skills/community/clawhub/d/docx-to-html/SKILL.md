---
name: docx-to-html
description: "Use this skill whenever the user has a DOCX file (.docx) and wants to convert, read, view, extract content from, or process it in any way — including summarization, displaying in a browser, extracting tables or lists, or feeding into AI pipelines. Always use this skill for any task involving .docx files, even if the request seems simple. Triggers include: 'convert docx', 'open word file', 'read word document', 'extract tables from docx', or any mention of a .docx filename."
---

# DOCX to HTML Converter

This skill provides a straightforward method to convert Microsoft Word (.docx) documents into clean, semantic HTML, making them suitable for various web-based and AI-driven applications.

## Compatibility

- **Python 3** (for the conversion wrapper)
- **Node.js** with `mammoth` installed (core conversion engine)

To install Node.js dependencies, run once from the `scripts/` directory:
```bash
npm install
```

## Use Cases

- **Browser-Based Viewing**: Convert DOCX documents for display in web browsers without requiring Microsoft Word.
- **AI-Ready Content**: Prepare DOCX content for LLMs for tasks like summarization, Q&A, and semantic search.
- **Web Integration**: Integrate Word document content into web applications, CMS, or online editors.
- **Data Extraction**: Extract structured data (tables, lists, headings) from DOCX files for automated reporting and analysis.
- **Search and Indexing**: Enable full-text and vector search by converting DOCX content into easily indexable HTML.

## Workflow

1. **Locate DOCX File**: Identify the path to the `.docx` file to convert.

2. **Run Conversion Script**: Execute the Python wrapper from the skill's `scripts/` directory:
   ```bash
   python3 <skill-dir>/scripts/convert.py <input_path.docx> <output_path.html>
   ```
   Replace `<skill-dir>` with the actual path where this skill is installed.

3. **Verify Output**: Open the generated `.html` file in a browser and check:
   - Headings (`<h1>`, `<h2>`, etc.) appear at the correct hierarchy levels
   - Tables render with the expected rows and columns
   - Lists appear as bullet or numbered items (not plain text)
   - Bold, italic, and inline formatting are preserved
   - Images are visible (embedded as base64 by default)

4. **Process HTML**: Use the resulting HTML for further tasks like summarization, indexing, or display.

## Bundled Resources

- `scripts/docx-converter.js`: Core Node.js conversion logic using `mammoth.js`.
- `scripts/convert.py`: Python wrapper for invoking the Node.js converter.
- `scripts/package.json`: Node.js dependency manifest (includes `mammoth`).

## Technical Details

The conversion leverages `mammoth.js`, which prioritizes semantic meaning over visual replication:

- **Semantic Conversion**: Document structure maps to proper HTML — headings become `<h1>`/`<h2>`, lists become `<ul>`/`<ol>`, etc.
- **Basic Styling**: Bold, italics, and common paragraph styles are preserved.
- **Image Embedding**: Images are extracted and embedded as base64 data URIs in the HTML output.

## Troubleshooting

| Problem | Likely Cause | Fix |
|---|---|---|
| `node: command not found` | Node.js not installed | Install Node.js (v16+) |
| `Cannot find module 'mammoth'` | npm deps missing | Run `npm install` in `scripts/` |
| Empty or garbled output | Corrupted or password-protected DOCX | Try re-saving the file from Microsoft Word |
| Missing images | Large embedded images | Check `mammoth.js` image size limits in `docx-converter.js` |

## Limitations

- Advanced or highly specific styling from the original DOCX may not be perfectly replicated in the HTML output.
- Features like tracked changes, comments, or complex layout elements may be simplified or omitted.
