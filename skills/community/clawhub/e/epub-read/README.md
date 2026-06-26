# epub-read

`epub-read` is a task-mode-driven EPUB reading and analysis skill for AstronClaw, ClawHub, and GitHub distribution. Its main goal is to make long-book workflows safe and inspectable by splitting EPUB work into explicit modes instead of trying to load an entire book into context at once.

It supports overview, targeted reading, continuous chunked reading, structured extraction, complex-content inspection, and batch processing.

## Highlights

- Task-mode routing: six explicit modes for different reading goals
- Safer long-book handling: chunk-first workflows for full-book reading
- Persistent reading state: supports continue, previous, next, and chapter jumps
- Rich output artifacts: metadata, TOC, book-level markdown, chapter files, chunk files, reading index, and complex-content report
- Backward-compatible outputs: keeps existing parse and chunk outputs usable for older workflows

## Supported Modes

### A. overview

Read metadata, structure, and table of contents without loading the full body text.

### B. targeted_read

Read by chapter, chapter ID, chunk range, or keyword match.

### C. full_read

Read a long book sequentially in chunks while maintaining reading progress.

### D. extract

Extract structured information such as keywords, definitions, quotes, examples, action items, names, locations, organizations, tables, and lists.

### E. complex_content

Inspect images, tables, SVG content, and low-text / high-resource sections.

### F. batch

Process multiple EPUB files from one or more directories.

## Typical Use Cases

- Get a quick structural overview of an ebook
- Read only selected chapters or chunk ranges
- Safely continue through a long book without loading the full text
- Extract concepts, definitions, quotes, or action items from a parsed EPUB
- Review image-heavy or table-heavy sections
- Batch-scan a library of EPUB files

## Dependencies

- `python3`
- `beautifulsoup4`
- `lxml`

Install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Quick Start

### 1. Parse an EPUB

```bash
python3 parse_epub.py /absolute/path/to/book.epub
```

### 2. Generate an overview plan

```bash
python3 task_router.py /path/to/book_dir --mode overview
```

### 3. Chunk a long book

```bash
python3 chunk_book.py /path/to/book_dir --mode balanced
```

### 4. Start or continue full reading

```bash
python3 task_router.py /path/to/book_dir --mode full_read --start-chunk 1
python3 task_router.py /path/to/book_dir --mode full_read --continue
```

### 5. Run structured extraction

```bash
python3 task_router.py /path/to/book_dir --mode extract --extraction-types definitions quotes action_items
```

## Output Artifacts

Parsing produces a directory similar to:

```text
.epub_read_output/<book_id>/
├── metadata.json
├── toc.json
├── book.json
├── book.md
├── manifest.json
├── complex_content.json
├── reading_index.json
├── session_state.json
├── chapters/
└── chunks/
```

Key files:

- `reading_index.json`: chunk ranges, word counts, images, and table information per chapter
- `session_state.json`: current mode, current chapter, current chunk, last action, last query
- `complex_content.json`: images, tables, SVGs, and sections that may need manual review

## Validation

Use the lightweight integration test first:

```bash
python3 test_integration.py --epub /absolute/path/to/test.epub
python3 test_integration.py --epub /absolute/path/to/test.epub --full
```

## Repository Layout

```text
epub-read/
├── SKILL.md
├── README.md
├── LICENSE.md
├── parse_epub.py
├── chunk_book.py
├── task_router.py
├── update_session_state.py
├── test_integration.py
├── requirements.txt
├── templates/
├── examples/
└── agents/
```

## ClawHub Notes

This repository is the English-source version intended for GitHub and future ClawHub packaging. If you publish to ClawHub, keep `SKILL.md`, `README.md`, metadata, and templates aligned with this repository so the public registry stays consistent with the GitHub source.

## License

This project is released under the `MIT` license for public distribution and reuse.
