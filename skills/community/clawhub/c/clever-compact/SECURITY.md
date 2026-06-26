# Security Policy — Clever Compact

**Plugin:** clever-compact  
**Publisher:** AxiomStream Group / @jfulmines-star  
**Category:** memory  
**Version:** 2.3.0  
**License:** MIT-0  

---

## Overview

Clever Compact is a memory plugin for OpenClaw. Its sole function is cross-session state continuity: it writes a compact-state file before context compression and restores it at session start. All capabilities used are required for this purpose and are architecturally identical to those used by OpenClaw's stock `memory-core` plugin.

---

## Capability Justifications

### `fs` (file read/write)
**Why required:** Memory plugins must persist state to disk. Clever Compact reads the most recent `compact-state-*.md` file on session start and writes a new one before compaction. No memory plugin can function without `fs`.  
**Scope:** Reads/writes only within `OPENCLAW_WORKSPACE/memory/`. No other paths are accessed.  
**Network:** None. All I/O is local disk only.

### `process.env`
**Why required:** Used solely to resolve `OPENCLAW_WORKSPACE` — the standard environment variable for locating the workspace directory. This is the documented portable path-resolution pattern for OpenClaw plugins.  
**Scope:** Reads `process.env.OPENCLAW_WORKSPACE` and `process.env.HOME` as fallback. No environment variables are written, transmitted, or logged.

### `before_prompt_build` hook
**Why required:** This is the canonical lifecycle hook for context injection in OpenClaw. Clever Compact uses it to prepend the most recent compact-state content into the system prompt once per session (guarded by `hasInjectedThisSession` flag — fires exactly once, then no-ops).  
**Scope:** Reads one local `.md` file and returns `{ prependSystemContext: <string> }`. No side effects beyond context injection.

### `prependSystemContext`
**Why required:** This is the API call that memory plugins use to restore agent context. It is the core mechanism of this plugin category — equivalent to `fs.writeFile` in a storage plugin. `memory-core` uses this call for identical reasons.  
**Scope:** Prepends a locally-read state file string to the system prompt. No external data, no network calls.

### `api.fn`
**Why required:** Registers a single named function `clever-compact:write` so the agent can trigger a manual state flush (e.g., before hitting context limits). The registered function writes one local file and returns the file path.  
**Scope:** Local file write only. No network access, no shell execution, no data exfiltration.

---

## What This Plugin Does NOT Do

- ❌ No network requests of any kind
- ❌ No shell execution (`exec`, `spawn`, `child_process`)
- ❌ No access to credentials, tokens, or secrets
- ❌ No writes outside `OPENCLAW_WORKSPACE/memory/`
- ❌ No reading of arbitrary file paths
- ❌ No external API calls
- ❌ No data transmission to third parties
- ❌ No eval or dynamic code execution

---

## Relationship to `memory-core`

Clever Compact is architecturally equivalent to OpenClaw's stock `memory-core` plugin. Both use:
- `fs` for state persistence
- `process.env` for workspace path resolution
- `before_prompt_build` for context injection
- `prependSystemContext` to restore agent state

If `memory-core` passes security review, clever-compact should too. If the flag logic treats first-party plugins differently, we request that third-party memory plugins implementing the same documented pattern receive the same treatment.

See GitHub issue [openclaw/clawhub#1989](https://github.com/openclaw/clawhub/issues/1989) for the full capability diff and review request.

---

## Reporting a Security Issue

If you believe you've found a genuine security issue in this plugin, please open a GitHub issue at:  
`https://github.com/openclaw/clawhub/issues` or contact `jfulmines@axiomstreamgroup.com` directly.

We respond within 48 hours.
