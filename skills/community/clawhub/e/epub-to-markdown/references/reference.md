# EPUB to Markdown — Reference

## Title Resolution

Resolve chapter titles in this order:

1. TOC entry matching the spine item's filename
2. Fallback title derived from the source filename, for example `part_01.xhtml` → `Part 01`

If the EPUB has a malformed or empty TOC, expect more fallback titles.

## Output Safety

The converter does **not** delete an existing output directory by default.

- Use a new output path when possible.
- Pass `--overwrite` only when the user explicitly wants to replace a previous generated export.

## Slugs and Filenames

Chapter filenames follow `{index:03d}_{slug}.md`.

- Lowercase titles
- Strip most punctuation
- Convert spaces and underscores to hyphens
- Cap slugs at 60 characters
- Append numeric suffixes for duplicates: `introduction`, `introduction-2`, and so on

Image filenames are sanitized similarly. Duplicate image names get numeric suffixes.

## Images

- Extract image assets into `images/`
- Rewrite chapter image links to `../images/{filename}`
- Match both full internal EPUB paths and bare filenames

## Word Count Heuristic

Compute chapter size after Markdown conversion.

- For CJK-heavy text, count CJK characters directly
- Otherwise, count whitespace-delimited words

CJK detection covers Chinese ideographs plus common Japanese and Korean blocks.

## Dependencies

The script uses `uv` inline metadata for dependencies:

- `ebooklib>=0.18`
- `beautifulsoup4>=4.12`
- `markdownify>=0.11`

## Known Limitations

- DRM-protected EPUBs cannot be processed
- Some EPUB3 books with heavy JavaScript behavior may extract incompletely
- SVG assets are preserved as-is and may not render in every Markdown viewer
- Chapter structure still depends on the EPUB spine and TOC quality
