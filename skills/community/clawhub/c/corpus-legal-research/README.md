# corpus-legal-research — Agent Skill

A portable [Agent Skill](https://agentskills.io/specification) that teaches any
skill-capable agent to search current US federal, state, and municipal law
through [Corpus](https://corpuslaw.us), using the hosted MCP server at
`https://corpuslaw.us/api/mcp`.

This is the research skill. Formation intake lives in
`skills/corpus-business-formation/`.

## Install

Copy the `corpus-legal-research/` directory into wherever your agent reads skills:

| Harness | Path |
|---|---|
| Claude Code | `~/.claude/skills/` or `.claude/skills/` |
| Cursor | `.agents/skills/` or `.cursor/skills/` |
| VS Code / Copilot | `.github/skills/`, `.claude/skills/`, or `.agents/skills/` |
| Hermes | `~/.hermes/skills/` |
| OpenAI Codex | per `learn.chatgpt.com/docs/build-skills` |

Then connect the MCP server — see
`../corpus-business-formation/references/harness-setup.md`.

Hermes can also install both skills plus the MCP URL as one Agent Plugins v1
package:

```bash
hermes plugins install teakesdev/corpus-agent-kit/plugins/corpus
hermes plugins enable corpus
```

## Why a skill and not just the MCP server

The MCP server's own instructions only reach an agent **after** the user has
already connected Corpus. A skill's `description` loads at startup, so an agent
that has never heard of Corpus still knows to reach for live search when its
user asks what US law currently says.

## Distribution note

This is the canonical copy. The Hermes plugin at `plugins/corpus/` ships a
generated copy of this skill; edit here, then run
`scripts/check-plugin-skill-drift.sh --write`.

Apache-2.0.
