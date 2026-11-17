---
name: ble
description: Use BLEA to diagnose and automate local Bluetooth Low Energy devices. Trigger for BLE adapter or permission problems, nearby-device scans, deterministic device selection, GATT discovery and reads, bounded notification observation, read-only JSONL evidence capture, offline semantic comparison or replay of BLE captures, adapter-free CI tests, guarded request/notification exchanges, guarded writes, repeatable BLE YAML workflows, and raw-byte evidence collection through the `ble` CLI or BLEA MCP tools.
---

# BLEA

Use BLEA for local BLE work. Prefer BLEA MCP tools when available; otherwise run the equivalent
`ble` CLI command with JSON output.

## Environment boundary

First determine whether the current Agent host has BLEA MCP tools or the `ble` runtime and native
Bluetooth access. A hosted Agent cannot access the Bluetooth adapter on the user's computer merely
because this Skill is installed. In that environment, analyze uploaded `.blea.jsonl` evidence,
explain or prepare commands for a local host, and clearly label them as not executed. Do not claim a
scan, connection, read, notification, or write occurred without the corresponding structured
result.

When uploaded evidence is available but the BLEA runtime is not, parse the JSONL as structured JSON
records, require a final complete summary before treating it as a complete capture, and report only
the recorded advertisement, profile, read, notification, error, and cleanup evidence. Do not turn
missing records into successful observations. Live operations require a local Agent host, the BLEA
Python runtime, operating-system Bluetooth permission, and a supported adapter.

## Diagnostic sequence

1. Run `ble_doctor` or `ble doctor --json` when adapter availability is unknown.
2. Scan and preserve the returned identifier, names, RSSI, advertised services, and raw advertising
   evidence.
3. Select by exact identifier. Use an exact name only when one observed device has that name.
4. Inspect the GATT profile before choosing characteristics.
5. For event discovery, use bounded `ble_observe`/`ble observe` before writing; omit characteristics
   to observe all notify/indicate traits from the discovered profile.
6. When probing, continue with `next_read_offset` until it is `null`. `ok=true` means the page ran;
   it does not mean every characteristic read succeeded. Aggregate `read_page.success_count`,
   `failure_count`, and `failure_reasons` across pages, and preserve both successful reads and
   per-characteristic failures.
7. Prefer reads and bounded observation before considering a write. Treat a silent observation
   window as evidence only for that window, not proof that a characteristic never emits events.
8. After the initial diagnosis, save a portable evidence package with `ble_capture` or
   `ble capture`. Use the exact resolved identifier, choose an explicit `.blea.jsonl` output path,
   and set `--redact-identifiers` when the package will leave the workstation. Capture is read-only:
   it records advertisements, the GATT profile, bounded readable-characteristic results, bounded
   notifications, operation errors, and a final integrity summary. It never writes, pairs, or
   changes configuration. Keep the file as the authoritative artifact and report its path plus
   summary status to the user.
9. Compare before/after captures offline with `ble_diff` or `ble diff`. Keep the default identity
   guard for normal comparisons and use `allow_different_devices` only for an intentional
   cross-device comparison. Treat the 5 dBm RSSI tolerance as noise control; use strict RSSI only
   when exact signal samples matter. Diff never scans, connects, pairs, subscribes, or writes.
10. Reproduce captured behavior offline with `ble_replay` or `ble replay`. Use instant timing for
   Agent debugging and CI. Treat `replay_miss` as absent evidence, not device behavior, and do not
   infer a successful subscription from a notify property alone. Replay never accesses a physical
   adapter and never sends or simulates writes.
11. When one authorized write is expected to trigger notifications, use `ble_exchange` or
   `ble_session_exchange`. These operations establish the subscription before writing and collect
   the response atomically; do not run standalone session subscribe and write tools concurrently.
12. Close the exact stateful MCP session once when the task is complete. Use `ble_session_list` when
   cleanup is uncertain. Use `ble_session_close_all` only when a session ID is unknown, an explicit
   close failed, or leaked state must be recovered; do not call it after a successful close.

Do not invent UUIDs, payload encodings, pairing requirements, or protocol semantics. Report the
observed evidence and distinguish it from an inference. Treat `uuid_namespace=custom` as a custom
128-bit UUID even when its leading bytes resemble a Bluetooth SIG assigned number.

## Commands and tools

- Diagnose: `ble doctor --json` or `ble_doctor`.
- Scan: `ble scan --timeout 8 --json` or `ble_scan`.
- Inspect: `ble inspect --device "id:<identifier>" --json` or `ble_inspect`.
- Probe readable characteristics: use `ble probe --device "id:<identifier>" --max-reads 32
  --read-offset <offset> --json` or `ble_probe`, following `next_read_offset` across pages.
- MCP probe results omit the full GATT tree by default while retaining `profile_summary`; call
  `ble_inspect` first or set `include_profile=true` when the full profile is needed on that page.
- Read: `ble read --device "id:<identifier>" --characteristic <uuid> --json` or `ble_read`.
- Notify: use `ble subscribe ... --jsonl` or `ble_subscribe` with a bounded duration.
- Observe all event-capable traits: use `ble observe --device "id:<identifier>" --duration 10
  --jsonl` or `ble_observe`. Pass `--characteristic <uuid>` repeatedly for explicit selection.
- Capture a unified read-only evidence package: use
  `ble capture --device "id:<identifier>" --output capture.blea.jsonl --observe-duration 10
  --max-reads 128 --redact-identifiers --json` or `ble_capture`. `--read-offset` starts at a
  deterministic readable-characteristic offset and the result's `read_page.next_offset` indicates
  whether a larger limit or a follow-up capture is needed.
- Compare complete captures offline: use
  `ble diff before.blea.jsonl after.blea.jsonl --json` or `ble_diff`. Inspect `added`, `removed`,
  and `changed` paths. Use `--strict-rssi` only when needed, and use `--fail-on-change` only when CI
  should return exit code 3 for a valid comparison containing differences.
- Replay one captured operation offline: use `ble_replay` or
  `ble replay capture.blea.jsonl <scan|inspect|probe|read|subscribe|observe|run>`. The captured
  identifier is selected automatically unless an exact device is supplied. Keep `speed=0` for
  deterministic immediate output; use a positive speed multiplier only when event gaps matter.
- Serve normal MCP tools from evidence: start `ble replay capture.blea.jsonl mcp`. Verify each
  result has the expected `replay.capture_id` and `replay.read_only=true`. This mode is useful when
  an Agent or CI integration should exercise its existing `ble_read`/`ble_observe` path unchanged.
- Guarded request/notification exchange: use `ble exchange ... --jsonl`, `ble_exchange`, or
  `ble_session_exchange` to subscribe before one write and collect its resulting events.
- Multi-step work: open an MCP session, note its `idle_timeout_seconds`, use
  `ble_session_observe` when the connection should be reused, then close the session.
- Repeatable work: encode the sequence in a guarded YAML file and run `ble run`.
- Repeatable request/notification checks: use a YAML `exchange` action with separate
  `write_characteristic` and `notify_characteristic` fields. Assert the notification count/content,
  final notification, and `cleanup.ok` when the protocol has deterministic events.

Read [workflows.md](references/workflows.md) before creating or editing workflow YAML. Read
[safety.md](references/safety.md) before any write, pairing-sensitive operation, firmware update,
lock, actuator, or other state-changing action.

`timeout` is a per-backend-operation bound, not a total command or tool deadline. Allow for device
discovery, connection, profile discovery, each requested read, and any subscription duration when
setting an outer Agent/tool timeout.

Capture files use Evidence Format v1. Read
[evidence-format-v1.md](https://github.com/Nitmi/blea/blob/v0.6.1/docs/evidence-format-v1.md)
when an agent needs to validate, redact, or build replay tooling around a package. Read
[diff-format-v1.md](https://github.com/Nitmi/blea/blob/v0.6.1/docs/diff-format-v1.md) before
interpreting comparison policy, stable paths, ignored fields, identity guards, or CI exit behavior.
Read [replay-format-v1.md](https://github.com/Nitmi/blea/blob/v0.6.1/docs/replay-format-v1.md)
before interpreting missing evidence, captured failures, notification timing, replay MCP mode, or
the read-only safety boundary. Read
[platform-acceptance.md](https://github.com/Nitmi/blea/blob/v0.6.1/docs/platform-acceptance.md)
before claiming platform support, running a cross-platform hardware acceptance, or publishing a
real-device capture fixture.

## Write policy

Treat every write as dangerous until the device protocol establishes otherwise.

- Require the user to authorize the specific state-changing operation.
- Require `allow_write=true` and `confirm_device=<resolved identifier>` for MCP writes.
- Require both `--allow-write` and `--confirm-device <resolved identifier>` for CLI writes.
- Never confirm with a friendly name, substring, stale identifier, or guessed address.
- Prefer write-with-response and read-back verification when supported.
- Prefer atomic exchange notification verification when a write triggers asynchronous events.
- Stop when the selected device is ambiguous or a prerequisite read/assertion fails.

Return the structured failure instead of bypassing a guard.
