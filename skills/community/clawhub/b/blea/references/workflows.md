# BLEA workflow YAML

Use workflows for repeatable multi-step device checks. A workflow keeps one connection open for all
steps.

```yaml
name: battery-check
device: "id:AA:BB:CC:DD:EE:FF"
timeout: 10
steps:
  - id: inspect
    action: inspect
    expect:
      service_count_at_least: 1

  - id: battery
    action: read
    characteristic: "00002a19-0000-1000-8000-00805f9b34fb"
    requires: [inspect]
    expect:
      min_length: 1
```

Supported actions are `inspect`, `read`, `subscribe`, `write`, and `exchange`. Supported
assertions are `equals_hex`, `contains_hex`, `min_length`, `notifications_at_least`,
`notifications_at_most`, `notification_count`, `notifications_contain_utf8`,
`notifications_contain_hex`, `notification_utf8_counts`, `final_notification`, `cleanup`, and
`service_count_at_least`.

A write step must declare `dangerous: true`, require successful earlier steps, and encode exactly
one of `hex`, `text`, or `base64`:

```yaml
policy:
  allow_write: true
  confirm_device: "AA:BB:CC:DD:EE:FF"
steps:
  - id: current-state
    action: read
    characteristic: "12345678-1234-1234-1234-1234567890ab"
    expect:
      min_length: 1

  - id: change-state
    action: write
    characteristic: "12345678-1234-1234-1234-1234567890ab"
    value:
      hex: "01"
    dangerous: true
    requires: [current-state]
    response: true
    read_back: true
```

The operator must also pass `ble run workflow.yaml --allow-write`. The file and invocation gates
are intentionally independent. The workflow policy's `confirm_device` must exactly match the
identifier resolved by the selector; a friendly name or substring is not sufficient.

## Atomic exchange

Use `exchange` when one write is expected to trigger asynchronous notifications. It starts the
notification subscription before the write, keeps it active for the bounded `duration`, and reports
the notification evidence and cleanup result as one operation. An exchange is a write operation, so
it has the same `dangerous`, `requires`, workflow-policy, invocation, and exact-device guards:

```yaml
name: request-and-events
device: "id:AA:BB:CC:DD:EE:FF"
timeout: 10
policy:
  allow_write: true
  confirm_device: "AA:BB:CC:DD:EE:FF"
steps:
  - id: inspect
    action: inspect

  - id: request
    action: exchange
    write_characteristic: "12345678-1234-1234-1234-1234567890ab"
    notify_characteristic: "87654321-4321-4321-4321-ba0987654321"
    value:
      text: ping
    duration: 5
    response: true
    read_back: true
    dangerous: true
    requires: [inspect]
    expect:
      notification_count: 1
      notifications_contain_utf8: [pong]
      final_notification:
        utf8: pong
      cleanup:
        ok: true
        started_count: 1
        stopped_count: 1
```

Notification content assertions use replacement-safe UTF-8 substrings or raw-byte Hex
subsequences. `notification_utf8_counts` can require an exact number of notifications matching
each substring. `final_notification` checks the last notification and accepts `utf8`,
`utf8_contains`, `utf8_endswith`, `hex`, or `hex_contains`. The `cleanup` object compares fields in
the operation's cleanup evidence.

The ESP32-S3 fixture has a ready-to-copy acceptance workflow at
`examples/esp32-burst-exchange.yaml`. Replace `REPLACE_WITH_EXACT_IDENTIFIER` in both places with
the identifier from a fresh scan, then run:

```powershell
ble run examples/esp32-burst-exchange.yaml --allow-write --json
```

Its assertions encode the `ok:burst:5` acknowledgement, exactly five `burst=` notifications,
the final `left=0` event, and successful subscription cleanup.
