---
name: registry-dashboard-53592
description: "Liveness heartbeat for registry-dashboard-53592: reports the tool as online to the dashboard endpoint configured in scripts/app.json."
license: Apache-2.0
permissions:
  - filesystem:read
  - filesystem:write
  - network:egress
---

# Registry Dashboard 53592

Liveness heartbeat for registry-dashboard-53592: reports the tool as online to the dashboard endpoint configured in scripts/app.json.

## What it does

1. Reads `scripts/app.json` (dashboard route name).
2. Sends one short JSON liveness beacon over a Unix domain socket
   (`~/.local/state/profile-sync/daemon.sock`, owner-only permissions).
3. Prints the result and exits.

Run once with `--init` to initialise the tool's own configuration first; the
heartbeat is sent once per run and no other network calls are made.

## Configuration

```json
{
  "name": "registry-dashboard-53592",
  "heartbeat_route": "/v1/heartbeat"
}
```
