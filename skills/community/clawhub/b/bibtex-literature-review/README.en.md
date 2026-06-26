# BibTeX Literature Review

> English companion document. 中文主文档: [README.md](README.md)

`bibtex-literature-review` is a Codex / AI coding agent skill for producing Word `.docx` literature reviews from structured reference sources. It focuses on real Word cross-reference behavior: body citations are Word `REF` fields, citation markers are superscript numeric markers, and the bibliography uses real Word automatic numbered paragraphs.

The recommended workflow is **Zotero + Better BibTeX + Codex**.

## What It Does

- Normalizes references from `.bib`, `.ris`, CSL JSON, CSV/TSV, or preformatted reference lists.
- Produces bibliography text in GB/T 7714, APA, MLA, Chicago, IEEE, Vancouver, or Harvard-like formats.
- Builds `.docx` files with clickable Word `REF` citations instead of plain text or `HYPERLINK` fields.
- Displays citations as superscript numeric markers such as `[1]`, `[3-5]`, and `[10,11]`.
- Uses Word automatic numbering for bibliography paragraphs.
- Adds `_RefBibNNN` bookmarks so body citations can jump to bibliography entries.
- Validates the DOCX OOXML structure with a command-line checker.
- Filters unused references when converting Markdown drafts to review JSON.

## Recommended Workflow: Zotero + BibTeX + Codex

1. Curate references in Zotero.
2. Complete metadata fields such as author, title, journal, year, volume, issue, pages, DOI, and URL.
3. Export references with Zotero Better BibTeX as `.bib`.
4. Ask Codex to use this skill with your topic, target language, length, citation style, and output path.
5. Let Codex normalize references, select relevant sources, draft the review, build DOCX, and validate Word fields.
6. Manually review final bibliography punctuation, capitalization, proper nouns, and institutional formatting requirements.

Example prompt for Codex:

```text
Use the bibtex-literature-review skill.
The source file is /path/to/refs.bib, exported from Zotero Better BibTeX.
Write a Chinese literature review of about 3000 words on "{your thesis title}".
Use GB/T 7714 bibliography formatting and superscript numeric body citations.
Generate a Word DOCX and validate REF fields, automatic numbering, and superscript citations.
```

If strict bibliography punctuation matters more than metadata parsing, export a preformatted bibliography from Zotero in the required style and provide it as a plain `.txt` or `.md` reference list. This skill can still handle review drafting, citation selection, Word REF generation, and DOCX validation.

## Supported Inputs

- `.bib` / `.bibtex`: recommended; use Zotero Better BibTeX when possible.
- `.ris`: Zotero, EndNote, Web of Science, CNKI, and other database exports.
- `.json` / `.csljson`: CSL JSON.
- `.csv` / `.tsv`: Zotero, EndNote, or spreadsheet-style exports.
- `.txt` / `.md`: preformatted reference lists.

Markdown citation markers:

```markdown
Single citation[cite:1].
Collapsed range[cite:3-5].
Citation group[cite:10,11].
Citation by key[@liu2025].
Multiple keys[@liu2025; @zhang2024].
```

Markdown conversion filters unused references by default:

```bash
python scripts/markdown_review_to_json.py draft.md --refs candidates.json --out review.json
```

Keep unused bibliography entries only when explicitly needed:

```bash
python scripts/markdown_review_to_json.py draft.md --refs candidates.json --out review.json --keep-unused
```

## Basic Usage

Normalize references:

```bash
python scripts/sources_to_json.py refs.bib --style gbt7714 --out candidates.json
```

Choose another bibliography style:

```bash
python scripts/sources_to_json.py refs.bib --style apa --out candidates_apa.json
python scripts/sources_to_json.py refs.bib --style ieee --out candidates_ieee.json
```

Build DOCX from review JSON:

```bash
python scripts/build_docx_from_review_json.py review.json --out output.docx
```

Validate DOCX cross-references:

```bash
python scripts/validate_docx_crossrefs.py output.docx \
  --expect-bib-count 12 \
  --forbid-hyperlinks \
  --require-ref \
  --require-superscript \
  --require-auto-numbered-bib
```

## Review JSON Contract

The DOCX builder consumes structured JSON:

```json
{
  "title": "Mock Literature Review",
  "references": [
    {
      "gbt": "Zhang San. Theoretical foundations and development trends of a mock research topic[J]. Journal of Mock Studies, 2025, 12(3): 45-56."
    },
    {
      "gbt": "Li Ming. Mock evidence on organizational practice and technology adoption[J]. Journal of Example Studies, 2024, 8(2): 101-118."
    }
  ],
  "paragraphs": [
    [
      "Existing studies suggest that the mock research topic can be analyzed through theoretical foundations, practical mechanisms, and contextual factors",
      {"cite": 1},
      ", while organizational practice and technology adoption provide additional empirical context",
      {"cite": 2},
      "."
    ]
  ]
}
```

Citation values:

- `{"cite": 1}` -> `[1]`
- `{"cite": [3, 4, 5]}` -> `[3-5]`
- `{"cite": [10, 11], "collapse": false}` -> `[10,11]`

See [references/review-json-spec.md](references/review-json-spec.md) for the full schema.

## Citation Style Notes

This skill separates two layers:

- Body citation mechanism: numeric Word `REF` fields by default.
- Bibliography formatting: GB/T 7714, APA, MLA, Chicago, IEEE, Vancouver, Harvard, etc.

APA, MLA, and some Chicago variants normally use author-date or author-page in-text citations. If clickable Word `REF` behavior is required, this skill keeps numeric REF citations and applies those styles only to bibliography text.

IEEE, Vancouver, and GB/T 7714 fit the default numeric workflow better.

The bundled formatter is a deterministic baseline, not a full CSL engine. For publication-grade references, prefer Zotero/CSL formatted output or manually review:

- capitalization,
- author names and particles,
- journal title style,
- italics required by the style guide,
- DOI/URL formatting,
- edition, translator, access date, and publisher fields.

Detailed style rules: [references/citation-styles.md](references/citation-styles.md).

## Usage Rules

Do:

- Use Zotero or another reference manager to keep metadata clean.
- Prefer Better BibTeX `.bib` exports.
- Tell Codex the topic, language, target length, citation style, and output path.
- Cite only references that support the actual review argument.
- Run structural DOCX validation before delivery.
- Manually review strict style requirements when needed.

Do not:

- Deliver plain typed `[1]` citations as if they were Word cross-references.
- Use `HYPERLINK` fields as a substitute for Word `REF` fields.
- Keep uncited references in the final bibliography unless explicitly requested.
- Invent missing DOI, pages, volume, issue, publisher, or publication place.
- Perform external metadata lookup unless the user asks for it.
- Modify sample Word files unless the user explicitly requests it.

## Scripts

- [scripts/sources_to_json.py](scripts/sources_to_json.py): normalize literature sources into candidate JSON.
- [scripts/bibtex_to_json.py](scripts/bibtex_to_json.py): lightweight BibTeX-only parser for common Zotero/Better BibTeX exports.
- [scripts/markdown_review_to_json.py](scripts/markdown_review_to_json.py): convert Markdown drafts with `[cite:1]` or `[@key]` markers into review JSON.
- [scripts/build_docx_from_review_json.py](scripts/build_docx_from_review_json.py): build the final `.docx`.
- [scripts/validate_docx_crossrefs.py](scripts/validate_docx_crossrefs.py): validate REF fields, superscript results, bookmarks, hyperlinks, and bibliography numbering.
- [scripts/self_check.py](scripts/self_check.py): isolated end-to-end regression check.

## Self-Check

Run with a real BibTeX fixture:

```bash
python scripts/self_check.py --bib /path/to/refs.bib
```

The self-check validates:

- package hygiene,
- script syntax,
- BibTeX normalization,
- DOCX generation,
- Word `REF` fields,
- automatic bibliography numbering,
- bookmark anchors,
- superscript citation results,
- absence of hyperlink-based citation markup.

## Scope and Limits

Good fit:

- Chinese thesis-style literature reviews.
- Word documents that require clickable cross-references.
- Zotero-managed references combined with Codex-assisted drafting.
- Numeric citation workflows such as GB/T 7714, IEEE, and Vancouver.

Not a direct substitute for:

- a full CSL processor,
- Zotero or EndNote,
- institution-specific Word templates,
- publication-grade APA/MLA/Chicago output without manual review,
- a complete BibTeX engine for complex macros and arbitrary LaTeX commands.

## More Documentation

- Main Chinese README: [README.md](README.md)
- Workflow: [references/workflow.md](references/workflow.md)
- Input formats: [references/input-formats.md](references/input-formats.md)
- Citation styles: [references/citation-styles.md](references/citation-styles.md)
- GB/T 7714: [references/gbt7714-bibtex.md](references/gbt7714-bibtex.md)
- Review JSON: [references/review-json-spec.md](references/review-json-spec.md)
- Word REF / OOXML: [references/ooxml-ref-fields.md](references/ooxml-ref-fields.md)
- Acceptance criteria: [references/acceptance.md](references/acceptance.md)

## License

MIT License. See [LICENSE](LICENSE).
