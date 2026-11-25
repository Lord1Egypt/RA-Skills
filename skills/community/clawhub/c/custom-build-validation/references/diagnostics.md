# Optional fixture diagnostics

Start with OCM/OpenClaw logs, health, timing and Crabbox's native capture/results.
Record the exact baseline/candidate revisions with each capture. Use matching
conditions for comparisons; label measurements made under different load.

When traces or metrics are needed, offer the release workflow's local OTLP
pattern: diagnostics-otel only in the disposable fixture, a task-owned local
collector, content capture off, file exporters, bounded rotation. Explain the
additional plugin/container and storage before enabling it; reuse an approval
that already covers this optional capture. No personal installation changes.

## Prepare

1. Verify the installed OCM, OpenClaw and collector command/configuration
   contracts from their versions. Select the official compatible diagnostics
   plugin and collector image, record exact version/digest and check relevant
   advisories. Do not carry the release skill's old image pin forward blindly.
2. Use a private task-owned telemetry directory. Docker must already be usable
   or its installation must be in the authorized scope. Otherwise report capture
   unavailable and continue with native diagnostics.
3. Configure three file exporters for traces, metrics and logs, each with an
   8 MiB rotation limit and one backup. Bind the collector's published OTLP HTTP
   port to loopback with an unused port. Verify the actual binding. Inside an
   isolated container the receiver may listen on all interfaces; the host
   publish must remain loopback-only. Configure no remote exporters or headers.
4. Mount configuration read-only and only the telemetry directory writable.
   Use a read-only container root, dropped capabilities, no-new-privileges,
   bounded process count and temporary filesystem, as supported by the selected
   image. Run with permissions sufficient only to write the telemetry files.
5. Install/inspect/enable the compatible official diagnostics plugin through the
   selected OCM fixture. Replace its OTLP configuration rather than merging old
   endpoints: loopback collector URL, http/protobuf, traces/metrics/logs enabled,
   logsExporter otlp, captureContent false, flushIntervalMs 1000. Verify current
   schema before setting these values. Validate, restart through OCM, then prove
   fixture health and that expected signals arrive locally.

Configuration alone is not capture proof. If binding, compatibility or signal
checks fail, disable the fixture exporter, stop the collector and report the
diagnostic failure separately. Keep the validation result independent.

## Crabbox

Read `openclaw-crabbox` before remote capture. Prefer its native timing, results
and artifact collection. If OTLP is necessary, keep the collector within the
approved remote environment and collect only scoped diagnostic artifacts.
Remote does not authorize forwarding a personal home, credentials or content.
Record provider/run identity privately; a local container is not remote proof.

## Closeout and public evidence

Stop fixture emission, allow a bounded flush, stop the task-owned collector,
restore the fixture's pre-capture plugin/config state if retained, and verify
the resulting state. Restore any personal source service changed with approval.
Retain captures privately or remove only within the approved cleanup scope.

Treat logs and traces as potentially secret-bearing even with captureContent
false. Public comments may contain a small aggregate count, latency statistic,
known operation name or low-cardinality error category that supports a recorded
observation. Exclude raw telemetry, request/session IDs, environment names,
hostnames, local paths, prompts, responses, tool payloads and credentials.
Human privacy review covers both visible prose and hidden JSON.
