---
name: epub-bilingual-converter-skill
description: Process EPUB files into structured extraction JSON, guide AI paragraph-aligned translation and summary filling, then assemble bilingual EPUBs with target-language summaries and report.txt. Use when an agent needs to convert books, magazines, newsletters, Calibre-generated EPUBs, The Economist-style EPUBs, or other EPUB sources into bilingual editions while preserving spine order, images, CSS, TOC/index pages, and one-to-one paragraph alignment.
---

# epub-bilingual-converter-skill

## Overview

Use this skill to convert an EPUB into a bilingual EPUB through four separated stages:

1. Extract structure with `scripts/extract.py`.
2. Estimate translation token budget with `scripts/estimate_tokens.py`.
3. Fill only target-language fields in `extraction.json`.
4. Assemble the bilingual EPUB, summary text files, and `report.txt` with `scripts/assemble.py`.

Keep extraction, translation, and assembly responsibilities separate. Extraction must not translate. Assembly must not invent translations. Translation must not alter source fields or structure.

## Inputs

Require an EPUB file and target language. If the user omits the target language, ask for it before processing.

Use an output directory supplied by the user. If none is supplied, create a sibling directory named `output` beside the EPUB.

If the user provides an EPUB path for translation or conversion, create or refresh `extraction.json` from that EPUB before estimating. If the user explicitly provides an `extraction.json` path, estimate and continue from that file instead of re-extracting.

## Dependencies

Before running the scripts, ensure Python 3 is available and install the required parser libraries if they are missing:

```bash
python3 -m pip install beautifulsoup4 lxml
```

The scripts use only Python standard libraries plus `beautifulsoup4` and `lxml`.

## Quick Start

```bash
python3 scripts/extract.py /path/to/input.epub /path/to/output --target-language Chinese
```

Estimate the translation budget before translating:

```bash
python3 scripts/estimate_tokens.py /path/to/output/extraction.json
```

Show the estimate to the user and wait for explicit confirmation. Only after the user confirms, fill `target_language` fields in `/path/to/output/extraction.json`, then run:

```bash
python3 scripts/assemble.py /path/to/output/extraction.json
```

The final outputs are:

- `/path/to/output/bilingual_<input filename>.epub`
- `/path/to/output/summary/*.txt`
- `/path/to/output/report.txt`

## Stage 1: Extract

Run `scripts/extract.py`. It reads EPUB files as zip archives, finds the OPF path via `META-INF/container.xml`, follows OPF spine order, classifies HTML/XHTML pages, extracts article-like pages, copies first images to `summary/`, and writes UTF-8 `extraction.json`.

The extractor supports:

- Magazine/news pages with `ul.calibre_feed_list` and `data-testid="article-title"`.
- Book/chapter pages with headings such as `h1.chapter_title`, `h1.chapter_head`, or content-heavy spine pages.
- TOC-like pages, cover/title/copyright pages, illustration lists, indexes, ads, and miscellaneous pages as non-article pages.

For unfamiliar EPUB sources, inspect the archive before changing logic:

```bash
python3 -c "import zipfile; z=zipfile.ZipFile('/path/to/input.epub'); print('\n'.join(z.namelist()))"
```

If extraction quality is poor, adjust page classification, title extraction, paragraph filtering, TOC detection, or image path handling in `scripts/extract.py` after observing the source structure.

## Stage 2: Estimate Translation Tokens

For every EPUB translation or conversion request, run `scripts/estimate_tokens.py` on `extraction.json` to estimate the translation-stage token budget before translating:

```bash
python3 scripts/estimate_tokens.py /path/to/output/extraction.json
```

When the user provides an EPUB, create or refresh `extraction.json` from the EPUB first. When the user explicitly provides `extraction.json`, use that file directly.

After showing the estimate report, stop and ask the user to confirm before starting translation. Do not begin filling translations until the user explicitly confirms after seeing the estimate. Valid confirmations include short replies such as `继续`, `ok`, `可以`, `确认`, `开始翻译`, `proceed`, or `go ahead`.

The user's initial request to translate or convert an EPUB is not enough to bypass this gate. The confirmation must happen after the concrete estimate report is shown.

If the user only asks for token estimation and does not ask to translate or convert, run extraction if needed, show the estimate, and stop without asking for translation confirmation.

The estimator is a lightweight character heuristic, not a tokenizer-exact counter. It estimates only translation-stage model usage:

- Source paragraph, title, section, and summary-source input tokens.
- Target paragraph, title, section, and summary output token range.
- Prompt/JSON overhead.
- Retry/rework buffer.
- Recommended paragraph batch count using source-character batches.

It does not estimate local EPUB extraction, parsing, or assembly work because those are local scripts. It also does not output cost amounts.

Default estimation behavior:

- Input is `extraction.json`, not the raw EPUB.
- Scope is the full extraction, even if some articles are already translated.
- Batch recommendation uses `--max-source-chars 8000`.
- Retry/rework buffer is `--retry-buffer 0.15`.
- The report includes a total overview and the largest 5 articles by source characters.

Useful options:

```bash
python3 scripts/estimate_tokens.py /path/to/output/extraction.json --max-source-chars 6000 --retry-buffer 0.2 --top 10
```

## Stage 3: Fill Translations

Translation execution policy:

- Default to translating with the current agent/session that invoked this skill.
- For every EPUB translation or conversion request, perform Stage 2 token estimation first and wait for the user's post-estimate confirmation before translating.
- Do not call external translation or LLM APIs, CLI agents, background model runners, or provider SDKs unless the user explicitly asks for that provider/tool or explicitly approves using it.
- Do not infer permission from environment variables, installed CLIs, available credentials, or a large translation workload.
- If the translation is too large for one response, process it in batches within the current session, saving progress after each article or batch.
- If using an API would materially improve speed or reliability, ask before switching execution methods and name the provider/tool that would be used.
- If the user asks to "use current skill" or "directly translate", treat that as permission to use this skill's extraction and assembly scripts, not permission to use third-party translation APIs.

For large EPUBs, prefer a resumable batch workflow instead of trying to translate the whole book in one pass:

1. Generate deterministic translation batches from `extraction.json`.
2. Translate one batch at a time in the current session.
3. Save each batch result separately.
4. Validate batch identity, source hashes, item counts, and non-empty translations before merging.
5. Save progress after each successful batch so interrupted work can resume from the next pending or failed batch.

See `docs/superpowers/specs/2026-05-31-resumable-translation-batches-design.md` for the full testable design.

Read `extraction.json` and fill only these fields for each article:

- `title_dest_language`
- `section_dest_language`
- `translated_paragraphs`
- `summary_dest_language`

Do not modify:

- `num`
- `title`
- `section`
- `href`
- `paragraphs`
- `plain_text`
- `image_filename`

## Translation Quality Pipeline: Faithfulness, Elegance, Readability

Translate in three focused passes instead of trying to satisfy every quality goal at once:

```text
Faithfulness (信) -> Draft A
Elegance (雅) checks and refines Draft A -> Draft B
Readability (达) checks and refines Draft B -> Final translation
```

Keep paragraph count, paragraph order, facts, and meaning unchanged across all passes. If a later pass conflicts with faithfulness, revert to the faithful wording.

### Pass 1: Faithfulness

Translate each source paragraph into Draft A while focusing only on faithfulness:

- Do not omit source information.
- Do not add information absent from the source.
- Do not distort facts, views, logic, or tone.
- Preserve numbers, dates, names, terms, and limiting conditions.
- Preserve causality, contrast, progression, comparison, and other logical relations.
- Keep technical terms, proper nouns, and repeated expressions consistent.
- Do not change the source judgment for the sake of fluency or polish.

After this pass, Draft A should be structurally complete and faithful, even if the wording is not yet polished.

### Pass 2: Elegance

Review Draft A and generate Draft B by improving elegance while preserving faithfulness:

- Keep expression restrained, natural, and rhythmic.
- Do not pile up decorative language.
- Do not over-literarize.
- Do not rewrite beyond the source.
- Match the source genre and tone.
- Keep technical writing accurate and clear.
- Keep journalism objective and fluent.
- Preserve flavor in essays when appropriate.
- Preserve stance and force in opinion writing.

After this pass, Draft B should sound more refined but must not change source meaning, add commentary, or lose details from Draft A.

### Pass 3: Readability

Review Draft B and generate the final translation by improving target-language readability:

- Avoid obvious translationese.
- Follow target-language idiom.
- Keep sentences readable and logic clear.
- Reorder long sentences when needed.
- Make phrasing natural without changing meaning.
- Ensure target-language readers can understand the passage easily.

Only write the final pass into `translated_paragraphs`. Do not expose Draft A or Draft B in `extraction.json`.

Hard constraint:

```text
len(translated_paragraphs) == len(paragraphs)
```

Each `translated_paragraphs[i]` must translate exactly `paragraphs[i]`. Do not merge, split, reorder, omit, add commentary, add notes, or put summaries/titles inside paragraph translations.

Bilingual reading order must always be source language first, target language second. For every paragraph pair, render or preview `paragraphs[i]` before `translated_paragraphs[i]`. For titles and TOC labels, use `{source title} | {target title}`. Do not place target-language content before the corresponding source-language content in bilingual previews or EPUB body content.

Generate `summary_dest_language` from `plain_text` in the target language. Default to 150-300 target-language characters when the article is long; shorter is acceptable for short articles.

After each article, self-check:

- Paragraph counts match.
- No empty translations exist.
- No source information is omitted or invented.
- Logic, tone, names, terms, and section translations are consistent.
- The summary is accurate and separate from paragraph translation.

When only doing the translation stage, output valid JSON only, without Markdown fences or explanation.

## Stage 4: Assemble

Run `scripts/assemble.py` after all translation fields are complete:

```bash
python3 scripts/assemble.py /path/to/output/extraction.json
```

The assembler:

- Rewrites article titles as `{source title} | {target title}`.
- Inserts `<p class="dest_translation">...</p>` after each source paragraph.
- Updates TOC and index link text when source titles/sections can be matched.
- Skips ad pages.
- Preserves covers, images, CSS, fonts, OPF, NCX, and other non-ad resources.
- Injects `.dest_translation` CSS once into HTML/XHTML heads.
- Writes one summary text file per article.
- Writes `report.txt` with EPUB title, paths, target language, article/image counts, missing first images, and untranslated/incomplete articles.

If `assemble.py` reports incomplete translations, fix `extraction.json` instead of changing source fields or bypassing validation.

## Output Contract

`extraction.json` uses this shape:

```json
{
  "epub_title": "...",
  "input_epub": "/abs/path/to/input.epub",
  "output_dir": "/abs/path/to/output",
  "target_language": "Chinese",
  "total_articles": 1,
  "articles": [
    {
      "num": 1,
      "title": "Source Title",
      "section": "Source Section",
      "href": "relative/path/article.xhtml",
      "paragraphs": ["Source paragraph"],
      "plain_text": "Source plain text, max 8000 chars",
      "image_filename": null,
      "title_dest_language": null,
      "section_dest_language": null,
      "translated_paragraphs": null,
      "summary_dest_language": null
    }
  ]
}
```

## Validation

Minimum validation before delivery:

```bash
python3 scripts/extract.py /path/to/input.epub /path/to/output --target-language Chinese
python3 scripts/estimate_tokens.py /path/to/output/extraction.json
python3 -m json.tool /path/to/output/extraction.json >/dev/null
python3 scripts/assemble.py /path/to/output/extraction.json
```

For assembly validation without real translation, use temporary placeholder values only in a disposable copy of `extraction.json`. Do not present placeholder output as a completed translation.
