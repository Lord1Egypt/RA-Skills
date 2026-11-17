# CloudArc Benchmark Contract

## Profiles

### Payload scaling

The payload profile is deterministic and streamed in 1 MiB writes. Each pack
and unpack operation runs in a new child process. The parent samples RSS and
logical staging directories; the worker reports an OS high-water mark. The
recorded peak is the maximum of parent and worker observations.

Required result fields:

```text
status
size_bytes
profile
pack.peak_rss_bytes
pack.peak_temp_bytes
pack.slo
unpack.peak_rss_bytes
unpack.peak_temp_bytes
unpack.slo
```

### Multi-file cardinality

The directory generator must be deterministic and stream each file separately.
Use `dedup=True` to exercise chunk/hash reuse. The profile is accepted only
when its cardinality is visible in the result:

```text
file_count
raw_bytes
duplicate_groups
dedup_entries
unique_entries
dedup_ratio
manifest_entry_count
index_document_count
index_term_count
```

The reference limits are 512 MiB RSS, 10,000 manifest entries, and 10,000
lexical documents. These are bounded-profile limits, not guarantees for
unbounded manifests.

## Remote telemetry semantics

Count returned bytes, not requested lengths. Count a request only after the
provider returns a byte string/bytearray successfully. For an embedded archive:

```text
range_requests = 3
sidecar_reads = 0
data_section_read = false
```

For a provider that raises `NotImplementedError` for range reads:

```text
range_requests = 0
sidecar_reads = 2
data_section_read = false
```

Do not catch or reinterpret other provider exceptions. `peak_rss_bytes` must
be a positive measurement when the platform reader is available; otherwise
return an explicit unavailable source and fail the acceptance check.

## Checkpoint/resume rules

Checkpoint JSON must preserve:

- schema and completion status;
- requested sizes and profile;
- sample interval and timeout;
- workload fingerprint;
- SLO values;
- completed operation measurements.

Resume only if all of those values match exactly. Recompute each operation's
SLO result before accepting a checkpoint.

## CI policy

The PR workflow runs unit tests and small smoke cases only. The manual workflow
owns 1/5/10 GiB and larger cardinality. Upload JSON and Markdown outputs so a
failed run remains inspectable. No workflow may require cloud credentials or
activate the native ViBo backend.

## Helper entry points

The bundled `scripts/cloudarc_benchmark.py` uses `subprocess.run` with argument
lists and never invokes a shell. Its commands are:

- `smoke`: unit tests, a small payload benchmark, and a small multi-file
  benchmark;
- `manual`: explicit large payload and high-cardinality runs, gated by
  `--yes`;
- `check-telemetry`: JSON-only validation of range/sidecar counters, RSS
  fields, and the `data_section_read=false` invariant;
- `doctor`: environment and repository readiness without running a benchmark;
- `selfcheck`: the smallest self-contained proof - a small pack/unpack with real
  RSS numbers against the 256 MiB SLO;
- `badge`: render the flat SVG SLO badge from a previous result artifact.
