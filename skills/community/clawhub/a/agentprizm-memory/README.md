# agentprizm-openclaw

[![AgentPrizm](https://img.shields.io/badge/AgentPrizm-memory%20of%20record-6C47FF)](https://agentprizm.com)
[![License: MIT-0](https://img.shields.io/badge/license-MIT--0-green)](./LICENSE)
[![OpenClaw skill](https://img.shields.io/badge/OpenClaw-skill-000000)](https://agentprizm.com)

**Persistent memory for your OpenClaw agent, powered by [AgentPrizm](https://agentprizm.com).**

This skill teaches your OpenClaw agent *when* and *how* to use long-term memory, and
wires it to AgentPrizm's remote MCP server. Your agent recalls durable facts, decisions,
preferences, lessons, and contacts **before** it acts — and stores new ones as it learns
them — so it stops relearning what it already knew, across sessions, projects, and
machines.

It's a thin, MCP-native skill: a [`SKILL.md`](./SKILL.md) of agent instructions plus the
OpenClaw MCP server config. AgentPrizm already ships the remote server
(`https://agentprizm.com/api/mcp`), so there's nothing to host.

---

## Get your API key

This skill is **bring-your-own-account**: each user supplies their own AgentPrizm key.
Your memories are yours, scoped to your account.

1. Sign up free at **[agentprizm.com](https://agentprizm.com)**.
2. Create an API key (keys are prefixed `ap_`).
3. Set it in your environment:

   ```bash
   export AGENTPRIZM_API_KEY=ap_xxxxxxxxxxxxxxxxxx
   # optional: a default container to scope your memories
   export AGENTPRIZM_CONTAINER=default
   ```

4. Register the key with the skill so OpenClaw marks it ready and exposes it to the
   skill's turns (stored in `~/.openclaw/openclaw.json` under
   `skills.entries.agentprizm-memory.apiKey`):

   ```bash
   openclaw config set skills.entries.agentprizm-memory.apiKey "$AGENTPRIZM_API_KEY"
   ```

   Your key is used in **two** places: the MCP server's `Authorization` header (below)
   authenticates the connection to AgentPrizm, and the skill `apiKey` above lets OpenClaw
   flip the skill from *Needs setup* → *Ready*. Confirm with `openclaw skills info agentprizm-memory`.

See [`.env.example`](./.env.example) for the full list of variables.

---

## 60-second install

**1. Add the remote MCP server.** This probes AgentPrizm before saving, so a success
means your key works. `--include "memory_*"` scopes it to the 8 memory tools
(least-privilege default — all a memory skill needs):

```bash
openclaw mcp add agentprizm-memory \
  --url https://agentprizm.com/api/mcp \
  --transport streamable-http \
  --header "Authorization=Bearer $AGENTPRIZM_API_KEY" \
  --include "memory_*"
```

**2. Install the skill** from this repo (git ref):

```bash
openclaw skills install git:https://github.com/AgentPrizm/agentprizm-openclaw
```

Or, once it's listed on ClawHub (ref is `@owner/slug`):

```bash
openclaw skills install @AgentPrizm/agentprizm-memory
```

That's it. Your agent now recalls before it acts and stores what's durable.

---

## Manual config alternative

If you'd rather set the server in one shot (e.g. to pin a literal key), use `mcp set`.
Note: `mcp set` takes only the **bare per-server object** `{url,transport,headers}` — not
a wrapped config. ([`mcp/openclaw.json`](./mcp/openclaw.json) shows the same server in the
`mcp.servers.<name>` shape it lands as in `~/.openclaw/openclaw.json`; copy only the inner
object into `mcp set`.)

```bash
openclaw mcp set agentprizm-memory '{"url":"https://agentprizm.com/api/mcp","transport":"streamable-http","headers":{"Authorization":"Bearer ap_xxxxxxxxxxxxxxxxxx"}}'
```

> `transport` must be `streamable-http` (the alternative OpenClaw transport is `sse`).

---

## Verify

```bash
openclaw mcp probe          # list AgentPrizm's advertised capabilities/tools
openclaw mcp status         # connection status
openclaw mcp doctor         # diagnose auth/transport issues
openclaw mcp tools          # see the memory_* tools that are exposed
```

With the recommended memory-only setup, a healthy probe shows the **8 memory tools**:
`memory_bootstrap`, `memory_recall`, `memory_context`, `memory_create`, `memory_forget`,
`memory_ingest` / `memory_ingest_url`, `memory_profile`.

**Want the full AgentPrizm surface (memory + skills marketplace)?** AgentPrizm also serves
14 `skill_*` AgentSkills tools (`skill_search`, `skill_get`, `skill_list`, `skill_install`,
`skill_fork`, `skill_publish`, `skill_publish_public`, `skill_update`, `skill_deprecate`,
`skill_unpublish`, `skill_marketplace_search`, `skill_marketplace_get`, `skill_report`,
`skill_appeal`) — 22 tools in all. Opt in by adding the server **without** the `--include`
filter (or widen an existing one with `openclaw mcp tools agentprizm-memory --include "*"`):

```bash
openclaw mcp add agentprizm-memory --url https://agentprizm.com/api/mcp \
  --transport streamable-http --header "Authorization=Bearer $AGENTPRIZM_API_KEY"
```

Other useful commands: `openclaw mcp reload`, `openclaw mcp list`,
`openclaw mcp show agentprizm-memory`, `openclaw mcp unset agentprizm-memory`.

---

## What's in the box (AgentPrizm memory model)

- **8 memory tools (default)** — `memory_bootstrap` (one-shot context),
  `memory_recall` (semantic search), `memory_create`, `memory_forget`, `memory_ingest` /
  `memory_ingest_url`, `memory_context` (token-budgeted block), `memory_profile`
  (per-container summary). The server can also serve 14 `skill_*` AgentSkills tools
  (search, install, fork, publish, marketplace, …) — 22 in all — as an **opt-in**
  (omit `--include "memory_*"`); the recommended setup stays memory-only.
- **6 memory types** — `fact`, `lesson`, `directive`, `preference`, `contact`,
  `bookmark`.
- **Containers** — scope memory by user, team, customer, environment, or agent so
  unrelated work doesn't bleed together.
- **Validity windows** — `validFrom` / `validUntil` let time-sensitive facts expire
  instead of misleading a future session.
- **Confidence** and **recall receipts** — every recall comes with a receipt your agent
  can ground its reasoning in.

The [`SKILL.md`](./SKILL.md) encodes the loop: **recall before you act, store what's
durable, scope it, let time-bound facts expire.**

---

## Per-user key model

There is no shared backend key. Each OpenClaw user brings their **own** AgentPrizm
account and key, and memories are isolated to that account. This skill never ships a key
— the placeholders in this repo (`ap_xxxxxxxxxxxxxxxxxx`) are examples only. Never commit
your real `ap_...` key.

---

## Publishing to ClawHub

ClawHub (the OpenClaw skill registry) publishes via **GitHub import**: it discovers a
`SKILL.md` in a repository that is

- **public**, and
- **not a fork**,

and is published by a **GitHub account at least one week old**. Imported skills are
auto-licensed **MIT-0** (this repo's [`LICENSE`](./LICENSE) matches), and there is no
pricing field. To publish your own variant, fork-free: create a public repo with a
`SKILL.md` at the root and import it from ClawHub.

---

## About

**AgentPrizm** is the memory of record for AI agents — a persistent, semantic memory
layer that any MCP-native agent (like OpenClaw) can plug into. Built by VUGA Enterprises
LLC.

- Website & docs: **https://agentprizm.com**
- This skill: **https://github.com/AgentPrizm/agentprizm-openclaw**
- Integration examples & full Wiki: **https://github.com/AgentPrizm/integration** · **[/wiki](https://github.com/AgentPrizm/integration/wiki)**

## License

[MIT-0](./LICENSE) — MIT No Attribution. Copyright (c) 2026 AgentPrizm (VUGA Enterprises
LLC).
