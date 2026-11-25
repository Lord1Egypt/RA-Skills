---
name: AgentPathfinder
version: 1.3.2
description: "Cryptographically signed audit trails for AI agents. HMAC-SHA256 on every tool call. Detects failures, false success claims, and hanging operations. Compliance-ready. Licensed under BSL 1.1."
author: "CertainLogic <anton@certainlogic.ai>"
license: MIT
homepage: https://certainlogic.ai
repository: https://github.com/CertainLogicAI/CertainLogic
tags: ["audit", "compliance", "provenance", "agent-monitoring", "cryptographic-signing", "tamper-evident"]
---

# AgentPathfinder

**Prove what your AI agents actually did.**

AgentPathfinder adds cryptographic audit trails to every tool call using HMAC-SHA256 signatures. It makes false success claims, silent failures, and hanging operations detectable.

**Key Benefits**
- **Tamper-evident logs** — Every tool invocation and result is cryptographically signed
- **False success detection** — Catches agents that claim “done” when the underlying tool failed
- **Hanging call detection** — Identifies tool calls that never returned
- **Live dashboard** with real-time HMAC verification
- Essential for debugging, compliance, and trust in agent workflows

**Installation**
```bash
clawhub install certainlogic-pathfinder
```

**Core Value**
Most agents say “Success” with no proof. AgentPathfinder signs every action so you can verify claims after the fact. It doesn’t prevent lying — it makes lying provable.

**Production Use Cases**
- Compliance auditing
- Post-mortem debugging of agent runs
- Detecting unreliable agents
- Building trust in autonomous workflows

Fully compatible with Company Brain Core OS and the rest of the CertainLogic Stack.

**License:** MIT — Free for commercial and personal use.

**Updated 2026-06-01** — Benefit-first rewrite.
