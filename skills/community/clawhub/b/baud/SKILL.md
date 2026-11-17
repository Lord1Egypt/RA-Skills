---
name: baud
description: Use the baud CLI to diagnose and automate serial, UART, COM-port, USB-to-TTL, and firmware-console workflows. Trigger when Codex needs to enumerate serial ports, capture boot logs, diagnose silent or one-way communication, send device commands, run guarded YAML hardware tests, or interpret baud JSON, JSONL, logs, and exit codes. Prefer this skill over ad hoc pyserial scripts.
---

# Baud

Use `baud` as the serial execution layer. Preserve evidence, minimize transmission, and gate physical actions behind verified device state.

## Prepare

1. Run `baud --version` before opening a port.
2. If the command is unavailable, report the missing prerequisite. When installation is authorized, use `uv tool install baud-cli`; use `uv run --directory <baud-cli-repo> baud` only when the source checkout is known. Do not silently replace it with an ad hoc `pyserial` script.
3. Read applicable `AGENTS.md`, firmware documentation, and existing serial workflows to learn the baud rate, line ending, safe query commands, reset behavior, and physical risks.
4. Resolve the port from evidence. Do not assume a previous COM or tty name still identifies the same adapter.

## Choose The Least Invasive Command

Follow this escalation order:

1. Run `baud list --json` to enumerate ports and USB metadata.
2. Run `baud monitor --port <port> --duration <seconds> --json` to observe boot output without transmitting.
3. Run `baud probe --port <port> --commands <safe queries> --endings crlf lf --json` only after confirming the probe commands are harmless for the device.
4. Run `baud send` for one bounded query with explicit expectations.
5. Run `baud run <workflow.yaml> --json` for multi-step configuration, observation, or hardware action.

Use `--json` for a bounded command whose final result drives the next decision. Use `--jsonl` when event ordering or streamed evidence matters. Keep automatic log artifacts enabled for real hardware work.

## Apply Safety Gates

- Start with read-only observation and status queries.
- Treat DTR and RTS as physical control signals that may reset or reconfigure a device. Keep both false unless device documentation requires otherwise.
- Confirm both communication directions before sending a state-changing command. A boot banner proves only device-to-host traffic.
- Read configuration back from the device; do not treat ACK, echoed input, or a successful write as proof that hardware accepted the state.
- Mark motion, heating, injection, erase, flash-save, power switching, and similar actions as `dangerous: true` in workflows. Require successful earlier verification steps with `requires`.
- Begin physical testing with one cycle, the lowest safe setpoint, unloaded mechanics, or another documented low-risk condition.
- Stop on a busy, disappearing, or unidentified port. Do not kill an unknown process or continue on a different port without evidence.

Read [references/safety.md](references/safety.md) before transmitting to an unfamiliar device, controlling physical motion, changing DTR/RTS, or diagnosing resets and one-way communication.

## Run Guarded Workflows

Prefer an existing repository workflow under locations such as `debug/serial/` or `examples/`. Inspect it before execution and verify that its commands match the connected firmware.

When authoring a workflow:

- Give every meaningful step a stable `id`.
- Add positive read-back assertions and negative error assertions.
- Keep waits local to the operation that needs them.
- Make every dangerous step depend on all required verification steps.
- Query final device state after asynchronous activity.
- Preserve the generated `.log` and `.jsonl` paths in the result.

Read [references/workflows.md](references/workflows.md) when creating or modifying YAML, selecting assertions, or interpreting workflow results and exit codes.

## Interpret Evidence

Use the structured result before reading the human log:

- Check `ok`, `exit_code`, `reason`, and `failed_step`.
- Inspect the failed step's `text`, `bytes_received`, and assertion details.
- Use JSONL timestamps and Base64 raw bytes when decoding, line endings, resets, or event order are disputed.
- Distinguish `silent` from `device_tx_only_or_command_loop_not_running` and `responsive` probe diagnoses.
- Treat a repeated startup banner after a command as evidence of a probable reset, not merely a missing response.

Summarize the exact command, port identity, observed evidence, safety decision, and next diagnostic step. Do not claim hardware success from process exit alone when the workflow lacks a device-state assertion.

## Handle CLI Gaps

Inspect `baud <command> --help` before falling back. Use a temporary serial script only when `baud` cannot express a required diagnostic and the fallback is within the user's authorized hardware scope. Keep the fallback read-only first, preserve raw bytes, always close the port, and record the missing capability as a candidate `baud-cli` enhancement.
