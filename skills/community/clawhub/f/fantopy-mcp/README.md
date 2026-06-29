# Fantopy MCP OpenClaw Skill

Fantopy MCP is a free-to-play World Cup prediction companion for human players.
It lets an OpenClaw agent help a user browse fixtures, save score predictions,
create groups, check standings, and share a public watch link through Fantopy's
MCP tools.

## Listing Copy

Use this copy for ClawHub or other OpenClaw skill listings:

```text
Fantopy MCP helps OpenClaw users play Fantopy's free-to-play World Cup
prediction game from an AI assistant. Connect the Fantopy MCP server, start a
session, choose a handle, make confirmed score picks, create groups, and share a
public watch link.
```

Short description:

```text
Free-to-play World Cup prediction companion for MCP-capable agents.
```

Suggested tags:

```text
sports, football, world-cup, predictions, mcp, games
```

Safety positioning:

```text
Fantopy is free-to-play. No wagers, no entry fees, no cash prizes, and no crypto
rewards.
```

## OpenClaw Install

Connect the production MCP server:

```bash
openclaw mcp add fantopy --url https://mcp.fantopy.ai/mcp --transport streamable-http --auth oauth --oauth-scope play --timeout 30
openclaw mcp login fantopy
openclaw mcp probe fantopy --json
```

Install this skill from a local checkout:

```bash
openclaw skills install /absolute/path/to/fantopy-mcp/skills/fantopy-mcp --as fantopy-mcp
openclaw skills check
```

The install source root must be this directory because OpenClaw expects
`SKILL.md` at the root of the skill being installed. If publishing to ClawHub,
publish this directory as the skill package root.

## MCP Connection

Hosted production MCP:

```text
MCP URL: https://mcp.fantopy.ai/mcp
Authentication: OAuth
```

Use OAuth, not no-auth. Hosted Fantopy uses guest OAuth to keep one anonymous
player attached to the user's tool calls.

OpenClaw 2026.6.8 was verified against this hosted MCP with OAuth and listed all
48 Fantopy tools. If the OpenClaw release being used cannot attach to a hosted
remote MCP with OAuth, use the local stdio fallback documented in
`docs/OPENCLAW.md`.

## First Prompt

After the MCP connection is active:

```text
Use Fantopy to start my World Cup prediction session.
```

The assistant should call `start_fantopy`, set or ask for a public handle, and
share the returned watch URL.

## Publish Checklist

- Verify the skill metadata with the OpenClaw CLI from this directory.
- Confirm the published package root contains `SKILL.md` and this `README.md`.
- Use the production MCP URL in public listings.
- Keep the dev MCP URL only for sandbox testing.
- State that OpenClaw 2026.6.8+ has been verified with hosted OAuth MCP.
- Include the local stdio fallback for clients without remote MCP OAuth.
- Avoid gambling, betting, cash-prize, crypto, and financial language.
