# EPUB Bilingual Converter Skill

Convert EPUB books, magazines, and article collections into paragraph-aligned bilingual EPUBs.

An agent skill for converting EPUBs into source-first, paragraph-aligned bilingual editions.

This repository includes the skill instructions plus a small Python toolchain. It extracts EPUB structure into `extraction.json`, helps estimate translation token usage, lets an agent or human fill translations, and assembles a bilingual EPUB while preserving the original spine order, images, CSS, TOC pages, and source-first reading order.

## Features

- Extracts article/chapter content from EPUB and XHTML/HTML spine files.
- Preserves paragraph order and enforces one-to-one source/target alignment.
- Estimates translation token usage before large translation work starts.
- Assembles bilingual EPUBs with source paragraph first and target paragraph second.
- Keeps original assets, images, covers, fonts, OPF/NCX, and non-ad resources.
- Adds target-language summaries and a conversion report.
- Handles math-heavy EPUB content, including inline formula metadata, superscripts/subscripts, italic math variables, equation blocks, and stacked inline coefficients.
- Provides a patch script to rebuild existing bilingual EPUBs with the latest assembly fixes.

## Requirements

- Python 3.10+
- `beautifulsoup4`
- `lxml`

Install dependencies:

```bash
python3 -m pip install beautifulsoup4 lxml
```

For development and tests:

```bash
python3 -m pip install pytest
```

## Quick Start

Extract an EPUB:

```bash
python3 scripts/extract.py /path/to/book.epub /path/to/output --target-language "Simplified Chinese"
```

Estimate translation token usage:

```bash
python3 scripts/estimate_tokens.py /path/to/output/extraction.json
```

Fill translation fields in `extraction.json`:

- `title_dest_language`
- `section_dest_language`
- `translated_paragraphs`
- `summary_dest_language`

Do not change source fields such as `paragraphs`, `href`, `num`, or `plain_text`.

Assemble the bilingual EPUB:

```bash
python3 scripts/assemble.py /path/to/output/extraction.json
```

Outputs:

```text
/path/to/output/bilingual_<input filename>.epub
/path/to/output/summary/*.txt
/path/to/output/report.txt
```

## Workflow

### 1. Extract

`scripts/extract.py` reads the EPUB as a zip archive, finds the OPF spine, classifies pages, extracts translatable article/chapter paragraphs, and writes `extraction.json`.

```bash
python3 scripts/extract.py input.epub output_dir --target-language Chinese
```

### 2. Estimate

`scripts/estimate_tokens.py` gives a lightweight token estimate for the translation stage. It does not estimate local extraction or assembly work.

```bash
python3 scripts/estimate_tokens.py output_dir/extraction.json
```

Useful options:

```bash
python3 scripts/estimate_tokens.py output_dir/extraction.json \
  --max-source-chars 8000 \
  --retry-buffer 0.15 \
  --top 5
```

### 3. Translate

Translation is intentionally separate from extraction and assembly. Fill only the target-language fields in `extraction.json`.

Hard requirement:

```text
len(translated_paragraphs) == len(paragraphs)
```

Each `translated_paragraphs[i]` must translate exactly `paragraphs[i]`. Do not merge, split, reorder, omit, or add notes inside paragraph translations.

### 4. Assemble

`scripts/assemble.py` validates translation completeness and paragraph pairing before writing the final EPUB.

```bash
python3 scripts/assemble.py output_dir/extraction.json
```

The assembler refuses to build if article counts, paragraph counts, or required translation fields are incomplete.

## Rebuild an Existing Bilingual EPUB

If assembly logic changes, rebuild an existing bilingual EPUB from its original `extraction.json`:

```bash
python3 scripts/patch_bilingual_math.py /path/to/output/extraction.json
```

This is useful for applying newer math-rendering or layout fixes without re-translating the book.

## Math Rendering

The assembler includes EPUB-oriented math cleanup for translated paragraphs. It applies general formatting rules for common mathematical notation rather than book-specific replacements:

- Converts common LaTeX-like inline formula metadata into readable text.
- Formats superscripts, subscripts, mathematical variables, and rms-style notation.
- Renders supported inline coefficients as stacked HTML so numerator and denominator-style markers align vertically in EPUB readers.
- Clones source equation blocks after target translations when needed so numbered equations remain visible near the bilingual paragraph.

## Output Contract

`extraction.json` has this high-level shape:

```json
{
  "input_epub": "/path/to/book.epub",
  "output_dir": "/path/to/output",
  "target_language": "Chinese",
  "total_articles": 1,
  "articles": [
    {
      "num": 1,
      "title": "Source title",
      "title_dest_language": "Target title",
      "section": "Source section",
      "section_dest_language": "Target section",
      "href": "OEBPS/chapter.xhtml",
      "paragraphs": ["Source paragraph."],
      "translated_paragraphs": ["Target paragraph."],
      "plain_text": "Full source text...",
      "summary_dest_language": "Target summary.",
      "image_filename": null
    }
  ]
}
```

## Run Tests

```bash
pytest
```

Current tests cover:

- Extraction of book-style `div.para` chapters.
- Inline math title extraction.
- Paragraph order and source-first bilingual insertion.
- Div paragraph insertion.
- Math normalization and stacked binomial HTML rendering.
- Token estimation reports.
- Assembly validation failures for incomplete or mismatched data.

## Repository Layout

```text
SKILL.md                         Agent skill instructions
agents/openai.yaml               Skill agent config
scripts/extract.py               EPUB -> extraction.json
scripts/estimate_tokens.py       Translation token estimate
scripts/assemble.py              extraction.json -> bilingual EPUB
scripts/patch_bilingual_math.py  Rebuild with current assembler fixes
tests/                           Unit tests
docs/                            Design notes
```

## Use as an Agent Skill

The skill entry point is `SKILL.md`. Install or symlink this repository into your agent skills directory, then invoke it when converting EPUBs into bilingual editions.

The skill policy is conservative by design:

- Run token estimation before large translation work.
- Ask for user confirmation after the estimate.
- Do not call external translation APIs unless explicitly requested or approved.
- Keep extraction, translation, and assembly as separate stages.

## Notes

This toolchain does not perform translation by itself. It prepares structured source data, validates translated data, and assembles the final bilingual EPUB. Translation can be performed by the current agent/session, a human, or an explicitly approved translation provider.
