---
name: diplomat-heartbeat
description: Surfaces overdue and upcoming commitment deadlines on every human message.
metadata:
  openclaw:
    events:
      - command:new
    timeout_ms: 500
    fail_open: true
---

On every new command, checks MEMORY.md ## Diplomat Commitments for [ACTIVE] entries
whose deadline has passed or is within 2 hours. Notifies the human via session notify.
Also checks ledger.json for INBOUND_PENDING sessions (inbound proposals from peers
waiting for human approval) and surfaces them as notifications.
