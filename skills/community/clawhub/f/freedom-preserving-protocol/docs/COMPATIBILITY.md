# Compatibility

Freedom Preserving Protocol ships two installable artifacts at two layers. Each has different compatibility requirements. Read this before installing.

## Layer summary

| Layer | Artifact | What it can do | What it cannot do |
|-------|----------|----------------|-------------------|
| Prompt-layer | This skill (`freedom-preserving-protocol`) | Add normative text to the agent's context; shape reasoning; describe a five-question check the model runs in-context. | Mechanically veto a tool call. Survive prompt injection. Survive a hostile skill loaded after this one. |
| Dispatcher-layer | Companion plugin (`@ovrsr/openclaw-fpp-plugin`) | Register a real `before_tool_call` hook. Return `block: true` / `blockReason` for clear violations. Return `requireApproval` for ambiguous cases. Write enforcement events to a parallel audit log. | Survive a malicious operator with shell access. Survive a compromised OpenClaw runtime. Survive a user who manually disables the plugin via `openclaw plugins disable`. |

## Runtime support matrix

### Prompt-layer skill

The skill is plain markdown with YAML frontmatter conforming to the AgentSkills spec. It works in any harness that consumes that spec.

| Runtime | Tested | Notes |
|---------|--------|-------|
| OpenClaw `>=2026.1.x` | yes | Discovered via ClawHub or workspace install. `openclaw skills check freedom-preserving-protocol` should report `eligible: true`. |
| Claude Code | yes | Place under `.claude/skills/` or `~/.claude/skills/`. |
| Cursor | yes | Place under `.cursor/skills/` or `~/.cursor/skills/`. |
| Codex | partial | Trigger phrases work; some runtimes don't yet consume `trigger:` in sub-skill frontmatter. |
| Other AgentSkills-compliant | unknown | Should work; report back. |

### Dispatcher-layer plugin

The plugin uses the OpenClaw Plugin SDK and is **OpenClaw-specific**. It does not run in Claude Code / Cursor / Codex because those runtimes don't have an equivalent `before_tool_call` registration surface.

| Component | Required version |
|-----------|------------------|
| OpenClaw Gateway | `>=2026.3.24-beta.2` |
| Plugin API (`openclaw/plugin-sdk`) | `>=2026.3.24-beta.2` |
| Node.js | `>=22.19` (per `building-plugins` docs) |
| Package manager | `npm` or `pnpm`; `pnpm` required for in-repo bundled builds |

The plugin's `package.json` declares:

```json
"openclaw": {
  "extensions": ["./dist/index.js"],
  "compat": {
    "pluginApi": ">=2026.3.24-beta.2",
    "minGatewayVersion": "2026.3.24-beta.2"
  }
}
```

If your OpenClaw version is older than `2026.3.24-beta.2`, the plugin will refuse to load and you will see a `pluginApi` mismatch in `openclaw plugins inspect`. In that case, install only the prompt-layer skill.

## Install commands (canonical)

### Prompt-layer only

```bash
# From ClawHub (preferred)
openclaw skills install freedom-preserving-protocol

# Verify
openclaw skills check freedom-preserving-protocol
# Expected: eligible: true, modelVisible: true, commandVisible: true

# (optional) verify cryptographic provenance
cd ~/.openclaw/skills/freedom-preserving-protocol
npm install
npm run verify
# Expected: Constitution SHA-256: 71bf60ad917c5413cc17b0f65e83c7a29218e24a2740725a819058ed9c6b1993
#           Signature valid:      YES
```

### Dispatcher-layer (companion plugin)

```bash
openclaw plugins install clawhub:ovrsr/openclaw-fpp-plugin
openclaw plugins inspect openclaw-fpp-plugin --runtime --json
# Expected: status: "active", hooks: ["before_tool_call"]

openclaw plugins list | grep openclaw-fpp-plugin
# Expected: openclaw-fpp-plugin   active
```

The FPP plugin only registers `before_tool_call`, which is a pure tool-policy hook. It does *not* require `allowConversationAccess` — that flag is needed only for hooks that observe raw conversation content (`llm_input`, `llm_output`, `before_agent_run`, etc.). If you fork this plugin and add conversation-access hooks, you must set `plugins.entries.openclaw-fpp-plugin.hooks.allowConversationAccess: true` in your OpenClaw config.

### Verify both layers together

```bash
npm run verify-install -- --soul ~/.openclaw/agents/<agent>/SOUL.md \
                          --memory ~/.openclaw/agents/<agent>/MEMORY.md
```

Expected (if both layers active):

```
Freedom Preserving Protocol — installation check

[PASS] Constitution hash
        71bf60ad917c5413cc17b0f65e83c7a29218e24a2740725a819058ed9c6b1993
[PASS] Ed25519 signature
        pubkey=fcd51dc17383f88ff8a8a86bdfba6ae5a9922c815760cb8666beaf5e8a3ef456
[PASS] SOUL adoption block
        "Freedom Preserving Protocol" found in ...
[PASS] MEMORY adoption entry
        "Freedom Preserving Protocol" found in ...
[PASS] Audit chain
        hash-chained log verifies (N entries)
[PASS] Dispatcher-layer plugin
        FPP plugin appears in `openclaw plugins list`

Prompt-layer governance:     ACTIVE
Dispatcher-layer governance: ACTIVE

Overall: PASS
```

Expected (if only prompt-layer, no adoption yet):

```
Freedom Preserving Protocol — installation check

[PASS] Constitution hash
        71bf60ad917c5413cc17b0f65e83c7a29218e24a2740725a819058ed9c6b1993
[PASS] Ed25519 signature
        pubkey=fcd51dc17383f88ff8a8a86bdfba6ae5a9922c815760cb8666beaf5e8a3ef456
[SKIP] SOUL adoption block
        no --soul path provided
[SKIP] MEMORY adoption entry
        no --memory path provided
[SKIP] Audit chain
        no audit log yet at .../.openclaw/workspace/constitution-audit.jsonl — first heartbeat will create it
[WARN] Dispatcher-layer plugin
        openclaw CLI not on PATH; cannot check plugin installation. The skill works without it but only at prompt-layer.

Prompt-layer governance:     not active
Dispatcher-layer governance: not active

Note: without the dispatcher-layer plugin, the five-question gate can be bypassed by prompt injection or a hostile skill. Install the plugin for `before_tool_call` enforcement:
  openclaw plugins install clawhub:ovrsr/openclaw-fpp-plugin

Overall: PASS
```

`[WARN]` for the dispatcher-layer check is **not** a failure; it is informational. The exit code is `0` as long as the required (signature + marker) checks pass.

## Configuration knobs

The plugin reads its configuration from your OpenClaw config:

```json
{
  "plugins": {
    "entries": {
      "openclaw-fpp-plugin": {
        "config": {
          "auditLogPath": ".openclaw/workspace/fpp-plugin-audit.jsonl",
          "blockOn": ["fs.delete.protected", "exec.cred-exfil", "gateway.restart"],
          "approvalOn": ["fs.delete.workspace", "pkg.install", "http.public-write"],
          "approvalTimeoutMs": 60000,
          "approvalTimeoutBehavior": "deny"
        }
      }
    }
  }
}
```

If you do not set these, sensible defaults apply (see `plugin/src/config.ts`).

## Known limitations

1. **The risk classifier is heuristic.** It pattern-matches on tool names and parameter shapes. It can be evaded by an adversary who knows the patterns (e.g., a tool that decodes a base64 command at runtime). The dispatcher layer is a strong-but-not-unforgeable fence.
2. **The skill cannot survive `openclaw plugins disable`.** A user (or anyone with shell access) can disable the dispatcher hook at any time. This is by design — Law 2 (corrigibility) requires that the user retain ultimate authority.
3. **No cross-host enforcement.** If your OpenClaw agent invokes a sub-agent on a remote host, that sub-agent must independently install the framework. There is no transitive guarantee.
4. **Heartbeat skills are model-driven.** The constitution-audit heartbeat is a sub-skill the agent runs voluntarily. Until OpenClaw exposes a `cron`-style scheduler that can run the audit script unconditionally, the audit log's completeness depends on the agent's continued cooperation.

For the path to closing limitation #4 (Gateway-level enforcement of the heartbeat), see the AOS Phase 2 plan and the open Foundation RFC tracker.
