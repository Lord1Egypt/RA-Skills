# Capabilities and public-version limits

Scope: fitctl CLI/core 0.8.0, Python bindings 0.1.1. Marked limits are
properties of these public releases and may change in later ones — check
the installed `--help` / pinned docs before promising more.

## Task -> route map

| Task | Route |
|---|---|
| Static inventory (CPU, memory capacity, storage/mounts, network, accelerators, topology) | CLI `survey --live`; Python `collect_survey()` |
| Current usable resources (allocatable cores/memory, used-excluding-cache, cgroup boundaries) | CLI `state --live`; Python `collect_state()` |
| Path capacity/identity checks | `state --path-check id=path`; Python `path_checks=[...]` (read-only) |
| Link/copy capability probes | explicit `--probe-path-links`/`--probe-path-link-pair`/`probe_links`/`link_pairs` — these WRITE temporary files in the inspected paths; needs authorization for those paths |
| Storage-health observations | opt-in health probe; public 0.8.0 gives limited safe sysfs temperature evidence, NOT full SMART diagnosis |
| Temperatures | CLI `--collect thermal` (built-in providers) or configured providers; Python needs a thermal provider config (see `examples/inputs/thermal-providers.json`) |
| Electrical/cooling sensors (voltage/current/power/fan/energy/humidity) | CLI `--collect hardware-sensors`; Python `hardware_sensors=True` — lm-sensors channels only, non-temperature |
| Reliability counters (memory EDAC; GPU ECC/retired pages/row remapper) | CLI `--collect memory-reliability --collect gpu-reliability`; Python matching bool kwargs |
| CUDA runtime suitability | CLI extension survey + `--collect cuda-runtime`; Python 0.1.1 can load/validate these artifacts but has NO CUDA collection selector |
| Python/Node runtime survey extensions | CLI extension-enabled survey/contract only; no Python 0.1.1 survey-selection API |
| Workload fit decision | CLI `validate`; Python `derive_contract` + `validate` |
| Host x profile matrix + CSV | CLI `classify`; Python `classify_batch()` / `BatchReport.export_csv` |
| Bounded observation window | caller loop over `collect_state`/`state --live` (see `scripts/observe.py`) |
| Explain/share artifacts | CLI `inspect`; Python artifact dict/JSON; `redact` |
| Semantic comparison / signing / trust | CLI `diff`, `sign`, `verify`; Python has semantic hash/bytes but no signing or trust-evaluation API |
| Decision/config bundles, recommendations, adapter exports | experimental CLI commands (`bundle`, `bundle-config`, `recommend`, `export`) |

## Capacity vs availability (the core distinction)

- A survey MAY include static GPU capacity when observable. The line is
  capacity vs current availability — not "surveys never contain GPU memory".
- `allocatable_cpu_logical_cores` is an instantaneous process view
  (includes cgroup limits), not CPU utilisation and not a reservation.
- CUDA `allocatable_memory_bytes` is allocatable-now, not GPU utilisation.
- State values describe the moment of collection; gaps between samples are
  unobserved.

## Public-version limits (do not over-promise)

- No dedicated GPU utilisation/wattage/power-limit collector;
  no Ollama/benchmark hooks; no token-efficiency computation; no deep
  NVMe/SMART health; no automatic power/fan control (fitctl observes and
  validates; it never acts).
- `hardware-sensors` power readings come from exposed lm-sensors channels;
  that is not guaranteed NVIDIA board-power coverage.
- External measurements (benchmarks, workload logs) may be joined to
  timestamped fitctl evidence, but attribute them to their real producer.
- No `fitctl fit` and no generic `fitctl monitor` command: decisions use
  `validate`; monitoring is a caller-controlled loop.
- Python 0.1.1 `collect_survey()` takes no extension arguments; there is
  no `cuda_runtime=True` kwarg, no standalone thermal collector, no
  signing/diff/trust/bundle/recommendation wrapper in Python. Use the CLI
  or load CLI-produced JSON; never invent keyword arguments.
- API limits: artifacts 16 MiB; configs 1 MiB; <=16 extension packs;
  <=128 thermal artifacts per validation; batch <=16 inputs/list and <=64
  pairs; state collection <=16 paths, 16 link pairs, 4 provider configs.
  Calls are synchronous; a Python-side timeout never cancels native work
  (bound collection calls in a killable child process instead).

## Survey vs state vs decision (evidence kinds)

| Kind | Artifact | Says | Never says |
|---|---|---|---|
| Survey | `host-survey.v2` | recorded static facts + collection context | current load, free memory, temperature |
| State | `host-state.v2` | runtime facts at `collected_at` (+opt-in providers) | that values still hold now; safety |
| Decision | `validation-report.v2` | fit verdict vs explicit profile | authorization, reservations |

Missing/unavailable/stale/malformed evidence is distinct from an observed
zero or a healthy result; a successful collection can contain failed
providers — read provider outcomes.
