# Live state, sensors, and bounded monitoring

These procedures target CLI 0.8.0 and Python 0.1.1/core 0.8.0.
Provider availability differs per host —
read provider outcomes; a successful call can contain failed providers.

## Live state (current usable resources)

```bash
"$FITCTL_PY" - <<'PY'
from pathlib import Path
import fitctl
state = fitctl.collect_state(path_checks=[{"path_id": "workspace", "path": str(Path.cwd())}])
Path("reports/host.state.json").write_text(state.to_json(), encoding="utf-8")
print(state.to_dict()["state"]["core_state"]["resources"])
PY
```

CLI equivalent: `fitctl state --live --path-check "workspace=$PWD"`.
`core_state.resources` is the process's current view (cgroup/namespace
limited) — allocatable, not free-or-stays-free, and not utilisation.
Expected schema `host-state.v2`, `collection_mode: live`. Timestamps:
the collection timestamp is `envelope.provenance.collected_at`; state
freshness is `core_state.freshness.observed_at` + `freshness_state`.
(The envelope itself has no `collected_at` key — look at `provenance`.)
`path_resources`
adds mount/device identity, filesystem type and available bytes per named
path. `boundaries` records cgroup limits (`memory_limit_bytes`,
`cpu_quota_logical_cores`, ...).

## Temperatures and sensors

Python 0.1.1 needs an explicit thermal provider config; a ready two-
provider config (lm-sensors + nvidia-smi, both `current_host`/
`local_process`) is packaged at
`examples/inputs/thermal-providers.json`. Extend or restrict it per host;
provider kinds and command shapes are from the public docs.

```bash
"$FITCTL_PY" - <<'PY'
from pathlib import Path
import fitctl
state = fitctl.collect_state(
    thermal_provider_config_paths=["<skill-dir>/examples/inputs/thermal-providers.json"],
    hardware_sensors=True)
Path("reports/sensors.state.json").write_text(state.to_json(), encoding="utf-8")
core = state.to_dict()["state"]["core_state"]
for p in core["thermal_resources"]["providers"]:
    print(p["provider_id"], p["outcome"])
for r in core["thermal_resources"]["readings"]:
    print(r["sensor_id"], r["temperature_millidegrees_celsius"]/1000, "C", r["status"])
PY
```

- Temperatures are millidegrees Celsius; statuses `ok|warning|critical`
  are the provider's own assessment.
- `hardware_sensors=True` is NON-temperature only (the section is
  `core_state.hardware_sensor_resources`): quantities carry scaled units
  (microvolts, microamperes, microwatts, millirevolutions/minute,
  microjoules, millipercent). Do not map channel labels to specific
  components; `flags`/`limits` come with `value_state` and quantity.
- Reliability: `memory_reliability=True, gpu_reliability=True`
  (CLI: `--collect memory-reliability --collect gpu-reliability`). These
  are counters/observations only — fitctl never enables ECC or changes
  persistence/power. Consumers may legitimately report `partial` with a
  provider diagnostic (e.g. EDAC present but no controllers).
- CLI-only: built-in thermal selection without a config
  (`fitctl state --live --collect thermal`), and standalone
  `fitctl thermal collect` / `thermal profile init` (target-bound
  evidence; the generated threshold is observed+margin, NOT a
  manufacturer limit — review before gating).
- Missing tools/devices/access must stay visible as provider failures.
  Never run sensors-detect or driver changes just to get a green result.

## Bounded monitoring with scripts/observe.py

`scripts/observe.py` is the reusable caller-side loop. Each sample runs
`collect_state` in a separate child process (own session) with a hard
per-sample timeout; an overall deadline caps the window; SIGTERM/timeout
kills the whole child group. Manifest preservation on handled
interruption is best-effort (it is written at finalization, not
atomically per sample). It never
overlaps samples and never installs or changes anything.

```bash
"$FITCTL_PY" <skill-dir>/scripts/observe.py \
  --samples 3 --interval 2 --duration 30 --timeout 12 \
  --thermal-config <skill-dir>/examples/inputs/thermal-providers.json \
  --hardware-sensors --out reports/monitor-run-1
```

Output: `<out>/sample-NNNN.state.json` (full artifacts) +
`<out>/manifest.json` with per-sample start/end/elapsed/status
(`collected|error|timeout|interrupted|skipped` — `skipped` means the
overall deadline prevented the sample from starting) and per-sensor
`sampled_temperature_ranges` (unit degrees_celsius, min/max/mean,
valid_sample_count, partial/warning/critical counts). Exit 0 = every
requested sample collected — not "all providers succeeded" and not
"temperatures are safe". Read manifest provider outcomes and per-sensor
counts before interpreting a range. The helper warns on stderr at launch
when `duration` cannot fit `samples` at `interval` (the last sample would
start at/after the deadline) — prefer adjusting `--samples` or
`--duration` over accepting a truncated window.

Interpretation rules:
- Compare `valid_sample_count` against attempted samples; a gap is a gap,
  never a low temperature. No fabricated range for missing sensors.
- Never forward-fill old values as fresh.
- Sampled extrema bound only the sampled instants — they do not prove
  nothing overheated between readings, and are not a safety guarantee.
- Reporting a user-supplied threshold crossing is fine; automatic
  shutdown/kill/fan/power actions require a separate, explicitly
  configured deterministic watchdog.

Per-sample timeout terminates and reaps the owned child and records
`timeout`; the overall
deadline stops a slow loop and still writes the manifest.
