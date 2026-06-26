# Production Workflow

Use this file when executing an end-to-end BibTeX-to-Word literature review task.

## 1. Gather Inputs

Confirm or infer:

- Literature source file path: `.bib`, `.ris`, `.json`/CSL JSON, `.csv`, `.tsv`, `.txt`, `.md`, or curated JSON.
- Sample `.doc` or `.docx` path, if the user wants style matching.
- Topic and scope, such as "ZS 公司员工激励策略优化研究".
- Approximate length, language, and output path.
- Citation style: default to sequential numeric citations unless the user states otherwise.
- Bibliography style: default to `gbt7714` for Chinese thesis tasks; use `apa`, `mla`, `chicago`, `ieee`, `vancouver`, or `harvard` when requested.

Do not modify the sample document unless explicitly asked.

## 2. Normalize Literature Sources

Prefer the bundled source normalizer for non-DOCX source files:

```bash
python scripts/sources_to_json.py input.bib --out candidates.json
python scripts/sources_to_json.py input.ris --out candidates.json
python scripts/sources_to_json.py input.csv --out candidates.json
```

Add a style when requested:

```bash
python scripts/sources_to_json.py input.bib --style apa --out candidates.json
```

For BibTeX specifically, the legacy helper is also available:

```bash
python scripts/bibtex_to_json.py input.bib --out candidates.json
```

Use `--contains` for quick narrowing:

```bash
python scripts/bibtex_to_json.py input.bib --contains 激励 --contains satisfaction --out candidates.json
```

When the user controls the source manager, recommend Zotero export:

- Better BibTeX `.bib` for stable citation keys and common metadata.
- CSL JSON when style-aware downstream processing matters.
- Plain preformatted Zotero bibliography when exact institution-required punctuation is more important than metadata parsing.

The bundled BibTeX parser is tuned for common Zotero/Better BibTeX exports. It is not a full BibTeX engine for complex macros, `@string` expansion, or arbitrary LaTeX commands.

For Markdown review drafts after reference selection:

```bash
python scripts/markdown_review_to_json.py draft.md --refs selected_refs.json --out review.json
```

The Markdown converter filters unused references and renumbers by first citation order by default. Multi-reference citation groups are displayed in ascending new-number order. Use `--keep-unused` only when the user explicitly wants uncited bibliography entries retained.

Read `input-formats.md` when using RIS, CSL JSON, CSV/TSV, plain references, or Markdown drafts.

Extract at least:

- entry type.
- citation key.
- author or editor.
- title.
- journal / booktitle / publisher.
- year.
- volume, number, pages, DOI, URL when present.

Reject or quarantine malformed entries instead of silently mixing fields between entries.

## 3. Select References

Choose references that support the actual review argument. For management thesis literature reviews, common clusters are:

- digital transformation and HRM.
- employee satisfaction and work experience.
- compensation, performance, equity incentive, and differentiated incentives.
- two-factor theory, expectancy theory, motivation, and innovation incentives.
- turnover, training, career development, and digital tools.

Use only selected references in the final bibliography.

## 4. Draft the Review

Draft in paragraphs with citations represented as structured placeholders. Do not type citation numbers as plain text in the prose.

Preferred paragraph rhythm for Chinese thesis reports:

- background and digital transformation.
- core employee motivation variables.
- incentive tools and HR mechanisms.
- broader theory and digital/intelligent context.
- research gaps and the focal company value.

Keep claims tied to the cited sources. Avoid overclaiming beyond metadata when the full text was not read.

## 5. Convert References

Convert selected entries to the requested bibliography style. Preserve available metadata and do not invent missing fields.

See `gbt7714-bibtex.md` for GB/T details and `citation-styles.md` for APA/MLA/Chicago/IEEE/Vancouver/Harvard.

## 6. Build DOCX

Create a review JSON file and run:

```bash
python scripts/build_docx_from_review_json.py review.json --out output.docx
```

The builder should create:

- body citation `REF` fields.
- superscript citation display.
- internal `_RefBibNNN` bookmarks.
- bibliography paragraphs with real Word automatic numbering.

## 7. Validate

Run:

```bash
python scripts/validate_docx_crossrefs.py output.docx --forbid-hyperlinks --require-ref --require-superscript --require-auto-numbered-bib
```

Then unzip or inspect XML when debugging. Useful patterns:

```bash
unzip -q output.docx -d /tmp/docx_check
rg 'REF _RefBib' /tmp/docx_check/word/document.xml
rg '<w:hyperlink' /tmp/docx_check/word/document.xml
rg '<w:numPr>' /tmp/docx_check/word/document.xml
```

## 8. Render and Inspect

First run structural code validation. Then render when a renderer is available.

Use the Documents skill renderer when available:

```bash
env TMPDIR=/private/tmp python render_docx.py output.docx --output_dir render --emit_pdf
```

Open page PNGs at full size. Check:

- citations appear where expected.
- no `[[1]]` double brackets.
- ranges like `[3-5]` and comma groups like `[10,11]` display correctly.
- bibliography numbering is visible and aligned.
- no field-code text leaks into the page.

If the active AI environment supports multimodal image inspection, inspect the rendered PNG pages directly and report that visual validation passed. If no renderer or multimodal image inspection is available, rely on the code-level OOXML validation and state that visual PNG inspection could not be performed.

## 9. Deliver

Return only the final `.docx` unless the user asks for intermediate artifacts. Briefly state the structural checks that passed.
