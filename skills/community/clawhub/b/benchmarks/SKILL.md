---
name: benchmarks
description: "Benchmark storage routing for agent memory/benchmark stacks: use when running BEAM-style evaluations, locomo benchmarks, calibration probes, or any benchmark that produces .db run databases. Tells you exactly what goes where — run databases OUTSIDE the repo, scripts and result JSONs in the repo. Now includes the run-resilience ladder: how long benchmark runs survive provider flaps. Load before creating any benchmark .db file or setting an output path."
---

# Benchmarks Skill — Storage Routing Constitution
**Version:** 1.1

## When to load this skill
- Running a benchmark evaluation (`*_eval_*.mjs`)
- Running a locomo/long-memory benchmark
- Running a calibration probe
- Creating or referencing any `.db` benchmark database
- Setting up a new benchmark or evaluation framework
- Asking "where do I put benchmark output?"
- **Debugging a failed/stalled benchmark run, or making long LLM-driven runs survive provider flaps (see § Run resilience)**

## The Golden Rule

> **Code and scores live in the repo (git). Run databases live outside the repo (scratch).**

## What goes WHERE

### ✅ Stays in `<repo>/benchmarks/` → tracked in git
| What | Examples |
|---|---|
| Evaluator scripts | `beam_eval_v*.mjs`, `locomo_eval_*.mjs` |
| Result summary JSONs | `beam_results_v17.2_100K.json` |
| Analysis + diff scripts | `diff_results.mjs`, `generate_comparison_report.mjs` |
| Dataset/fixtures | `beam_data/`, `fixtures/` |
| Download scripts | `download_beam.py`, `download_locomo.py` |
| Reports and logs | `EVAL-REPORT.md`, `run-logs/` |

**Rule:** if it's a text file that a human wrote or that summarises a result, it belongs here.

### ❌ Goes in a scratch root outside the repo (e.g. `~/.openclaw-benchmarks/`) → NOT in git
| What | Destination subfolder | Examples |
|---|---|---|
| Run databases | `beam/` | `beam_bench_v17.2.db` |
| Locomo run databases | `locomo/` | `locomo_bench_v10.db` |
| Calibration run databases | `calib/` | `calib_bench.db` |
| Test / scratch databases | `scratch/` | `test_full.db` |
| Dev workspace forks | `beam-workspace/` | full repo forks used for benchmarking |
| Version snapshots | `beam-snapshots/` | versioned snapshot dirs |

**Rule:** if it ends in `.db` or is a full repo fork used for benchmarking, it goes here.

## How to write to the right place
In benchmark scripts, always pass `--output` explicitly (defaults: `<scratch>/beam|locomo|calib`).
CLI: `node benchmarks/beam_eval_vX.mjs --output <scratch>/beam/beam_bench_vX.db`.
Naming: `<type>_bench_v<version>[_<variant>].db`. Add a `.gitignore` backstop (`**/*.db`) so a mis-routed run database never enters git even by accident.

## Why this split matters
- **git bloat prevention:** one `.db` dir is 15–175 MB binary — one accidental commit costs MB in pack history forever.
- **backup hygiene:** repo backups capture code and results, not multi-GB scratch databases.
- **reproducibility:** run databases are reproducible from scripts + data. Result summaries are not.

## Enforcement reminders
- About to write a `.db` inside the repo? Stop; reroute to the scratch root.
- Benchmark script lacking `--output` or hardcoding a repo path? Fix it in that session.
- New benchmark type? Create a new subfolder under the scratch root + add a row to the table above.

---

## § Run resilience — long LLM-driven runs that survive provider flaps

> Multi-hour benchmark/ingestion runs **must survive transient provider failures by design.** Before this pattern shipped (2026-07-29), a transient GLM/OpenRouter flap killed the whole run and re-ingested from zero (~5h worst case). The ladder below eliminated that class of loss — and was **proven organically the day it shipped**, when a real 60+ minute provider outage hit mid-run and the run survived while the pre-ladder version had died 3× in the same flap.

**The ladder (implement it in your shared LLM client so every caller inherits it):**
1. **Retry hardening** — transient errors AND empty-content responses retry: ≥8 attempts, exponential backoff + jitter, ~5-min cap. (Empty provider responses used to burn one retry then FAIL the work unit.)
2. **Flap circuit** — ≥5 consecutive transient failures in a 2-min window ⇒ **park-and-probe** (60s→300s probes, ≤30 min) ⇒ if still down, **RESUMABLE abort** (distinct exit code, checkpoint intact — never a dead run that can't continue).
3. **Checkpoint/resume** — persist per-work-unit progress (e.g. a manifest table inside the run's own database, atomic with the run DB's lifecycle — a sidecar file can desync and skip work into an empty DB). Rerun the same command to resume; completed units are skipped; partial units are wiped and redone cleanly.
4. **Data-quality gate** — every run reports failed work-unit counts; `>0` ⇒ the run is **FLAGGED, not publication-grade**. Silent data thinning must never pass silently.

**⚠️ Probe false-negative trap:** reasoning-on models (e.g. GLM thinking variants) burn tiny `max_tokens` on reasoning and return HTTP 200 with **empty content** (`finish_reason: length`) — a tiny-token connectivity probe misreads a HEALTHY endpoint as down. Probes must use `reasoning: {exclude: true}` + a small-but-real budget. Distinguish failure shapes: `finish_reason: "error"` = provider failure (retry/circuit); `finish_reason: "length"` = budget truncation (raise budget / drop reasoning).

**Operating knobs (example envs):** retry max attempts / base backoff ms / cap ms; circuit window + park budget; `KEEP_DB=1` to skip end-of-run wipes so post-run audits (duplicate-rate audits, tag verification) can inspect the kept run database. Test-only failure-injection hooks should print a loud DO-NOT-SCORE banner when armed.

**Design notes that matter:**
- Put the primitives in the *shared* client module with an **opt-in wrapper** — keep the public call surface byte-identical so existing callers are unaffected.
- A checkpoint that trusts partial state is worse than none: verify every manifest row against actual DB state at startup; stale rows get dropped, unverifiable partials get wiped and redone.
- Version your harness; a checkpoint from a different harness version should trigger a clean rebuild, not a resume.
