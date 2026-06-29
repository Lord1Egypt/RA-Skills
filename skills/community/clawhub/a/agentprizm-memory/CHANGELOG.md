# Changelog

All notable changes to this skill are documented here. This project adheres to
[Semantic Versioning](https://semver.org/).

## 1.2.0 — Memory-only by default (least privilege)

- **Default tool surface is now memory-only.** The recommended install scopes the MCP
  server with `--include "memory_*"` (8 memory tools), and `mcp/openclaw.json` carries the
  matching `toolFilter.include`. The 14 `skill_*` AgentSkills-marketplace tools are now an
  explicit opt-in (wire the server without the `--include` filter) rather than exposed by
  default — addresses a ClawHub scan note that a *memory* skill shouldn't hand the agent
  marketplace powers it doesn't need. No change to AgentPrizm or the memory tools
  themselves; this only narrows the recommended default.

## 1.1.0 — Recall receipts & confidence

- **`SKILL.md`** — recall now surfaces a per-memory `confidence` (0–1) and a `why` block
  (including `validityState`); the skill instructs the agent to lean on high-confidence,
  `active` memories and verify the rest. Documents that expired facts are excluded from
  recall by default, with `includeExpired: true` to review them. No config changes.

## 1.0.0 — Initial release

- **`SKILL.md`** — agent instructions teaching when to recall (before starting a task,
  answering, or writing code) and when to store (durable facts, lessons, directives,
  preferences, contacts, bookmarks), how to pick a memory type, how to scope with
  containers, how to use validity windows for time-sensitive facts, and the rule never
  to store secrets. Includes a worked example.
- **`mcp/openclaw.json`** — OpenClaw MCP server config wiring the `agentprizm-memory`
  remote server (`https://agentprizm.com/api/mcp`, `streamable-http`, Bearer auth).
- **`README.md`** — 60-second install, per-user API key model, manual config, probe
  verification, and ClawHub publishing notes.
- **`.env.example`**, **`LICENSE`** (MIT-0).
