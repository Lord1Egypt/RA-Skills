# GameLegend — OpenClaw Skill

Game discovery and recommendations for your OpenClaw agent, powered by GameLegend's Gameplay DNA engine.

Your agent can find similar games, recommend titles based on gameplay feel, and build a taste profile of your preferences — all through natural conversation on WhatsApp, Telegram, Discord, or any connected messaging platform.

## What It Does

- **"Games like Civilization VI"** — finds similar games ranked by 69-dimension DNA similarity
- **"What should I play?"** — asks about your mood and preferences, then matches games by gameplay feel
- **"Tell me about Stardew Valley"** — shows a game's full DNA profile with standout traits
- **Learns your taste** — remembers what you like and proactively suggests games that fit

## Installation

### From ClawHub

```bash
clawhub install gamelegend
```

### Manual Install

Copy the `SKILL.md` file to your OpenClaw skills directory:

```bash
mkdir -p ~/.openclaw/skills/gamelegend
cp SKILL.md ~/.openclaw/skills/gamelegend/
```

Or add it as a workspace skill:

```bash
mkdir -p ./skills/gamelegend
cp SKILL.md ./skills/gamelegend/
```

Restart your OpenClaw instance to pick up the new skill.

## Configuration

No configuration needed. The GameLegend API is public and requires no authentication.

## API

This skill uses the [GameLegend Public API](https://gamelegend.com/docs/api):

| Endpoint | Description |
|----------|-------------|
| `GET /api/v1/games` | Search games by title or gameplay dimensions |
| `GET /api/v1/games/{slug}` | Full game details with DNA profile |
| `GET /api/v1/games/{slug}/similar` | Similar games by DNA cosine similarity |
| `GET /api/v1/dimensions` | All 69 gameplay dimensions |

Rate limit: 100 requests/minute. No API key required.

## About Gameplay DNA

GameLegend analyzes games across 69 dimensions of gameplay feel, grouped into 9 categories:

- **Mechanics** — core systems (turn-based, deck building, base building, etc.)
- **Feel** — pacing and mood (meditative, frantic, cozy, etc.)
- **Progression** — how advancement works (linear story, roguelike loops, etc.)
- **Social Mode** — multiplayer styles (solo, co-op, competitive, etc.)
- **Aesthetic** — visual style (pixel art, photorealistic, etc.)
- **Themes** — narrative content (existential dread, wholesome, etc.)
- **Complexity** — depth level (pick-up-and-play to spreadsheet-deep)
- **Session Length** — typical play sessions
- **Strategic Scope** — scale of decisions

## Links

- [GameLegend](https://gamelegend.com) — game discovery engine
- [API Documentation](https://gamelegend.com/docs/api)
- [MCP Server](https://www.npmjs.com/package/@gamelegend/mcp) — for Claude Code, Cursor, and other MCP clients
