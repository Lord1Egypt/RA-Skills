# Context Pipeline v1 (retrieval + compression)

Portable spec for agents:

1) Always include `always_on.md`.
2) Route message → task_type using `router.yml`.
3) Retrieve snippets from memory according to router policy; build Retrieval Bundle JSON.
4) Compress Retrieval Bundle → Context Pack JSON using `compressor_prompt.txt`.
5) Lint Context Pack; if it fails, fall back to raw snippets.
6) Feed Always-on policy + Context Pack (+ optional raw snippets) + user message to the reasoning model.
7) For `debug` and `audit`, persist runtime artifacts according to `RUNTIME_ARTIFACTS.md`.
8) Emit evidence according to runtime mode: compact summary in `normal`, full artifacts in `debug`, full artifacts plus Receipt Ledger in `audit`.

Files:
- `always_on.md` — tiny always-on policy + topic catalog (template).
- `router.yml` — deterministic task router + retrieval caps.
- `compressor_prompt.txt` — prompt for cheap compressor model.
- `schemas/retrieval_bundle.schema.json` — JSON Schema for retrieval bundle.
- `schemas/context_pack.schema.json` — JSON Schema for context pack.
- `schemas/receipt_ledger.schema.json` — JSON Schema for audit-mode receipt ledger.
- `RUNTIME_ARTIFACTS.md` — run folder and artifact naming contract for debug/audit.
- `tests/golden.json` — starter/example file retained for orientation and validator sanity checks.
- `tests/harness_cases.json` — authoritative deterministic positive-path fixtures for routing, snippet IDs, caps, compression/lint fallback behavior, artifacts, transcript evidence, and router overlap coverage.
- `tests/anti_fabrication_cases.json` — authoritative deterministic negative-path fixtures for missing artifacts, forged claims, bad receipt hashes, and missing receipt steps.

Regression stance:
- Use the executable harness fixtures as the source of truth for behavior correctness.
- Keep `golden.json` only as a lightweight starter example, not as the primary proof surface for correctness.

Version: v1.0
