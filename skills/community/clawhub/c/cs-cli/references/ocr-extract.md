# OCR Recognition and Content Extraction Workflow

> **Preread**: `references/image-processing.md` for `ocr`/`convert`/`merge-text` parameters, and `references/pdf-processing.md` for `pdf convert` parameters.

Commands below identify routes; supply input paths and save options from `SKILL.md` when executing. TXT and stdout output do not support cloud saving; do not change the requested format just to provide a cloud link.

## Scenario

The user needs to extract text content from images or PDFs.

## Decision Tree

| User Need | Best Approach | Notes |
|-----------|---------------|-------|
| Plain text only | `image ocr` | Prints to stdout; does not support `-s` |
| Preserve structure such as headings and lists | `image convert --format md` | Markdown format |
| Extract multiple images into one text document | `image merge-text --format md` | Up to 100 images |
| Extract a PDF as Markdown | `pdf convert --format md` | |
| Need editable Word | `image convert --format word` | Preserves layout |

## Selection Logic

1. **Is the input a PDF?** Use `pdf convert --format xx`.
2. **Are the inputs multiple images?** Use `image merge-text` for plain text or `image merge-word` to preserve layout.
3. **Is the input a single image?** Choose `image ocr` or `image convert` based on the required output format.

## Multi-Page Document Handling

When multiple images need to be combined into one document:

- Plain text: `image merge-text` -> stdout or `-o` output.
- Formatted document: `image merge-word`; without a save preference use `-o merged.docx -s` and a contextual cloud title.
