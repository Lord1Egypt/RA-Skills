# corpus-business-formation — Agent Skill

A portable [Agent Skill](https://agentskills.io/specification) that teaches any
skill-capable agent to form a US LLC or nonprofit through
[Corpus](https://corpuslaw.us), using the hosted MCP server at
`https://corpuslaw.us/api/mcp`.

## Install

On Hermes it is one line — no clone, no copy:

```bash
hermes skills install https://corpuslaw.us/skills/corpus-business-formation/SKILL.md
```

Or by well-known identifier, which resolves through
`https://corpuslaw.us/.well-known/skills/index.json` and so survives a move of
the static files:

```bash
hermes skills install well-known:https://corpuslaw.us/.well-known/skills/corpus-business-formation
```

For harnesses with no installer, copy the `corpus-business-formation/` directory
into wherever your agent reads skills:

| Harness | Path |
|---|---|
| Claude Code | `~/.claude/skills/` or `.claude/skills/` |
| Cursor | `.agents/skills/` or `.cursor/skills/` |
| VS Code / Copilot | `.github/skills/`, `.claude/skills/`, or `.agents/skills/` |
| OpenAI Codex | per `learn.chatgpt.com/docs/build-skills` |

Connecting the MCP server is **optional** — the skill runs the intake over plain
HTTP when no connector is present. To add it anyway, see
`references/harness-setup.md`.

## Why a skill and not just the MCP server

The MCP server's own instructions are excellent, but they only reach an agent **after** the
user has already connected Corpus. A skill's `description` loads at startup, so an agent
that has never heard of Corpus still knows to reach for it when its user says
"help me start a company."

The two compose: the skill gets the agent to connect; the server's instructions take over
from there.

Hermes can also install this skill plus `corpus-legal-research` and the MCP URL
as one Agent Plugins v1 package:

```bash
hermes plugins install teakesdev/corpus-agent-kit/plugins/corpus
hermes plugins enable corpus
```

## Distribution note

`SKILL.md` and `references/` here are a **one-way mirror** of the Corpus monorepo
(`packages/skills/corpus-business-formation/`) and are not edited in this repo —
a fix belongs upstream first, then comes back down as a re-mirror. This README is
the exception: it describes *this* repo, so it lives here.

The Hermes plugin at `plugins/corpus/` ships a generated copy of the skill (the
mirrored bytes plus a provenance stamp). After a re-mirror, run
`scripts/check-plugin-skill-drift.sh --write`.

Apache-2.0.
