---
name: biomedical-reference-verifier
version: 1.2.1
description: "Verify or normalize biomedical and life-science reference lists, when the task is about AI-caused reference errors. Checks identifiers and bibliographic fields, preserves source evidence, and produces a searchable offline report. 生物医学/生命科学参考文献真实性验证skill，可以对参考文献列表（引文列表）进行多轮核查和错误修复，附带引文格式整理功能，能统一规范化所有引文为AMA、APA、GB/T 7714等格式。"
metadata:
  openclaw:
    requires:
      bins:
        - python3
    envVars:
      - name: NCBI_API_KEY
        required: false
        description: Optional NCBI API key for higher PubMed E-utilities rate limits.
      - name: OPENALEX_API_KEY
        required: false
        description: Optional OpenAlex API key for authenticated metadata lookups.
---

# Biomedical Reference Verifier

Use this skill only for reference-list authenticity checking, AI-caused reference cleanup, and citation-format normalization. Do not use it to judge whether papers are relevant, suitable, or correctly used in the manuscript body unless the user explicitly asks for reference authenticity plus body cleanup.

## Core Rule

Always reduce the task to this sequence:

1. Build or read `biomedical-reference-verifier.records.v1`.
2. Choose the lightest pipeline.
3. Run the script.
4. Report result files and retained process files.
5. Ask before expensive manual recovery or process-file deletion.

Load `references/verification_policy.md` before classifying authenticity errors, changing severe items, or explaining network/query policy.

## Pipeline Choice

- **Format only**: use when the user only asks to convert or unify citation style. Run `--pipeline format-only`. Do not query Crossref/PubMed/OpenAlex.
- **Verify**: use when the user asks whether references are real, fake, wrong, AI-generated, DOI/PMID-mismatched, or metadata-corrupted. Run the default `verify` pipeline.
- **Verify then format**: use when the user asks both to check authenticity and standardize style. Run `verify` with the requested `--citation-style`; the fixed copy is generated after verification.

## Execution Mode

- **Fast** (`--mode fast`): use for quick scans and large routine lists. Stop after primary DOI evidence when available.
- **Balanced** (`--mode balanced`): default for ordinary authenticity checks. Auxiliary evidence lines receive a short 2.5-second grace period after primary DOI lookup completes (and supplied PMID lookup when enabled).
- **Strict** (`--mode strict`): use for final or pre-submission checks. Wait for every enabled evidence line to complete or fail explicitly.

Do not invent a local confidence score. For DOI-bearing references, resolve the DOI and directly compare returned title, authors, journal, year, DOI, and PMID with source fields. Keep the existing classification policy. Severe items are reported and retained; never auto-delete them.

Do not run AI-assisted per-paper web searching by default. Stop after batch verification and title recovery, then ask the user whether to continue.

## Machine Input

Prefer `biomedical-reference-verifier.records.v1` JSON/JSONL. If the source is free text, convert it to records first using only values present in the user source. Do not fill missing source fields from Crossref, PubMed, OpenAlex, memory, or plausible guesses.

Minimal record:

```json
{
  "schema": "biomedical-reference-verifier.records.v1",
  "records": [
    {
      "index": 1,
      "source": {
        "original_text": "exact source reference",
        "title": "title from source, or empty string",
        "authors": ["First Author"],
        "year": "2024",
        "journal": "Journal from source",
        "identifiers": {"doi": "10.xxxx/example", "pmid": "", "urls": []},
        "source_lines": [12],
        "context": ""
      }
    }
  ]
}
```

Use `--input-mode records` for standardized JSON/JSONL. Use Markdown worksheet and `doi-context` modes only for compatibility.

## Commands

Run from this skill directory:

```bash
python3 scripts/verify_references.py refs.md --output-dir /tmp/reference-audit --citation-style ama
```

Common variants:

```bash
python3 scripts/verify_references.py refs.md --pipeline format-only --citation-style ama
python3 scripts/verify_references.py records.json --input-mode records --citation-style ama
python3 scripts/verify_references.py records.json --input-mode records --mode fast
python3 scripts/verify_references.py records.json --input-mode records --mode strict
python3 scripts/verify_references.py records.json --input-mode records --reuse-results previous/reference-audit.json
python3 scripts/verify_references.py records.json --input-mode records --write-index
python3 scripts/convert_reference_artifact.py previous/reference-audit.json --to index --output reference-index.json
python3 scripts/convert_reference_artifact.py reference-index.json --to audit --output restored-reference-audit.json
python3 scripts/verify_references.py refs.md --pubmed-mode off --openalex-mode off
python3 scripts/verify_references.py refs.md --doi-output append
python3 scripts/verify_references.py refs.md --keep-process-json
python3 scripts/generate_html_report.py previous/reference-audit.json --output reference-audit-report.html
python3 scripts/verify_references.py refs.md --cleanup-process-files all
python3 scripts/verify_references.py refs.md --cleanup-process-files normalized_input,extracted_references
```

## Output Contract

Result files:

- `reference-audit-summary.md`: concise chat-ready summary.
- `reference-audit-detail.md`: detailed report with evidence links.
- `reference-audit-report.html`: self-contained interactive report generated from the fixed template in `assets/reference-audit-report-template.html`.
- `references.auto-fixed.md` or `document.auto-fixed.md`: fixed/formatted copy; never overwrites the source.

The HTML report is a default result file for both verification and format-only runs. Do not regenerate its page structure, CSS, or JavaScript in the task output. The script injects structured report data into the template marker and escapes script-breaking characters. Keep result cards in the input `results` order; never sort them by category, severity, title, or index.

The HTML report uses a compact, white, single-page list. All records, original/output citations, field differences, issues and evidence links are visible without expanding cards or changing pages. Preserve input order. Provide text search, category/status/field filters, reset, copy of filtered results with eligibility warnings, and print. Use small semantic tags rather than large decorative panels. Never equate title similarity with a confidence percentage.

Display groups:
- `correct`: `verified`.
- `auto_fixed`: `minor_fix`, legacy `minor_format_error`.
- `blocked`: identifier-only, metadata conflicts, fabrication, parser errors and unresolved items. Label **不可用**.
- `unchecked`: `formatted_only`; formatting never proves authenticity.

Each result separately records `verification_level`, `usable`, `repair_state`, and `field_differences`. Only verified/strongly matched, safely repaired results from the verification pipeline are eligible. A reference that cannot be verified must not be used. Keep the existing fabrication classifications, but distinguish an unavailable query from evidence that a query actually completed. Never imply that a timeout proves fabrication.

Process-file lifecycle:
- Retain `reference-normalized-records.json`, the source extraction suitable for reuse and parser review.
- Automatically clean newly generated `reference-normalized-input.md` and `references.extracted.md`: both can be rebuilt from the retained records. `--cleanup-process-files none` explicitly retains all generated process files.
- Write `reference-audit.json` only with `--keep-process-json`; write `reference-index.json` only with `--write-index`. These retain reusable evidence and runtime information.
- Remove task-created disposable scratch scripts and redundant previews after validation; never remove maintained skill scripts, user inputs, result files, or prior-run artifacts as generic cleanup.
- After every round, report cleanup and ask which remaining process files to keep. Keep them if the user does not reply. A prior explicit keep/delete instruction takes precedence.

There is no hidden persistent cache. `--reuse-results` accepts either `reference-audit.json` or schema `biomedical-reference-verifier.index.v1`. The converter supports audit-to-index and index-to-audit round trips; the `results` array must remain identical after a round trip. In a conversation, ask about reuse once when such an artifact is available; do not repeatedly ask after the user decides.

User-edited prior artifacts are handled conservatively: malformed JSON is rejected with one concise error; invalid individual rows are skipped and rechecked; valid rows remain reusable. Do not guess repairs for damaged structured fields.

Prior-result reuse requires all stored source fields to agree (including PMID, authors, journal and publication details), current policy version, compatible pipeline/mode/channels, a valid canonical record and a check date within 30 days. Failed, unresolved, incomplete and old artifacts are rechecked. Punctuation-only changes may be normalized. Reuse evidence, then regenerate the output for the requested citation style and DOI settings; never reuse stale formatted text. Temporary network failures receive one bounded retry; permanent 4xx failures do not. PubMed DOI batches split only when a batch fails. Early DOI recovery uses Crossref first, then OpenAlex and PubMed outside Fast mode.

`--write-index` optionally writes `reference-index.json`; it is off by default. Network request events and phase timings are stored in `reference-audit.json` when `--keep-process-json` is used.

Never delete user-requested result files. Delete only process files generated in the current run, according to the lifecycle above or an explicit user selection. Never delete an existing audit merely because this run did not request JSON.

## Closeout

After running:

1. Paste or summarize `reference-audit-summary.md`.
2. Link result files and retained process files.
3. State which process files were cleaned or skipped.
4. Ask whether to delete retained process files:
   - A. delete all retained process files
   - B. keep selected process files
   - C. keep all process files for now
5. If severe items exist, ask whether to continue AI-assisted recovery, delete, keep with warning notes, or stop with the report.
6. Ask whether recovered DOI values should be appended when DOI output is optional.

## Formatting and repair boundaries

Use `formatted_only` for formatting without external queries. A missing or unreliable title leaves the original intact. Never invent an author. Preserve source DOI values; only newly recovered DOI values are subject to the append choice. Preserve volume, issue and page/article numbers in every supported style. The built-in renderer is a plain-text journal-article formatter, not a complete CSL engine: books, datasets and exact publisher typography need a dedicated renderer. Do not promise full style compliance for unsupported document types.

Prefer author objects with `family`/`given`, or explicit `family, given` strings. Preserve surname-first initials and corporate names; retain ambiguous names rather than guessing. Compare authors, title, journal, date and supplied identifiers. Only an explicit provider abbreviation establishes journal equivalence; a different journal is a conflict. A one-year date difference is a reviewable difference unless date evidence explains it. Do not rewrite an identifier-only or partial/conflicting item automatically. Store field-level before/after values and evidence source.

This skill does not require another design skill to maintain its report template.

## Real-list regression boundaries

- Treat an explicit trailing `et al.` as an omitted author suffix. Compare every named author, in order, against the canonical prefix; do not require the abbreviated and complete author lists to have the same length. Preserve real prefix disagreements.
- Commas in a scientific title are not evidence that it is an author list. Only apply the comma heuristic when each segment has author-name syntax.
- Preserve PubMed `CollectiveName` and explicit family/given components. Normalize typographic apostrophes and diacritics for author comparison; do not infer missing initials or compound surnames.
- Treat abbreviated page ranges and repeated electronic page endpoints as equivalent; distinct article numbers remain conflicts.
- If a primary provider returns a recognized placeholder title such as `OUP accepted manuscript`, compare other enabled records for exactly the same DOI. Use a matching title/author/year record and disclose the fallback; do not replace the DOI. A placeholder alone cannot establish hijacking.
- Retain same-identifier journal aliases and explicit publication years from provider evidence. Preserve a valid source year when it matches a known publication year. Save `provider_records` in structured results for reproducible diagnosis.

## Implementation map and review scope

These files implement the advertised workflow; inspect them together rather than inferring missing functionality from one chunk:

| Capability | Implementation | Offline verification |
| --- | --- | --- |
| Input normalization, Crossref/PubMed/OpenAlex lookup and field comparison | `scripts/verify_references.py` | `scripts/test_verification_boundaries.py` |
| Formatting, output safety and query-failure handling | `scripts/verify_references.py` | `scripts/test_release_boundaries.py` |
| HTML payload escaping and report generation | `scripts/generate_html_report.py` | `scripts/self_test_verify_references.py`, `scripts/test_privacy_language.py` |
| Chinese and English report layout and filtering | `assets/reference-audit-report-template.html`, `assets/reference-audit-report-template.en.html` | `scripts/test_privacy_language.py` |
| Evidence reuse and artifact conversion | `scripts/verifier_prior_results.py`, `scripts/convert_reference_artifact.py` | `scripts/self_test_verify_references.py` |

The skill executes local Python, reads the selected reference input, writes reports, and queries the documented bibliographic services. Formatting-only is offline. Verification sends DOI/PMID and, for title recovery, reference titles; it does not need manuscript paragraphs. Tests use subprocess argument lists to exercise local scripts. HTML templates are bundled and have no external script/font dependencies. This implementation map aids inspection; it is not a security certification.

## Contact email and report language

Do not read `USER_EMAIL` or `CLAWDBOT_EMAIL`. No contact email is included by default. Only pass `--email` when the user explicitly wants a contact email sent to the enabled bibliographic providers. The two optional provider API keys retain their existing purpose.

Choose the HTML language from the user's request or conversation language: `--report-language en` for English and `--report-language zh` for Chinese. The CLI default remains Chinese for compatibility. Both templates show the complete report with the same filters, eligibility rules, copy and print functions. Preserve source citations and provider evidence in their original language; selecting English translates the interface and generated eligibility messages, not the cited research.

```bash
python3 scripts/verify_references.py records.json --input-mode records --report-language en
python3 scripts/generate_html_report.py reference-audit.json --output report.en.html --language en
```
