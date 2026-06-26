# AI Agent OPSEC v1.4.0 — Runtime Classified Data Enforcer

Prevent your AI agent from leaking classified terms to external APIs, subagents, or logs. Term registry + runtime redaction + pre-publish audit. Zero dependencies, zero network calls.

---

## Quick Start

```javascript
const ClassifiedAccessEnforcer = require('./src/ClassifiedAccessEnforcer');

const enforcer = new ClassifiedAccessEnforcer('/path/to/workspace');

// Gate any external API call
const { safe, payload } = enforcer.sanitizeOutbound(userQuery, 'web_search');
if (!safe) {
  // Redacted automatically — payload is now safe to send
}
await callExternalAPI(payload);

// Redact before spawning a subagent
const { task } = enforcer.redactTaskBeforeSpawn(taskString, 'ResearchAgent');
```

---

## Setup

**1. Create your term registry:**

```
<workspace>/classified/classified-terms.md
```

Add one term per line. Blank lines and `#` comments are ignored:

```
# Internal project codenames
APEX
CRUCIBLE

# Personal details
MyRealName

# Credentials
my-secret-api-prefix

# Case-sensitive: proper nouns matched as-is, lowercase terms matched case-insensitively
```

**2. Configure your agent lists** (in `ClassifiedAccessEnforcer.js`):

```javascript
// Agents that make external network calls — classified data must NEVER reach them
this.externalAgents = ['ResearchAgent', 'WebSearchAgent', 'PublisherAgent'];

// Agents that are internal-only — still redacted as defense-in-depth
this.internalAgents = ['CoderAgent', 'AuthorAgent', 'MemoryAgent'];
```

**3. Add to `.gitignore`:**

```
classified/
memory/security/
```

---

## API Reference

### `sanitizeOutbound(payload, service)`

Call before any web search, external LLM call, or outbound HTTP request. Redacts classified terms and logs the action.

```javascript
const result = enforcer.sanitizeOutbound(text, 'web_search');
// result.safe          — true if no terms were found
// result.sanitized       — redacted text (safe to send)
// result.redactionCount — number of terms removed
// result.service       — echoed service name
```

### `redactTaskBeforeSpawn(task, agentType)`

Redact classified terms from a task string before spawning an agent. Throws if the agent is in `externalAgents`.

```javascript
try {
  const { task: safeTask } = enforcer.redactTaskBeforeSpawn(rawTask, 'ResearchAgent');
  spawnAgent('ResearchAgent', safeTask);
} catch (e) {
  // Agent is blocked from receiving this task
  console.error(e.message);
}
```

### `validateSubagentAccess(agentType)`

Check whether an agent is allowed to receive classified context.

```javascript
const result = enforcer.validateSubagentAccess('ResearchAgent');
// result.allowed  — boolean
// result.reason   — human-readable explanation
// result.action   — 'BLOCK_SPAWN' if denied
```

### `containsClassified(text)`

Check if text contains any classified terms without redacting or logging.

```javascript
if (enforcer.containsClassified(userInput)) {
  // Handle before any external call
}
```

### `getAuditReport(limit)`

Get recent audit log entries.

```javascript
const report = enforcer.getAuditReport(20);
// report.total   — total log entries
// report.recent  — last N entries
```

---

## CLI

```bash
# Check agent access permission
node src/ClassifiedAccessEnforcer.js check ResearchAgent

# Redact text
node src/ClassifiedAccessEnforcer.js redact "My project APEX is..."

# Gate external payload
node src/ClassifiedAccessEnforcer.js gate "Searching for info about CRUCIBLE..."

# View recent audit log
node src/ClassifiedAccessEnforcer.js audit

# Run self-test (including log safety verification)
node src/ClassifiedAccessEnforcer.js test
```

---

## Security Design

**Audit log never contains original text.** Logs use already-redacted previews — the original classified content is never written to disk.

**Term loading is runtime.** Patterns reload from `classified-terms.md` on each call — add a term once, protected everywhere immediately, no restart needed.

**Proper noun matching.** Terms starting with an uppercase letter are matched case-sensitively. Lowercase terms match case-insensitively. Both use word-boundary matching.

**Log rotation.** Audit log auto-rotates at 1MB — old log is renamed with a timestamp suffix before a new file begins.

**No network calls.** The enforcer is fully local. Zero external dependencies.

---

## Side Effects (Declared)

| Type | Path | Description |
|------|------|-------------|
| **READS** | `<workspace>/classified/classified-terms.md` | Term registry |
| **WRITES** | `<workspace>/memory/security/classified-access-audit.jsonl` | Append-only audit log; auto-rotates at 1MB; never contains original sensitive text |
| **NETWORK** | None | Zero external calls. Fully local. |

---

## ⚠️ Disclaimer

This software is provided "AS IS", without warranty of any kind, express or implied.

**USE AT YOUR OWN RISK.**

- The author(s) are NOT liable for any damages, losses, or consequences arising from
  the use or misuse of this software — including but not limited to financial loss,
  data loss, security breaches, business interruption, or any indirect/consequential damages.
- This software does NOT constitute financial, legal, trading, or professional advice.
- Users are solely responsible for evaluating whether this software is suitable for
  their use case, environment, and risk tolerance.
- No guarantee is made regarding accuracy, reliability, completeness, or fitness
  for any particular purpose.
- The author(s) are not responsible for how third parties use, modify, or distribute
  this software after purchase.

By downloading, installing, or using this software, you acknowledge that you have read
this disclaimer and agree to use the software entirely at your own risk.

**DATA DISCLAIMER:** This software processes and stores data locally on your system.
The author(s) are not responsible for data loss, corruption, or unauthorized access
resulting from software bugs, system failures, or user error. Always maintain
independent backups of important data. This software does not transmit data externally
unless explicitly configured by the user.

---

## Support & Links

| | |
|---|---|
| 🐛 **Bug Reports** | TheShadowyRose@proton.me |
| ☕ **Ko-fi** | [ko-fi.com/theshadowrose](https://ko-fi.com/theshadowrose) |
| 🛒 **Gumroad** | [shadowyrose.gumroad.com](https://shadowyrose.gumroad.com) |
| 🐦 **Twitter** | [@TheShadowyRose](https://twitter.com/TheShadowyRose) |
| 🐙 **GitHub** | [github.com/TheShadowRose](https://github.com/TheShadowRose) |
| 🧠 **PromptBase** | [promptbase.com/profile/shadowrose](https://promptbase.com/profile/shadowrose) |

*Built with [OpenClaw](https://github.com/openclaw/openclaw)*

---

🛠️ **Need something custom?** Custom OpenClaw agents & skills starting at $30. If you can describe it, I can build it. → [Hire me on Fiverr](https://www.fiverr.com/s/jjmlZ0v)


