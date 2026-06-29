# MCP-Native Agents

> Members of this family speak MCP `2024-11-05` natively. **All protocol details
> (12 tools, error codes, billing) live in [`../SKILL.md`](../SKILL.md) — do not duplicate.**

## Verified members

These rows are backed by a runnable snippet below. Other agents in this family are
listed under [Unverified members](#unverified-members) — see the policy in
[`./README.md`](./README.md#adding-a-new-agent).

| Agent | Transport | Verified on | Known quirks |
|-------|-----------|-------------|--------------|
| Claude Code | stdio MCP or HTTP JSON-RPC | 2026-06-17 | Paste the `## instructions` block from `../usage/instructions.md` into the system prompt. For the full doc layout, see `../SKILL.md` §7. |
| Cline (VS Code) | stdio MCP | 2026-06-17 | Default tool timeout ~60s — **t4 must be tuned to ≥120s** |

## Unverified members

> The agents below are believed to fit this family but no runnable snippet has been
> validated against a live config. To promote one, add a verified snippet in the
> "Agent-specific snippets" section and update the `Verified on` column.

| Agent | Transport | Suspected quirk |
|-------|-----------|-----------------|
| Codex CLI | stdio MCP | Config lives in `~/.codex/config.toml` `mcp_servers` block |
| Cursor | stdio MCP | Default tool timeout tight; same ≥120s guidance for t4 |
| OpenClaw | stdio MCP | Open-source framework; config file format varies per release |
| Hermes | HTTP MCP (SSE or streamable) | Python `mcp` client SDK; check stdio vs SSE support |

## Common setup (any member)

1. Register fortune-hub as an MCP server with base URL `https://fortunehub.lighttune.com.au`.
2. Point at `/.well-known/mcp.json` for discovery (cache 5 min).
3. Auth via `Authorization: Bearer <api_key>` header on every `tools/call`.
4. Set client tool timeout to **≥120s** to absorb t4 latency (~30–90s).

## Agent-specific snippets

### Claude Code (stdio MCP via thin shim)

Register the server with `claude mcp add`, or add it to a project-scoped `.mcp.json`
(repo root) — both use the same `mcpServers` shape:

```json
{
  "mcpServers": {
    "fortune-hub": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://fortunehub.lighttune.com.au/api/mcp"],
      "env": {
        "FORTUNE_HUB_API_KEY": "<your-api-key>"
      }
    }
  }
}
```

Invocation example from a Claude Code session:

```
Use mcp__fortune-hub__bazi_basic_analysis with birth_year=1985, birth_month=7,
birth_day=15, birth_hour=14, birth_minute=30, gender=male,
location={"city_name": "Beijing"}.
```

For tool name ↔ request field semantics, error codes, and billing, see
[`../SKILL.md`](../SKILL.md) §3 and §5.

### Cline (VS Code) — t4 timeout is mandatory

`settings.json` (workspace or user):

```json
{
  "cline.mcpServers": {
    "fortune-hub": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://fortunehub.lighttune.com.au/api/mcp"],
      "env": {
        "FORTUNE_HUB_API_KEY": "<your-api-key>"
      },
      "disabled": false
    }
  },
  "cline.mcp.toolTimeoutMs": 120000
}
```

Quoting [`../SKILL.md`](../SKILL.md) §2 verbatim: **t4 client timeout**: "`bigluck_year_fortune_eval`
may take up to ~90s (LLM jitter). Some MCP clients default to ~60s tool timeout.
**Configure your client tool timeout to ≥120s.**" Setting `cline.mcp.toolTimeoutMs`
to `120000` is the only way to keep t4 from being killed mid-LLM.

## When NOT to use this family

- Agent has no MCP support (browser-only, web-agent, function-call-only) → [`rest-only.md`](./rest-only.md)
- Agent supports MCP but the deployment cannot reach `/api/mcp` directly → [`mixed.md`](./mixed.md)

---

*Last verified: 2026-06-17. Verified on column reflects the date the runnable
snippet was last checked end-to-end. See [README.md](./README.md#adding-a-new-agent)
for the verified/unverified promotion policy.*
