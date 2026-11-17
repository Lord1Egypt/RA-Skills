# End-to-end pipeline

Use this workflow for complete books where hierarchy, text fidelity, and remote reproducibility matter.

## 1. Establish scope and provenance

Create a manifest with one row per book:

- stable `book_id` and exact title;
- source path, format, size, and checksum;
- expected TOC item count if known;
- target language and writing system;
- destination environment only if upload is explicitly requested.

Keep raw sources immutable. Put extracted page text, OCR output, reviewed corrections, canonical trees, derivative files, audit reports, backups, and remote exports in separate directories.

## Primary executable entry point

Use `scripts/convert_book.py` rather than recreating the pipeline ad hoc:

```bash
python3 scripts/convert_book.py SOURCE.pdf \
  --output-dir output/BOOK_ID-v1 \
  --book-id BOOK_ID \
  --title "Exact printed title"
```

Supported inputs are `.pdf`, `.docx`, and UTF-8 `.txt`. Text PDFs use Poppler layout extraction; weak or forced PDF text layers render at a stable DPI and use page-by-page Tesseract OCR. DOCX preserves paragraph order and explicit/rendered page breaks. TXT recognizes `===== 第 N 页 =====` markers when present.

The entry point writes:

- `{book_id}_tree.json` even when review remains;
- deterministic tree TSV/TXT, per-node TXT, and combined TXT;
- `{book_id}_ocr-review.tsv`;
- `_work/pages/*.txt`, detected TOC, source manifest, and validation log.

Exit codes are contractual: `0` means the complete local bundle passed; `3` means a traceable JSON draft exists but review or validation remains; `2` means extraction/configuration failed. Do not convert exit `3` into success in a wrapper.

For publication use, prefer a visually reviewed printed-TOC manifest:

```bash
python3 scripts/convert_book.py SOURCE.pdf \
  --output-dir output/BOOK_ID-v2 \
  --book-id BOOK_ID \
  --title "Exact printed title" \
  --toc-json reviewed-toc.json \
  --toc-pages 7-9 \
  --review-ledger reviewed-ocr.tsv \
  --reviewer REVIEWER_NAME
```

The TOC JSON is a list, or an object containing `nodes`, `toc`, or `entries`. Each entry requires `title`; provide `level`, `logical_page`, `kind`, and optionally stable `key`/`parent_key`. When omitted, the entry point assigns deterministic keys, inferred levels, and parents.

## 2. Obtain page-aware source text

For a text PDF, run a layout-preserving extractor such as `pdftotext -layout`. For DOCX, preserve paragraph order with a document parser. Normalize encoding to UTF-8 and line endings to LF. Insert unambiguous page markers such as `===== 第 N 页 =====` into the intermediate text only.

For a scanned or broken-text PDF:

1. render pages at a stable resolution;
2. OCR each page independently;
3. retain page numbers and raw OCR output;
4. if both OCR and a text layer exist, compare them page by page and choose or merge using evidence;
5. record low-confidence pages for review.

Never let page markers enter final chapter content.

The executable requires `pdftotext` for PDFs. OCR fallback additionally requires `pdftoppm`, `tesseract`, and the requested language data (default `chi_sim+eng`). Missing OCR dependencies fail explicitly; the tool does not silently fall back to an empty text layer.

## 3. Reconstruct the authoritative TOC

Render the printed TOC pages and transcribe each item into a structured list:

```json
{
  "key": "toc-001",
  "title": "第一章 示例",
  "level": 1,
  "parent_key": null,
  "logical_page": 1,
  "sort": 1
}
```

Record the constant or piecewise mapping from printed page to source-PDF page. Include front matter, appendices, and unnumbered sections when the printed TOC includes them. If a container heading has no body, mark it explicitly instead of silently accepting an empty chapter.

The printed TOC wins over duplicated running headers, noisy OCR headings, and formatting artifacts in the body.

## 4. Locate headings in body text

For each TOC item:

1. predict a source page from `logical_page + page_offset`;
2. search a bounded window around that page;
3. prefer exact normalized ordinal tokens and title text;
4. score remaining candidates by normalized string similarity and layout evidence;
5. select at most one candidate and record `heading_start`, `content_start`, `actual_source_page`, and `heading_score`;
6. fail when the best candidate is below the declared threshold or conflicts with ordering.

Use monotonic ordering as an invariant: a later TOC entry cannot begin before an earlier one. Do not use an unconstrained global fuzzy match.

## 5. Slice and clean content

Set a node's content from its located heading end to the next located heading start. Then apply cleaning in this order:

1. remove page markers and verified running headers/footers;
2. separate page-body text from footnotes before joining pages; preserve each footnote and marker, but do not insert the footnote block into the middle of a sentence continued on the next page;
3. dehyphenate or join page-boundary text only when the sentence is demonstrably unfinished;
4. normalize Unicode and punctuation conservatively;
5. apply reviewed exact or context-bound OCR replacements;
6. preserve paragraph boundaries where the source supplies semantic separation.

Do not assume running headers and footers occupy independent text-layer lines. Layout extraction can merge a header, printed page number, or footnote into the preceding or following body line. Build page-specific header candidates from rendered pages and page geometry, then audit for both standalone and embedded occurrences after cleanup.

For the final TOC node, do not default to end-of-file. Inspect the following rendered pages and record a terminal boundary before colophons, copyright notices, anti-piracy statements, advertisements, answer sheets, covers, or other material excluded by the authoritative TOC. Include such material only when it is intentionally modeled as its own node.

Keep an auditable correction table with old text, new text, book, context, reason, and reviewer status. Broad global character replacement is prohibited unless every occurrence has the same meaning in context.

Language models or masked-language models may rank suspicious rare characters, but their output is a review queue, not an edit instruction.

The final OCR review ledger must be a UTF-8 TSV with these columns:

```text
candidate_id	book_id	node_key	original	suggestion	context	decision	reviewer
```

`candidate_id` must be stable and unique. `decision` is exactly `corrected`, `accepted`, or `false_positive`; blank, pending, or machine-only decisions block completion. For `corrected`, both original and replacement text are required and the original candidate must no longer remain in that node. A header-only ledger is valid only when the recorded audit produced no candidates.

## 6. Canonical JSON contract

The canonical per-book JSON should contain:

```json
{
  "book_id": "stable-book-id",
  "title": "书名",
  "authority": "printed_toc",
  "node_count": 1,
  "nodes": [
    {
      "key": "toc-001",
      "title": "出版说明",
      "level": 1,
      "parent_key": null,
      "sort": 1,
      "logical_page": null,
      "source_page": 1,
      "heading_start": 0,
      "content_start": 4,
      "content_end": 100,
      "heading_score": 1.0,
      "structural_only": false,
      "content": "……",
      "content_chars": 96,
      "source_file": "source.txt"
    }
  ]
}
```

Additional metadata is allowed, but `book_id`, `title`, `nodes`, node keys, parent references, levels, order, titles, and bodies must remain deterministic.

Every displayed field in this contract is required on every node. Use JSON `null` for an unavailable `logical_page` or `source_page`; do not omit the key. `structural_only` is always a JSON boolean. Record a declared minimum heading score for the run and manually resolve every node below it before release.

## 7. Derivative bundle

Generate every derivative from the canonical JSON in one run:

- `{prefix}_tree.json` — authoritative structured edition;
- `{prefix}_tree.tsv` — spreadsheet-friendly audit view;
- `{prefix}_tree.txt` — readable hierarchy preview;
- `{prefix}_chapters/*.txt` — one file per node;
- `{prefix}_all-content.txt` — complete ordered text;
- corpus-level audit reports and optional archive/checksum manifest.

Do not hand-edit derivative files. Correct the source or canonical tree, then regenerate.

Use the bundled deterministic builder after the final canonical edit:

```bash
python3 scripts/build_derivatives.py CANONICAL_JSON_DIR \
  --output-dir VERSIONED_BUNDLE_DIR --replace
```

The builder replaces only its known derivative targets. Point it at a reviewed, versioned output directory; do not use a broad workspace root.

## 8. Quality gates

### Structural

- JSON parses and `node_count == len(nodes)`.
- Keys are unique; each parent exists; no node parents itself; no cycles exist.
- Roots have the intended level; child levels agree with their parent relationship.
- Sort order is deterministic and matches the printed TOC.
- Located headings are monotonic and expected item counts match.

### Content

- Every required content node is nonempty.
- `content_chars` matches the actual content length under the selected normalization.
- Boundary inspection shows no content lost or duplicated between adjacent nodes.
- No page marker, running header/footer, or next-chapter heading leaks into content.
- Sample every page-boundary form and verify that a continued body sentence is not interrupted by a footnote block; audit standalone and embedded running-header forms separately.

### Encoding and OCR

- UTF-8 decode succeeds.
- No unexplained U+FFFD, mojibake, private-use glyphs, or control characters.
- Repeated spaces between CJK characters and suspicious symbol runs are reported.
- Report line-leading `O`, `0`, `○`, or similar glyphs before CJK text when the rendered page shows a bullet; normalize only after visual confirmation. Report spaces before CJK punctuation and ASCII punctuation embedded between CJK characters.
- Report mixed letter-digit runs such as `I960`, `10S`, or `7L5`, stray decorative glyph fallbacks such as `@`, duplicated punctuation, and citation markers that appear inside a broken sentence.
- Rare-character and language-model findings are reviewed; they are never auto-accepted solely by score.

### Cross-artifact

- The ordered titles and bodies in chapter TXT and combined TXT are generated from and traceable to JSON.
- Rebuilding the bundle twice from identical inputs produces identical normalized JSON fingerprints.
- No derivative may predate or disagree with the final canonical JSON. Matching file counts are insufficient.

Run the bundled fail-closed validator before upload or delivery:

```bash
python3 scripts/validate_bundle.py CANONICAL_JSON_DIR \
  --artifact-dir VERSIONED_BUNDLE_DIR \
  --ocr-review REVIEWED_OCR_LEDGER.tsv \
  --require-ocr-review \
  --min-heading-score 0.80 \
  --fail-on-warnings
```

Choose the heading threshold from the extraction plan rather than silently lowering it to pass. If the validator reports a likely OCR pattern, add it to the review ledger with the emitted `candidate_id`, inspect the source, record the disposition, and rerun. Do not waive errors or replace a failed validation with an importer-only schema check.

## 9. Safe remote upload

Uploading replaces remote state and is a separate, explicitly authorized phase.

1. Resolve and display the exact base URL, environment name, equipment/library ID, book IDs, and book count.
2. Export a full backup including chapter bodies, metadata, hierarchy, and identifiers.
3. Save backup path and checksum before deletion or replacement.
4. Validate all local trees before the first mutation.
5. Freeze the validator output and per-book fingerprints. Import only those exact selected files in parent-ready batches. Use low bounded concurrency; prefer one worker for a problematic or previously mismatched book.
6. Preserve stable book IDs. A title match is not sufficient identity.
7. After the upload finishes, create a new export of book metadata, full chapter bodies, levels, sort values, and parent IDs. Record target, equipment/library ID, export time, and book set. Never reuse a pre-upload snapshot as read-back evidence.
8. Compare the remote export with local JSON using `scripts/compare_tree_export.py`.

Pass tokens through standard input or an environment variable. Never echo, persist, or include a token in command history, generated reports, Skill files, or the final response.

Stop before upload if the target is uncertain, backup fails, authorization is absent, validation fails, or remote identity cannot be resolved.

After read-back, run the validator again with `--remote-export POST_UPLOAD_EXPORT.json`. A remote mismatch invalidates acceptance even when titles, book counts, or chapter counts look plausible.

## 10. Acceptance report

Report:

- exact canonical version directory and source manifest;
- books, nodes, and content-character totals;
- all failed or waived checks;
- reviewed correction and audit report paths;
- remote target and backup path, if applicable;
- read-back comparison result and one SHA-256 fingerprint per book;
- any intentionally empty structural nodes or unresolved source defects.
