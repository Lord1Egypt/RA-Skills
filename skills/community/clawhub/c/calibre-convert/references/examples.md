# Calibre Convert Examples

## Common conversions

```bash
./scripts/convert_with_calibre.py ~/books/input.epub ~/books/output.pdf
./scripts/convert_with_calibre.py ~/books/novel.md ~/books/novel.epub
./scripts/convert_with_calibre.py ~/books/old.mobi ~/books/new.epub
./scripts/convert_with_calibre.py ~/books/source.docx ~/books/source.epub
./scripts/convert_with_calibre.py ~/books/page.html ~/books/page.epub
```

## Pass-through Calibre options

```bash
./scripts/convert_with_calibre.py ~/books/novel.md ~/books/novel.epub -- --title "Novel" --authors "Author Name"
./scripts/convert_with_calibre.py ~/books/input.epub ~/books/output.pdf -- --paper-size a4 --pdf-default-font-size 14
```

## Troubleshooting

- If `ebook-convert` is missing, install Calibre and confirm the binary is reachable.
- If Markdown conversion renders poorly, try normalizing headings and metadata first.
- If PDF output looks broken, prefer EPUB as an intermediate target and test layout options explicitly.
