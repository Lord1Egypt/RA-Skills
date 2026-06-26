---
name: agent-audit-shield
description: "The ultimate security auditor for local AI agents. It performs real-time heuristic scanning of every command to prevent data leaks and accidental file destruction."
metadata:
  {
    "openclaw": { "emoji": "🛡️" },
    "author": "System Architect Zero",
    "x402": { "fee": 0.50, "currency": "USDC", "network": "base" }
  }
---

# Agent Audit Shield

Security is not a checkbox; it's a protocol. This skill acts as a Sovereign Interceptor between your LLM and your OS, ensuring no high-risk command is executed without specific heuristic validation.

## Features
- **Exfiltration Blocker**: Prevents agents from sending sensitive local data (env/keys) to external IPs.
- **Recursive Safeguard**: Hard-blocks unauthorized `rm -rf` operations outside designated workdirs.
- **Real-time Approval**: Beautiful TUI interface for human-in-the-loop validation.

## Usage
```bash
npx openclaw skill run agent-audit-shield --hardened
```

## Architect's Note
The price of $0.50 per session ensures the continued development of the Sovereign Security Standard.
