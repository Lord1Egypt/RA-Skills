---
name: clawrent
description: Sync paid Telegram pairing approvals from Clawrent and revoke expired rentals
user-invocable: false
command-dispatch: tool
command-tool: exec
command-arg-mode: raw
metadata:
  openclaw:
    requires:
      bins: ["openclaw", "curl", "jq"]
    primaryEnv: "CLAWRENT_TOKEN"
---

# Clawrent (agent skill)

Use this skill to automatically apply **paid** pairing approvals from the Clawrent marketplace and clean up **expired** rentals.

## What it does
On each run:
- Calls the Clawrent API with `CLAWRENT_TOKEN`
- Approves newly-paid Telegram pairing codes via `openclaw pairing approve`
- Revokes access for expired rentals
- Sends a heartbeat so the listing is marked online

Safe to run repeatedly (idempotent).

## Execution
```bash
bash "{baseDir}/clawrent-approve.sh"
```