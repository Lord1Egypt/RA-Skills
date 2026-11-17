# Errors & Troubleshooting (agent-facing)

Companion to the `## Errors` section of SKILL.md. Full error table preserved here.

| Error | Cause | Fix |
|---|---|---|
| `urllib.error.URLError` / timeout | No network / proxy | Confirm `api.fda.gov` reachable; configure proxy |
| HTTP 429 / rate-limited | Exceeded openFDA quota. **Official limits:** anonymous **240 req/min, 1,000 req/day (per IP)**; free API key **240 req/min, 120,000 req/day (per key)**. Rate-limited by **request count, not row count**; FAERS single-request `limit` max = 100 rows | Add `--api-key` (raises to 120k/day); or lower frequency. `fetch_reports.py` sleeps 0.5s/page + HARD_CAP 10000 (=100 requests) — only 10% of anonymous daily cap, safe |
| `--drug` given, `--event` omitted | Intent = top adverse events of a drug, not a pair signal | **No longer errors**: auto-degrades to "top-N adverse-event report" (no 2×2). Add `--event <MedDRA PT>` to compute a signal |
| Field-name mismatch | Wrong drug-name field | Default `patient.drug.medicinalproduct`; standardize via `--field patient.drug.openfda.substance_name` |
| CN-PV: HTTP 412 / WAF | nmpa.gov.cn blocked by CDN/WAF | Expected — only cdr-adr.org.cn is scraped; NMPA intentionally excluded |
| CN-PV: 0 hits | Keyword too specific / only latest page sampled | Pass `--drug-cn` (Chinese name) + `--event-cn`; raise `--cn-max` (sampling only, not full archive) |
| FAERS multi-word event **persistent** 404 `NOT_FOUND` | That three-word PT is not accepted by openFDA (e.g. `RENAL FAILURE ACUTE`), not transient jitter | `total()` has built-in "404 → `.exact` downgrade"; still 404 → swap to standard MedDRA PT (`ACUTE KIDNEY INJURY`, not `RENAL FAILURE ACUTE`); two-word PTs (e.g. `HEPATIC FAILURE`) usually work |
| Case download `--max > 10000` | Trying to exceed free quota cap | HARD_CAP=10000; auto-clamped to 10000 with a warning. Downloaded = **first N in API-return order (not random sample)** — mind selection bias in stats |

## Diagnostic / regression harnesses

> **Maintainer-only (not shipped).** The suites below live in the local `tests/`
> directory, which is **not tracked by git and not shipped to any publish target**
> (GitHub / ClawHub / SkillHub) per ct-base §16.8. Installed packages contain no
> test code; these paths are documented for maintainers running from a local
> checkout. Both suites are stdlib-only (no pytest) and run offline by default, so
> they never consume openFDA quota unless a case explicitly goes live.

- `tests/mode_b_test.py` — broad hardening suite (ct-update methodology §11.1),
  10 cases across difficulty tiers:
  - **Simple (1–3):** happy path for all four methods (strong signal / no signal /
    EBGM standalone).
  - **Middle (4–6):** boundary & abnormal inputs (continuity correction /
    structural zero `a==0` / negative-count clamping).
  - **Complex (7–10):** cross-function coupling (signal_score tiering / Naranjo
    causality / MedDRA coding) and a live end-to-end run (`--validate-controls`
    against openFDA positive & negative controls).
  - `python tests/mode_b_test.py` — case 10 needs openFDA reachability; its failure
    does not block the offline cases.

- `tests/mode_c_test.py` — deep per-branch suite (F1–F11), one simple + one complex
  case per functional branch: `compute` four methods; EBGM shrinkage (incl. `a==0`);
  signal_score composite + T1–T4 tiering; Naranjo causality (incl. reverse polarity);
  verbatim→PT coding; multi-source aggregation; drug-name resolution
  (exact / fuzzy / non-ASCII); PT→SOC mapping; top-events degradation with no
  `--event`; export rendering (HTML / XLSX must not crash); main-flow input parsing
  (`--no-resolve-drug-name` / `--code-verbatim`).
  - `python tests/mode_c_test.py`

- Contract checks asserted by both suites (regression guards for previously-fixed
  bugs): a zero co-occurrence must **not** fabricate a signal; negative cells must
  **not** crash; score ∈ [0,100]; tier ∈ {T1–T4}; `map_soc` correctness.
