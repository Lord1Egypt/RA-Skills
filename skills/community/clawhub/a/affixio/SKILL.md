---
name: affixio
description: "Host-side AffixIO attestation before high-value agent actions; signed allow/deny without sending PII off-host."
metadata:
  {
    "openclaw":
      {
        "emoji": "🔏",
        "homepage": "https://github.com/AffixIO/affixio-mcp",
        "requires": { "bins": ["npx"], "env": ["AFFIX_API_KEY"] },
        "primaryEnv": "AFFIX_API_KEY",
      },
  }
---

# AffixIO attestation

Use AffixIO when the agent is about to take a privileged or irreversible action (payments, tool gates, outbound sends, destructive ops). Prove the action on the host first. Do not send raw credentials or PII to AffixIO.

## Preferred path: local MCP

If `@affixio/mcp` is available, prefer the MCP tools:

- `attest_action` — signed yes/no that an action happened on the host
- `verify_action` — check an attestation or receipt
- `gate_tool_call` — allow/deny before a privileged tool call

Install / probe:

```bash
npx -y @affixio/mcp@0.1.0 probe
```

Claude Desktop / Cursor-style config:

```json
{
  "mcpServers": {
    "affixio": {
      "command": "npx",
      "args": ["-y", "@affixio/mcp@0.1.0"],
      "env": {
        "AFFIX_API_KEY": "local_operator",
        "AFFIX_MCP_HOME": "${HOME}/.affix-mcp"
      }
    }
  }
}
```

`AFFIX_API_KEY` may be `local_operator` for offline local use.

## SDK path

When wiring scripts or custom tools:

```bash
npm i affixio
```

```js
import { AffixSDK } from "affixio";

const affix = new AffixSDK({ apiKey: process.env.AFFIX_API_KEY });
const proof = await affix.prove({ claim: "approved" });
```

For agent trust / spend gates, use the SDK helpers documented in https://github.com/AffixIO/SDK (`createAgentTrust`, `mcpToolGate`, `x402BeforePay`).

## Rules

- Attest **before** the high-value tool runs; fail closed on deny or verify failure.
- Keep tool arguments hashed or summarized; do not paste secrets into AffixIO prompts.
- Prefer HMAC prove for latency; UltraHonk only when a stronger proof is required.
- Dashboard (optional): `npx affixio dashboard` → http://127.0.0.1:8787

## When not to use

Skip AffixIO for read-only, local, low-risk lookups (docs search, status checks).
