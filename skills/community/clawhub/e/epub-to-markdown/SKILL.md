---
name: epub-to-markdown
description: Convert EPUB books into an AI-ready Markdown library with a first-read META.md navigation index, per-chapter Markdown files, and extracted images. Use when the user wants to turn a .epub into Markdown for reading, summarization, analysis, retrieval, or downstream text processing, especially when the book should be explored chapter-by-chapter without loading the entire text at once.
---

# EPUB to Markdown Conversion

Convert an EPUB into a structured Markdown workspace using the bundled script.

## Run

```bash
uv run scripts/convert.py <path/to/book.epub> [output_dir]
```

- Omit `output_dir` to write beside the EPUB as `{epub_stem}/`.
- If `output_dir` already exists, the script stops instead of deleting it.
- Pass `--overwrite` only when the user explicitly wants to replace an existing generated directory.
- Dependencies are declared inline in the script, so `uv run` installs them automatically on first use.

## Output

```text
{output_dir}/
├── META.md
├── images/
└── chapters/
    ├── 001_{slug}.md
    ├── 002_{slug}.md
    └── ...
```

- Read `META.md` first. It contains book metadata, total chapter and word counts, and a chapter index pointing at the generated files.
- Read files in `chapters/` only when the user asks about specific content.

## Reply Format

After a successful conversion, report:

```text
✅ Conversion complete

Title   : {title}
Authors : {authors}
Chapters: {total_chapters}
Words   : {total_words}
Output  : {output_dir}/
```

If chapter titles look wrong, the TOC is sparse, or the user needs edge-case behavior details, read `references/reference.md`.