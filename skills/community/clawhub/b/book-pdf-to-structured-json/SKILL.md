---
name: book-pdf-to-structured-json
description: Convert whole-book PDF, scanned PDF, DOCX, or TXT sources into a publication-grade hierarchical electronic edition with authoritative printed-TOC reconstruction, reviewed OCR cleanup, per-chapter TXT, combined TXT, structured JSON/TSV, deterministic validation, safe API upload, backup, and full read-back verification. Use when extracting or rebuilding complete books for a knowledge base; not for casual single-page OCR.
license: MIT-0
---

# Book PDF to Structured JSON

Produce a traceable electronic edition whose hierarchy comes from the printed table of contents and whose remote copy can be proven identical to the reviewed local JSON.

## Read the right reference

- Read [references/pipeline.md](references/pipeline.md) before planning or executing a book conversion.
- Use [scripts/convert_book.py](scripts/convert_book.py) as the primary one-book entry point. It extracts PDF/DOCX/TXT sources, falls back to page OCR for weak PDF text layers, reconstructs or imports the printed TOC, locates headings, writes canonical JSON, creates an OCR review ledger, rebuilds derivatives, and runs strict validation.
- After every canonical JSON change, run [scripts/build_derivatives.py](scripts/build_derivatives.py) to rebuild the complete derivative bundle. Never preserve older TXT/TSV files beside newer JSON.
- Before describing a local bundle as final, run [scripts/validate_bundle.py](scripts/validate_bundle.py) with the artifact directory, reviewed OCR ledger, declared heading threshold, and fail-on-warning mode.
- Use [scripts/compare_tree_export.py](scripts/compare_tree_export.py) after a full remote export. It compares titles, bodies, levels, order, and parent relationships and emits reproducible SHA-256 fingerprints.

## Core rules

1. Treat the rendered printed TOC as the structural authority. Do not infer the final tree only from OCR body headings.
2. Preserve source evidence: page boundaries, source-page mapping, heading-match score, and the original extracted text.
3. Separate detection from correction. OCR models and rare-character audits propose candidates; only reviewed, context-safe rules may change text.
4. Make the JSON tree the authoritative deliverable. Generate TXT, TSV, chapter files, and upload payloads from that same tree.
5. Keep the canonical schema explicit and uniform. Every node must contain every contract field, including nullable `logical_page`/`source_page` and boolean `structural_only`; absence is not equivalent to `null` or `false`.
6. Treat an OCR candidate report as unfinished until every row records a decision and reviewer. A clean encoding scan or “zero abnormal symbols” is not semantic OCR proof.
7. Fail closed on uncertain headings, missing parents, duplicate keys, cycles, unexpected node counts, empty content-bearing nodes, unresolved OCR candidates, stale derivatives, or unexplained text loss.
8. Never mutate a remote environment until the user has authorized upload and the exact environment, equipment/library ID, and book set are known.
9. Export a full remote backup before replacement. Pass credentials through environment variables or standard input; never place tokens in commands, reports, or logs.
10. Freeze and fingerprint the exact local JSON immediately before upload. After upload, create a new full remote export and compare it with that frozen version. An older export, matching counts, or matching titles is not acceptance evidence.

## One-command behavior

Run one source through the complete local pipeline with:

```bash
python3 scripts/convert_book.py SOURCE \
  --output-dir VERSIONED_OUTPUT_DIR \
  --book-id STABLE_BOOK_ID \
  --title EXACT_TITLE
```

The command always writes a canonical JSON draft when extraction and TOC reconstruction succeed. It exits `0` only for a validated final bundle, `3` when JSON was produced but TOC/OCR review remains, and `2` for extraction or configuration failure. A reviewed `--toc-json` and `--review-ledger` can be supplied on the same entry point; reviewed corrections are applied to the named node before derivatives and validation are rebuilt.

Automatic TOC parsing is a draft path unless `--accept-auto-toc --reviewer NAME` records a completed printed-page review. Scanned-PDF OCR remains a draft unless `--accept-ocr --reviewer NAME` records rendered-page review. Never describe an exit-3 JSON as publication-grade final.

## Access and authorization

- Read only the source books and extraction evidence the user placed in scope.
- Write only to the approved local output and audit locations.
- Use network access only when the user explicitly requests upload or remote read-back verification.
- Do not create background jobs, persistence, credential stores, or privilege changes.

## Execution outline

1. Inventory sources, select a versioned output directory, and invoke `convert_book.py` for each text PDF, scanned PDF, DOCX, or TXT source.
2. Let the entry point extract page-aware UTF-8 text and use OCR only where the PDF text layer is absent or demonstrably worse; inspect its retained `_work/pages` evidence for review.
3. Render and transcribe the printed TOC, including hierarchy, printed page number, and expected item count.
4. Locate every TOC heading near its expected source page; record score and offsets, and stop for ambiguous matches.
5. Slice content between adjacent located headings and clean only layout artifacts and reviewed OCR errors.
6. Build the canonical tree with the complete schema, then run structural validation.
7. Generate a semantic OCR candidate ledger, review every candidate against source evidence, and record `corrected`, `accepted`, or `false_positive` plus reviewer identity.
8. Rebuild every derivative in one run from the reviewed JSON, then run strict cross-artifact validation. Any later JSON edit invalidates the derivatives and this validation.
9. If upload is requested, freeze the validated fingerprints, back up the target, import only those exact files, create a post-upload full export, and run the deterministic comparator.
10. Report the exact local version directory, book/node totals, audit results, backup path, remote target, and per-book fingerprints.

## Completion standard

Do not call the work complete unless:

- every printed TOC entry maps to exactly one node in the intended order;
- every parent exists and the hierarchy is acyclic and level-consistent;
- every required book and node field is present with the declared type; nullable values are explicit;
- expected content-bearing nodes are nonempty;
- no unexplained replacement characters, mojibake, private-use glyphs, page headers, or page markers remain;
- every OCR/rare-character candidate has a source-reviewed disposition, and corrected source strings no longer remain in the referenced node;
- running headers are removed even when the PDF text layer merges them into an adjacent body line, and footnotes do not interrupt or reorder a sentence continued on the next page;
- the final included node ends at a reviewed terminal boundary rather than blindly consuming the PDF tail;
- JSON parses, strict validation exits zero, and every derivative byte sequence is regenerated from that exact JSON version;
- the remote full export was created after the upload and matches the frozen reviewed local fingerprints when an upload occurred.
