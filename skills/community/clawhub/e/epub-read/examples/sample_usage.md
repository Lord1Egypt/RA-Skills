# Sample Usage

## Example 1: Parse a book

```bash
python parse_epub.py ~/Books/sample.epub
```

## Example 2: Parse with custom output root and book_id

```bash
python parse_epub.py ~/Books/sample.epub \
  --output-dir ~/Desktop/epub_outputs \
  --book-id sample-book
```

## Example 3: Chunk the parsed result

```bash
python chunk_book.py .epub_read_output/sample-book
```

## Example 4: Chunk with custom settings

```bash
python chunk_book.py .epub_read_output/sample-book \
  --target-chars 3200 \
  --max-chars 4800 \
  --overlap-chars 250
```

## Example 5: Suggested AstronClaw reading workflow

1. Parse the EPUB
2. Run `task_router.py --mode overview`
3. Chunk the parsed output if the book is long
4. Read `manifest.json`
4. Report:
   - title
   - author
   - chapter count
   - chunk count
   - output directory
5. Use `toc.json` and `reading_index.json` to navigate
6. Read `chapters/*.md` for chapter-level work
7. Read `chunks/*.md` for detailed analysis

## Example prompt ideas

- Read this EPUB chapter by chapter
- Parse this ebook and show me the TOC
- Summarize chunk 12
- Compare chapter 3 and chapter 8
- Produce a full-book summary without loading the entire book at once
- Continue the next chunk from session_state.json
