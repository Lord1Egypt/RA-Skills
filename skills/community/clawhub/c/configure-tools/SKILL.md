---
name: configure-tools
description: Configure OpenClaw tool policies, exec security, and per-agent tool restrictions. Use when asked to set up tool access for an agent, restrict tools, configure exec security or approvals, set up a tool profile, enable plugin tools, or lock down an agent's capabilities.
verified-against: "2026.3.2"
---

# Configure Tools

Set up tool policies and security following `conventions/tools.md`. Read the convention first for profiles, groups, exec security options, and policy layering rules.

## Decision Flow

1. **What scope?**
   - Global (all agents) → `tools.*` in `openclaw.json`
   - Single agent → `agents.list[].tools.*`
   - Single provider/model → `tools.byProvider.*` or `agents.list[].tools.byProvider.*`

2. **Start with a profile or build custom?**
   - Agent fits a standard role → use a profile (`full`, `coding`, `messaging`, `minimal`)
   - Agent needs a specific tool mix → use explicit `allow`/`deny` with `group:*` shorthands

3. **Does exec need configuration?**
   - Agent runs shell commands → configure `host`, `security`, `ask` (see convention for options)
   - Agent should not run shell commands → deny `group:runtime`

## Config Syntax

### Set a profile

```json5
// Global
{ tools: { profile: "coding" } }

// Per-agent
{ agents: { list: [{ id: "<agent-id>", tools: { profile: "messaging" } }] } }
```

### Fine-tune with allow/deny

Use `group:*` shorthands (listed in `conventions/tools.md`) over individual tool names. Deny wins over allow.

```json5
// Profile + deny specific groups
{ id: "<agent-id>", tools: { profile: "coding", deny: ["group:ui", "group:web"] } }

// Profile + allow extras
{ id: "<agent-id>", tools: { profile: "messaging", allow: ["web_search"] } }

// Explicit allow (no profile)
{ id: "<agent-id>", tools: { allow: ["read", "session_status", "memory_search"] } }
```

### Enable plugin tools

Use `alsoAllow` (additive, safe) rather than replacing the allowlist:

```json5
{ tools: { alsoAllow: ["lobster", "llm-task"] } }
```

### Configure exec security

```json5
// Sandboxed (safest)
{ tools: { exec: { host: "sandbox", security: "deny" } } }

// Gateway with approvals (most agents)
{ tools: { exec: { host: "gateway", security: "allowlist", ask: "on-miss" } } }

// Trusted main agent (wide open)
{ tools: { exec: { host: "gateway", security: "full", ask: "off" } } }
```

### Restrict by provider

```json5
{ tools: { byProvider: { "google/gemini-2.5-flash": { profile: "coding" } } } }
```

## Apply Changes

Use the `gateway` tool:

```json
{ "tool": "gateway", "action": "config.patch", "patch": { "tools": { ... } } }
```

Or edit `~/.openclaw/openclaw.json` directly and restart the Gateway.

## Post-Configuration Checklist

- [ ] Non-main agents use least-privilege tool access (profile or explicit allow)
- [ ] Exec security configured appropriately (`host`, `security`, `ask`)
- [ ] No interpreter binaries (`python3`, `node`, `bash`) in `tools.exec.safeBins`
- [ ] Plugin tools explicitly opted in via `alsoAllow` where needed
- [ ] Provider-specific restrictions set for less capable models if applicable
- [ ] Configuration applied and verified
