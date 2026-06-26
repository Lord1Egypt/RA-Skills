---
name: "epub-read"
slug: "epub-read"
version: "2.0.0"
description: "Task-mode-driven EPUB reading and analysis skill with overview, targeted reading, chunked full reading, extraction, complex-content inspection, and batch processing."
changelog: "English-source release for GitHub and international ClawHub publishing."
metadata: {"clawdbot":{"emoji":"📚","os":["linux","darwin","win32"],"requires":{"bins":["python3"]}}}
---

<objective>
Provide a strict, auditable EPUB workflow that safely handles long books through explicit task routing instead of loading full-book text by default.
</objective>

<use_when>
- The user mentions an `.epub` file or ebook
- The user wants a quick structural overview
- The user wants chapter-specific or chunk-specific reading
- The user wants full-book sequential reading with chunking
- The user wants structured extraction
- The user wants to inspect images, tables, or other complex content
- The user wants to batch-process multiple EPUB files
</use_when>

<process>

**STEP 0 - Choose exactly one task mode before doing anything else**

| Mode | Purpose | Use when |
|------|---------|----------|
| `overview` | Fast structural overview | Metadata, TOC, themes, structure only |
| `targeted_read` | Focused reading | Specific chapters, chunk ranges, or keyword hits |
| `full_read` | Sequential reading | Long-book chunked reading with saved progress |
| `extract` | Structured extraction | Keywords, definitions, quotes, examples, action items, entities, tables, lists |
| `complex_content` | Complex-layout inspection | Images, tables, SVG, low-text sections |
| `batch` | Multi-book planning | Multiple EPUB files or folders |

Default to `overview` or `targeted_read` when the user intent is ambiguous. Never load a long book's full body text by default.

**STEP 1 - Parse if needed**

1. Check whether the output directory already exists and contains `manifest.json`.
2. If not, run `parse_epub.py`.
3. After parsing, report:
   - title
   - author
   - chapter count
   - chunk count if available
   - image count
   - table count
   - output directory

**STEP 2 - Build an execution plan**

Use `task_router.py` to decide whether parsing, chunking, or state updates are required:

```bash
python3 task_router.py <book_dir> --mode <mode> [params...]
```

The plan should tell you:
- whether parsing is required
- whether chunking is required
- which files are recommended to read
- whether session state must be updated

**STEP 3 - Mode-specific behavior**

### overview

- Read only metadata, TOC, reading index, and other structural outputs
- Do not load the whole book body by default
- Return:
  - title
  - author
  - chapter count
  - TOC structure
  - theme overview
  - suggested next actions

### targeted_read

Support:

- `--chapter`
- `--chapter-id`
- `--chunk-start`
- `--chunk-end`
- `--keyword`

Return:

- the requested section
- short context
- concise summary

### full_read

- Prefer chunk-based reading for long books
- Support continue, previous, next, and jump flows
- Always update `session_state.json`
- Never pretend progress exists if the session state is missing

### extract

Support extracting:

- keywords
- definitions
- quotes
- examples
- action_items
- names
- locations
- organizations
- tables
- lists

Return a hit list with chapter references and short context.

### complex_content

Inspect:

- images
- SVG
- tables
- image-heavy sections
- low-text / high-resource sections

Return a structured report. OCR is not required by default.

### batch

Support:

- multiple EPUB file paths
- directory scanning
- batch planning
- batch extraction requests

Return success / failure counts and a concise overview.

**STEP 4 - Long-book safety rules**

- Never push the full body of a long book into context at once
- Prefer `chunks/` over chapter markdown for full sequential reading
- When chunking is required, run `chunk_book.py` first
- Use `reading_index.json` to map chapters to chunk ranges

**STEP 5 - State management rules**

When running `full_read` or any progress-sensitive flow:

1. Read `session_state.json` first
2. Update it after every progress-changing action
3. Respect existing saved progress unless the user explicitly asks to restart

**STEP 6 - Output style**

Be explicit about:

- what files were used
- what mode was selected
- why a long book was chunked instead of loaded fully
- what the user can do next

When possible, point the user toward the safest next step:

- continue reading
- jump to a chapter
- inspect a chunk range
- extract a structure
- review complex content

</process>

<validation>

Before considering the task complete, check:

- parsing outputs exist
- chunk files exist when required
- reading index and session state are coherent
- extraction targets match the requested type
- complex-content reports are generated from real parsed outputs

</validation>
