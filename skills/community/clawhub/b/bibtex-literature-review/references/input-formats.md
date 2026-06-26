# Supported Input Formats

Use this file when the user provides literature sources or review drafts in formats other than BibTeX.

## Literature Source Formats

Normalize sources with:

```bash
python scripts/sources_to_json.py source-file --out candidates.json
```

Supported formats:

- `.bib`, `.bibtex`: BibTeX.
- `.ris`: RIS exports from Zotero, EndNote, Web of Science, CNKI tools, and many databases.
- `.json`, `.csljson`: CSL JSON, including Zotero Better BibTeX / citeproc-style exports.
- `.csv`: Zotero/EndNote/Excel-style CSV with recognizable columns.
- `.tsv`: tab-separated exports.
- `.txt`, `.md`: plain preformatted reference lists, one reference per paragraph or numbered line.

## Zotero Export Recommendation

For reliable metadata, ask users to export from Zotero when possible:

- Preferred structured export: **Better BibTeX `.bib`** with stable citation keys.
- Preferred style-aware export: **CSL JSON** when the downstream formatter or institution uses CSL.
- Preferred preformatted export: Zotero bibliography copied/exported in the required style, then supplied as `.txt` or `.md` plain references when exact punctuation is more important than metadata parsing.

The bundled BibTeX parser handles common Zotero/Better BibTeX exports, but it is intentionally lightweight. It is not a full BibTeX engine for complex macros, `@string` expansion, custom LaTeX commands, or all title-protection edge cases. If parsing looks suspicious, re-export from Zotero as CSL JSON or provide a Zotero-formatted plain reference list.

Use `--format` when extension inference is ambiguous:

```bash
python scripts/sources_to_json.py refs.txt --format plain --out candidates.json
```

Use `--contains` to quickly filter:

```bash
python scripts/sources_to_json.py refs.ris --contains 激励 --contains satisfaction --out candidates.json
```

Use `--style` to choose bibliography formatting:

```bash
python scripts/sources_to_json.py refs.bib --style apa --out candidates_apa.json
python scripts/sources_to_json.py refs.csv --style ieee --out candidates_ieee.json
```

## CSV / TSV Column Names

The normalizer recognizes common variants:

- key: `key`, `citekey`, `citation key`, `id`.
- type: `type`, `item type`, `entrytype`.
- author: `author`, `authors`, `creator`, `creators`.
- title: `title`, `publication title`.
- journal: `journal`, `publication`, `publication title`, `journal title`.
- year: `year`, `date`, `publication year`.
- volume, issue/number, pages, publisher, place/address, DOI, URL, abstract.

After conversion, inspect `candidates.json`; automatic field mapping is a starting point, not a substitute for human judgment on final reference selection.

## Markdown Review Drafts

When a user has already written a draft in Markdown, convert it to review JSON with:

```bash
python scripts/markdown_review_to_json.py draft.md --refs selected_refs.json --out review.json --title 文献综述
```

Supported citation markers:

- `[cite:1]` or `[1]`
- `[cite:3-5]`
- `[cite:10,11]`
- `[@citekey]`
- `[@citekey1; @citekey2]`

The converter resolves citation keys against `key`, `id`, `citation-key`, or `anchor` fields in the selected references JSON.

By default, the converter keeps only references that are cited in the Markdown draft and renumbers them by first citation order. Multi-reference citation groups are displayed in ascending new-number order. This enforces the "bibliography contains only actually cited sources" requirement.

Use `--keep-unused` only when the user explicitly wants to retain uncited bibliography entries:

```bash
python scripts/markdown_review_to_json.py draft.md --refs candidates.json --out review.json --keep-unused
```

## Recommended Multi-Format Flow

1. Convert source file to candidates JSON.
2. Select the references that support the review argument. If converting a Markdown draft, let the converter filter and reorder by first citation order.
3. Draft review directly as JSON or write Markdown with citation markers.
4. Convert Markdown to review JSON if needed.
5. Build DOCX.
6. Validate REF fields and bibliography numbering.
