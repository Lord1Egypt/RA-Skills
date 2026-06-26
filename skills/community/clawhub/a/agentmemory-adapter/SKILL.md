---
name: agentmemory-adapter
description: Install, wire, audit, and harden AgentMemory for AI coding agents and project workspaces. Use when Codex needs to adopt rohitg00/agentmemory, configure Codex or OpenClaw memory integration, create ClawHub-ready AgentMemory guidance, debug MCP/hook/plugin setup, verify memory capture, or handle edge cases such as npx stalls, sandbox localhost routing, duplicate plugin paths, stale Codex hooks, remote bearer-token security, multi-agent isolation, or missing full-tool proxy mode.
license: MIT
metadata:
  openclaw:
    skillKey: agentmemory-adapter
    homepage: https://github.com/zack-dev-cm/agentmemory-skills
    requires:
      bins:
        - node
        - python3
    envVars:
      - name: AGENTMEMORY_URL
        required: false
        description: Optional AgentMemory REST base URL. Defaults to http://localhost:3111.
      - name: AGENTMEMORY_SECRET
        required: false
        description: Optional bearer secret for protected AgentMemory servers. Never print this value.
      - name: AGENTMEMORY_REQUIRE_HTTPS
        required: false
        description: Set to 1 to refuse sending bearer tokens over non-loopback HTTP.
---

# AgentMemory Adapter

Use this skill to make AgentMemory a dependable shared memory layer, not just a copied MCP snippet.

## When To Use

Use this skill when the user wants to install AgentMemory, wire AgentMemory MCP into Codex or OpenClaw, audit an existing memory setup, publish AgentMemory guidance to ClawHub, or debug memory failures involving `npx`, localhost routing, bearer-token safety, stale hooks, duplicate plugin paths, or degraded MCP fallback mode.

## Operating Order

1. Confirm the target surface: Codex, OpenClaw, ClawHub skill packaging, or a specific project workspace.
2. Read the bundled references for current architecture and platform-specific recipes.
3. Prefer a pinned local AgentMemory binary over long-lived `npx` commands.
4. Apply the narrowest config change that satisfies the target surface, preserving existing user settings.
5. Run the diagnostic script before and after changes, then explain any warnings as operational risks rather than hiding them.
6. For public skill work, run Codex quick validation, ClawHub skill doctor, leak/prompt-bleed scans, ClawPatch review, and a gstack-style ship gate before publishing.

## First Pass

1. Inspect the target agent and project scope before editing config. Prefer user-level integration for "all current projects"; prefer repo-local integration only when the user asks for project-specific behavior.
2. Read `references/agentmemory-deep-analysis.md` for the current AgentMemory architecture and `references/platform-recipes.md` for exact Codex, OpenClaw, and ClawHub-ready patterns.
3. Run `scripts/check_agentmemory.py` before and after changes. Use `--url <base-url>` when the server is remote or uses a non-default port.
4. Preserve existing user config and backups. `agentmemory connect` writes backups under `~/.agentmemory/backups`; manual JSON/TOML edits should be equally scoped.

## Install Strategy

Prefer a stable local command over unbounded `npx` in long-lived MCP configs:

```bash
npm install --prefix ~/.agentmemory/npm @agentmemory/agentmemory@0.9.22 --omit=optional
mkdir -p ~/.local/bin
ln -sfn ~/.agentmemory/npm/node_modules/.bin/agentmemory ~/.local/bin/agentmemory
```

Use full optional dependencies only when the user explicitly needs local vector/image embeddings and accepts native package install cost. If `npx @agentmemory/agentmemory@latest` stalls, install the core package locally as above and point MCP entries at `~/.local/bin/agentmemory mcp`.

## Codex Workflow

1. Wire MCP with the local command:

```bash
codex mcp remove agentmemory 2>/dev/null || true
codex mcp add agentmemory \
  --env AGENTMEMORY_URL=http://localhost:3111 \
  --env AGENTMEMORY_TOOLS=all \
  -- ~/.local/bin/agentmemory mcp
```

2. Install the Codex hook fallback when Codex Desktop or plugin-local hooks are unreliable:

```bash
agentmemory connect codex --with-hooks --force
```

Then re-run the MCP add command above if `connect` rewrites the server back to `npx`.

3. Install the upstream Codex plugin or a local marketplace copy when slash skills are wanted. Patch the plugin `.mcp.json` to the local command if avoiding `npx`.

4. Verify:

```bash
codex mcp list
python3 ~/.codex/skills/agentmemory-adapter/scripts/check_agentmemory.py
```

## OpenClaw Workflow

1. Add the MCP server:

```bash
openclaw mcp set agentmemory '{"command":"'"$HOME"'/.local/bin/agentmemory","args":["mcp"],"env":{"AGENTMEMORY_URL":"http://localhost:3111","AGENTMEMORY_TOOLS":"all"}}'
```

2. Install or link the OpenClaw memory plugin from a durable directory, not a temporary source checkout.
3. Ensure `plugins.slots.memory` is `agentmemory`, `plugins.entries.agentmemory.enabled` is true, and the plugin config includes `base_url`, `token_budget`, `min_confidence`, `fallback_on_error`, and `timeout_ms`.
4. Verify with:

```bash
openclaw mcp show agentmemory
openclaw plugins inspect agentmemory
openclaw plugins doctor
```

## Edge-Case Rules

- Treat MCP fallback mode as degraded: it exposes only a small local tool set when the REST server is unreachable. Start the server for the full tool surface.
- For sandboxed agents, `localhost` may point inside the sandbox. Use a reachable host route and `AGENTMEMORY_FORCE_PROXY=1` only when the route is correct.
- Never send `AGENTMEMORY_SECRET` over non-loopback `http://`. Prefer HTTPS or SSH tunneling; set `AGENTMEMORY_REQUIRE_HTTPS=1` for hard failure.
- Re-run `agentmemory connect codex --with-hooks` after upgrading AgentMemory because user-scope hooks contain absolute script paths.
- Remove duplicate OpenClaw plugin paths; stale temp paths can shadow durable installs.
- Use `AGENT_ID` and `AGENTMEMORY_AGENT_SCOPE=isolated` only when roles need strict separation. Default shared memory is usually better for one user's coding agents.
- Keep `AGENTMEMORY_INJECT_CONTEXT=false` and `AGENTMEMORY_AUTO_COMPRESS=false` unless the user explicitly accepts token spend.
- Do not use `memory_governance_delete` or the `/forget` workflow without explicit confirmation.

## ClawHub-Ready Skill Work

For a skill intended for ClawHub, keep `SKILL.md` concise, declare OpenClaw runtime requirements in `metadata.openclaw`, avoid paid-skill/licensing claims, and include a `--clawscan-note` when publishing because this workflow intentionally configures local binaries, MCP, and network access. Use `references/platform-recipes.md` before publishing or reviewing the bundle.
