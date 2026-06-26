# Foreground Path Optimization

Goal: minimize user-visible turn time while preserving async playback behavior.

## Primary rule
Keep foreground work limited to enqueue + immediate acknowledgement.

## Common foreground delays
- Heavy health/status probes (`systemctl show`, full queue introspection)
- Verbose benchmark output and extra shell process startup
- Synchronous waits for queue drain or playback completion
- Extra post-processing not required for the immediate reply

## Recommended mitigations
1. Default benchmark mode to `--status none --output compact`.
2. Run deep status probes only on demand (`--status both --output full`).
3. Separate "quick ack" from "detailed analysis" into two turns when needed.
4. Avoid per-item logging in foreground unless actively debugging.
5. Keep producer scripts append-only and lock-light.

## Operational pattern
- Fast path (default): enqueue, brief text reply.
- Slow path (debug): explicit diagnostics command + structured breakdown.

## Acceptance checks
- Typical benchmark turn should complete in roughly 1-2s when status probes are disabled.
- Enqueue path should remain sub-100ms on local host under light load.
- Playback must continue asynchronously in worker after reply is sent.
