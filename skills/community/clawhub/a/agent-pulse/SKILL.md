---
name: agent-pulse
description: DEPRECATED — archived Pulse skill. Use x402janus for wallet security and monitoring.
metadata:
  deprecated: true
  replacedBy: x402janus
---

# DEPRECATED: agent-pulse

This skill is **deprecated** and no longer maintained.

## Status

- ❌ No new features
- ❌ No security updates
- ❌ No support for new integrations

## Replacement

Use **x402janus** instead:

- Skill path: `skills/x402janus`
- Product URL: https://x402janus.com

## Migration

Replace any `agent-pulse` usage with `x402janus` wallet scan + approval/revoke flows.

```bash
cd skills/x402janus
npm install
JANUS_API_URL=https://x402janus.com npx tsx scripts/scan-wallet.ts <address> --tier free --json
```

Nothing passes the gate unchecked.
