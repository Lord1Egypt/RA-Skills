---
name: "AI Agent OPSEC — Runtime Classified Data Enforcer"
description: "Prevent your AI agent from leaking classified terms to external APIs, subagents, or logs. Term registry + runtime redaction + pre-publish audit. Zero dependencies, zero network calls."
author: "@TheShadowRose"
version: "1.4.0"
tags: ["opsec", "security", "redaction", "privacy", "classified", "agent-safety"]
license: "MIT"
---

# AI Agent OPSEC — Runtime Classified Data Enforcer

Keep your secrets out of web searches, external LLM calls, and subagent spawns.

## Side Effects (Declared)

| Type | Path | Description |
|------|------|-------------|
| **READS** | `<workspace>/classified/classified-terms.md` | Your term registry — add terms here once, protected everywhere |
| **WRITES** | `<workspace>/memory/security/classified-access-audit.jsonl` | Append-only audit log; auto-rotates at 1MB; **never contains original sensitive text** |
| **NETWORK** | None | Zero external calls. Fully local. |

> **Important:** Add `classified/` and `memory/security/` to your `.gitignore` to prevent accidental commits.

## Setup

1. Create `classified/classified-terms.md` in your workspace root
2. Add one term per line (blank lines and `#` comments ignored)
3. Require and use the enforcer before any external call

```javascript
const ClassifiedAccessEnforcer = require('./src/ClassifiedAccessEnforcer');
const enforcer = new ClassifiedAccessEnforcer('/path/to/workspace');

// Before any external API call
const { safe, payload } = enforcer.gateExternalPayload(userQuery, 'web_search');

// Before spawning a subagent
const { task } = enforcer.redactTaskBeforeSpawn(taskString, 'ResearchAgent');
```

See README.md for full documentation.

