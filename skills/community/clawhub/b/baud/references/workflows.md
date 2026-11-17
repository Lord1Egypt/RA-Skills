# Baud Workflow Authoring and Results

## Minimal Guarded Workflow

```yaml
version: 1
name: guarded-device-action

serial:
  port: COM14
  baudrate: 115200
  timeout: 0.05
  write_timeout: 1
  line_ending: crlf
  encoding: utf-8
  decode_errors: replace
  dtr: false
  rts: false
  settle_ms: 300
  drain_ms: 500

steps:
  - id: identify
    send: version
    wait: 2
    expect:
      response_required: true
      contains: ["EXPECTED-FIRMWARE"]
      not_contains: ["ERR", "failed"]

  - id: configure
    send: target=10
    wait: 1
    expect:
      contains: ["target=10"]

  - id: verify
    send: status
    wait: 2
    expect:
      contains: ["target=10", "fault=0"]
      not_contains: ["ERR", "failed"]

  - id: act_once
    send: start
    wait: 3
    dangerous: true
    requires: [identify, configure, verify]
    expect:
      contains: ["started"]

  - id: observe
    monitor: 10

  - id: final_state
    send: status
    wait: 2
    expect:
      contains: ["running=0", "fault=0"]
```

Replace every example command and assertion with the connected firmware's documented protocol before running it.

## Step Types

Define exactly one action per step:

- `send`: transmit text plus the configured or step-specific line ending, then collect a bounded response.
- `monitor`: receive without transmitting for a duration in seconds.
- `drain`: consume queued input for a duration in seconds.
- `sleep`: wait without serial I/O for a duration in seconds.

Use `wait` in seconds or `read_ms` in milliseconds for a send response window. Override `line_ending` on a step only when diagnosing or supporting a mixed protocol.

## Assertions

Under `expect`, use:

- `response_required: true`
- `contains`: literal strings that must appear
- `not_contains`: literal strings that must not appear
- `regex`: patterns that must match
- `not_regex`: patterns that must not match
- `fail_if_contains`: alias for forbidden literal strings

Prefer specific positive state assertions over generic `OK`. An echoed command, transport success, or absence of `ERR` does not prove the requested state.

Assertions fail the workflow by default. Use `continue_on_failure: true` only for deliberate diagnostic branches where later read-only evidence remains useful. Never use it to bypass a prerequisite for a dangerous step.

## Guards

Set `dangerous: true` for physical or persistent actions. Such a step must declare `requires`; the configuration is rejected otherwise. A required step counts only when its assertions succeeded during the current run.

## Machine Results

Run with `--json` for one final object or `--jsonl` for ordered events. Important fields include:

- `ok`
- `exit_code`
- `reason`
- `failed_step`
- `steps[].text`
- `steps[].bytes_received`
- `log_file`
- `events_file`

Exit codes:

| Code | Meaning |
| ---: | --- |
| 0 | Command or workflow completed |
| 2 | Step or guard failed |
| 3 | Assertion failed |
| 4 | Port missing, busy, disconnected, or unreadable |
| 5 | Timeout |
| 6 | Encoding or protocol error |
| 7 | Workflow configuration error |

Do not equate exit 0 with physical success unless the workflow contains assertions that prove the required final device state.
