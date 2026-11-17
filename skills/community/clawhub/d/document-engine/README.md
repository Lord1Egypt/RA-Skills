# Document Compliance Audit Engine · Document Engine

A deterministic compliance audit engine for Chinese business documents. Pure Python standard library, zero third-party dependencies, fully offline.

## Features

- **Clause-level rule scan**: 14 built-in rules covering generic wording standards, contract risk clauses and compliance red lines (minimum wage / penalty cap / unpaid overtime), regulation duty & permission boundaries, and official-document format standards. Keyword rules report **every occurrence** (no per-rule cap), and each finding carries its character offset for clause-level attribution.
- **Document-level audit**: element completeness (6 contract / 6 regulation / 4 official-doc elements), same-assignment contradiction detection, contract rights-duty balance detection, official-document document-number and date checks
- **Responsibility anchoring**: every report binds a named responsibility node and a fully traceable audit log
- **Three report formats**: HTML (self-contained single file, shareable) / JSON (system integration) / Markdown (archival)

## Quick start

```bash
python3 scripts/document_engine.py audit --type contract --input contract.txt --output report.html
python3 scripts/document_engine.py demo --output-dir ./out
```

Document types: `contract`, `regulation`, `official_doc`, `generic`.

## Verdict policy

- A hit is a verdict; no probability estimates
- Scoring: WARNING −5 / CRITICAL −15 / FATAL −30 (100 max, floored at 0)
- Pass condition: score ≥ 60 **and** no FATAL / CRITICAL findings

## What's new in v1.1.0 (2026-11-06)

- **Every occurrence reported** — keyword rules no longer stop at the first hit per keyword, and the temporary per-rule cap has been removed (a clause repeated 300 times yields 300 findings).
- **Offset-based clause attribution** — each finding carries its character `offset`; findings are attached to the owning clause by binary search over node boundaries (snippet fallback retained).
- **Regex pattern lists** — a regex rule may declare several `patterns`, merged by position.
- **Rules widened** — `COM-001` now also flags `及时`; `CT-003` also matches bare percentages such as `50%`.
- **Exit codes** — `0` success, `2` missing input file, `1` any other error.

## Custom rules

Point `--rules-dir` at a directory of JSON rule files; format in [references/RuleCatalog.md](references/RuleCatalog.md).

## License

MIT
