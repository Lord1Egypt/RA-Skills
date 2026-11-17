---
name: cloudarc-bounded-memory-benchmark
version: 1.4.2
description: "Make CloudArc large-package performance reproducible, measurable and safe to ship. Drives the bounded-memory workflow for the .vibo container - streaming pack/unpack inside a fixed RSS ceiling, high-cardinality multi-file archives with SHA-256 dedup, remote-search range telemetry and the CI/manual gates that guard them. Use when changing benchmarks, SLOs, manifest or index cardinality, remote metadata reads or GitHub Actions checks, or when reviewing a large-package MVP before real cloud providers are switched on."
tools: [python]
license: MIT-0
metadata:
  hermes:
    tags: [benchmark, compression, memory, cloudarc, ci]
    version: 1.4.2
---

# CloudArc Bounded-Memory Benchmark

> main: run `scripts/cloudarc_benchmark.py` (from the skill directory; subcommands: `doctor`, `selfcheck`, `smoke`, `manual`, `check-telemetry`, `badge`; without a subcommand it prints usage and exits 2)

**Release:** `1.4.2` (2026-09-12)

Use this skill to make large-package performance work reproducible, measurable,
and safe to run once a real cloud provider (Yandex Disk via an OAuth token) is enabled. Keep the portable
reference backend authoritative; a native ViBo semantic executor is now accepted on
any CPython that has a matching build, because the adapter probes a real import and
the `cloudarc.native-semantic-v1` capability instead of gating on 3.11.

## Workflow

### 1. Inspect the repository

Read the current implementations before editing:

- `benchmarks/large_package.py` and `benchmarks/resource_monitor.py`;
- `core/packer.py`, `core/format.py`, `core/index.py`;
- `cloudarc.py`, `cloud/protocol.py`, and provider adapters;
- `tests/test_benchmark.py`, `tests/test_cli.py`, and protocol tests;
- `docs/LARGE_PACKAGE_SLO.md` and `docs/REMOTE_SEARCH_PROTOCOL.md`.

Perform a defect-first review. Preserve unrelated user changes. Do not edit
source materials in Downloads, and do not connect credentials, cloud services,
or proprietary ViBo packages.

### 2. Preserve the single-file SLO

Run the existing payload-scaling profile with a fresh child process for each
operation. Keep these limits unchanged unless the user explicitly approves a
new contract:

- peak RSS: `<= 256 MiB` for pack and unpack;
  (streaming payloads only - the lexical index is built in memory, so a text-heavy
  tree is measured differently: 64.1 MiB / 358 files = 169 MiB with the index and
  29.7 MiB with `pack --no-index`. Report both when a tree is text-heavy.);
- 1/5/10 GiB peak-RSS spread: `<= 64 MiB`;
- pack staging: `<= 2.10 * payload + 64 MiB`;
- unpack staging: `<= 1.10 * payload + 64 MiB`.

Use `--sizes-mib 32` or `64` for normal CI. Keep 1/5/10 GiB runs out of the
default unit-test path.

```powershell
python -B -m unittest discover -s tests -v
python -B -m benchmarks.large_package `
  --sizes-mib 64 `
  --json-output benchmarks/results/ci-smoke.json `
  --markdown-output docs/LARGE_PACKAGE_BENCHMARK_CI.md `
  --fail-on-slo
```

For a large acceptance run, use `--sizes-gib 1 5 10`, atomic JSON/Markdown
checkpoints, and `--resume` only when the workload fingerprint, settings,
environment, and SLO match exactly.

### 3. Add or extend the multi-file profile

Use a deterministic directory generator that writes one file at a time.
Expose bounded parameters for:

- file count;
- file size;
- duplicate-group count;
- nested path cardinality;
- text/searchability.

Run `pack(..., dedup=True)` and `unpack(...)` in isolated workers. Record at
least:

- raw bytes, file count, unique entries, duplicate entries, dedup ratio;
- manifest entry count;
- lexical index document and term/posting counts;
- pack/unpack peak RSS;
- sampled staging bytes and operation-derived temporary-disk floor;
- restored file count and bytes.

Do not silently apply the single-file O(1) claim to arbitrary metadata
cardinality. Use a separate profile and explicit bounds. The reference
multi-file gate is:

- pack/unpack peak RSS `<= 512 MiB`;
- manifest entries `<= 10,000`;
- lexical documents `<= 10,000`;
- temporary disk measured and reported for each operation.

Run a small case in tests (for example 24 files) and a 512-file CI smoke. Put
larger cardinalities in the manual workflow.

### 4. Instrument remote search

Instrument the actual metadata path, not a mock:

1. Create a small recorder object with bounded integer counters.
2. Record every successful `read_range` response and its returned byte length.
3. Record every sidecar `read_bytes` response and its returned byte length.
4. Sample current/peak RSS and retain the source string.
5. Attach telemetry additively to `list`, `info`, and `search` responses.

The stable response field is:

```json
{
  "telemetry": {
    "range_requests": 3,
    "range_bytes": 12345,
    "sidecar_reads": 0,
    "sidecar_bytes": 0,
    "peak_rss_bytes": 25165824,
    "rss_source": "linux-proc-status",
    "mode_used": "lexical",
    "data_section_read": false
  }
}
```

Embedded metadata normally makes exactly three range reads: fixed header,
manifest, and index. Unsupported range APIs may fall back to two validated
sidecar reads. A provider error must not be converted into fallback. The data
section must never be read by remote metadata/search operations.

Keep protocol compatibility additive: version 1.0/1.1 readers must continue
to parse responses, lexical fallback remains explicit, and no secrets or full
provider credentials may enter telemetry.

### 5. Add CI gates

Maintain two separate workflows:

- `.github/workflows/ci.yml`: push/PR unit tests plus small bounded-memory and
  multi-file smoke profiles;
- `.github/workflows/large-package-benchmark.yml`: `workflow_dispatch` only,
  defaulting to 1/5/10 GiB and a configurable high-cardinality run, with
  uploaded JSON/Markdown artifacts.

The manual workflow must have a generous timeout and must not require cloud
credentials. Never make 10 GiB data generation a normal PR gate.

The bundled helper provides the same safe entry points without shell-specific
glue:

```powershell
python -B skills/cloudarc-bounded-memory-benchmark/scripts/cloudarc_benchmark.py `
  smoke --repo .
python -B skills/cloudarc-bounded-memory-benchmark/scripts/cloudarc_benchmark.py `
  manual --repo . --yes
python -B skills/cloudarc-bounded-memory-benchmark/scripts/cloudarc_benchmark.py `
  check-telemetry --input remote-response.json --expected range
```

`manual` requires `--yes` because it can consume hours and tens of GiB of
temporary disk. `check-telemetry` accepts a response object containing
`telemetry` or a telemetry object directly, and returns non-zero on invariant
violations. Both benchmark commands also verify that JSON reports a passing
evaluation, that the multi-file manifest covers every file (one entry per file
plus one entry per directory - the check uses the reported `kinds`) while
the search index holds exactly the files, and that the paired Markdown report
exists and contains `PASS`.

### 6. Update contracts and verify

Update the SLO and remote protocol documents whenever measurements or response
fields change. Keep machine-readable results and Markdown generated from the
same result object.

Run:

```powershell
python -B -m unittest discover -s tests -v
python -B -m compileall -q core cloud stats benchmarks tests cloudarc.py config.py
Get-ChildItem -Recurse -Directory -Filter __pycache__ | Remove-Item -Recurse -Force
Get-ChildItem $env:TEMP -Directory -Filter 'cloudarc-large-benchmark-*'
```

Confirm that the final JSON reports `evaluation.pass == true`, no benchmark
temporary directories remain, and all final documents/workflows are present.
Register user-facing artifacts after verification. Do not create a git commit
unless explicitly requested.

## Failure handling

- Treat missing, truncated, or invalid worker JSON as a failed run.
- Treat incomplete requested sizes as `in_progress` or `failed`, never as pass.
- Reject resume checkpoints when settings, workload fingerprint, environment,
  or SLO differ.
- Fail closed on malformed manifest/index or inconsistent archive IDs.
- Keep provider errors visible; only `NotImplementedError` may trigger sidecar
  fallback.
- If RSS measurement is unavailable, report the source and fail the relevant
  acceptance gate rather than inventing a value.
- If disk preflight fails, preserve the checkpoint and report the exact
  required/free byte counts.

## References

Read [references/contract.md](references/contract.md) when implementing or
reviewing the detailed SLO, telemetry, resume, and CI contracts. Read
[references/release-notes.md](references/release-notes.md) when handing the
skill to another team or upgrading from an earlier package.

## Skipped files and the index flag

`pack` returns `skipped`, `skipped_count` and `skipped_by_reason`, and `analyze`
returns `skipped` plus `skipped_summary: {count, by_reason}` (reasons:
`protected` / `system` / `special` / `symlink-target` / `changed` / `vanished`);
the CLI warns on stderr. Never treat a pack as complete without checking that count: protected
subtrees (`.git`, `__pycache__`, `.venv`), leading system paths (without
`--allow-system`) and special files are skipped by design.

A symlink inside a tree is stored as a `symlink` entry (the target string is the
payload) and recreated on unpack, and every entry carries `mode` and `mtime_ns`,
so a restore rebuilds permissions, timestamps, empty directories and links.
Version history lives in `references/release-notes.md`. Check the result from the repository
root with `python3 scripts/verify_restore.py <archive.vibo> <original-root>
<restored-root>`: it compares kind, content hash, mode and mtime per entry,
prints `verdict: OK` and exits 0, or exits 1 with the list of mismatches.

`pack --no-index` (also on `push`) skips lexical index construction for
memory-bounded runs on text-heavy trees; the manifest records
`search.index_built = false` and `search` returns nothing. The archive payload
and restore path are unchanged.
