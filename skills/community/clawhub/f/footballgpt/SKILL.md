---
name: footballgpt
description: AI football coaching assistant. Generate session plans, animate drills, get coaching advice, search player stats, and search drill databases. Use when a user asks about football training sessions, drills, coaching tactics, player development, match preparation, or player statistics. Requires a FootballGPT API key.
homepage: https://www.footballgpt.co
metadata:
  {
    "openclaw":
      {
        "emoji": "⚽",
        "requires": { "bins": ["mcporter"], "env": ["FOOTBALLGPT_API_KEY"] },
        "primaryEnv": "FOOTBALLGPT_API_KEY",
        "install":
          [
            {
              "id": "node",
              "kind": "node",
              "package": "mcporter",
              "bins": ["mcporter"],
              "label": "Install mcporter (npm)",
            },
          ],
      },
  }
---

# FootballGPT

AI football coaching assistant based on FA, UEFA, and FIFA coaching methods.

## Setup

1. Subscribe at [footballgpt.co](https://www.footballgpt.co) ($10.99/month)
2. Add API bolt-on ($4.99/month) at [footballgpt.co/app/mcp](https://www.footballgpt.co/app/mcp)
3. Generate an API key from the dashboard
4. Set `FOOTBALLGPT_API_KEY` as an environment variable:

```bash
export FOOTBALLGPT_API_KEY="fgpt_your_key_here"
```

5. Register the MCP server with mcporter:

```bash
mcporter config add footballgpt https://footballgpt.co/api/mcp/stream \
  --header "Authorization=Bearer $FOOTBALLGPT_API_KEY" \
  --description "AI football coaching assistant" \
  --scope home
```

6. Verify the connection:

```bash
mcporter list footballgpt --schema
```

## MCP Server

FootballGPT exposes tools via a streamable-http MCP endpoint at `https://footballgpt.co/api/mcp/stream`.

Once registered with mcporter, call tools directly:

```bash
mcporter call footballgpt.get_coaching_advice message="How do I set up a 4-3-3 high press for U14s?"
```

```bash
mcporter call footballgpt.generate_session_plan topic="defensive shape" age_group="u12" duration=60
```

```bash
mcporter call footballgpt.animate_drill description="passing triangle, one-touch" category="passing"
```

## Tools

| Tool | Description |
|------|-------------|
| `get_my_profile` | Loads your team, squad, formation, and coaching priorities |
| `get_coaching_advice` | Coaching advice for any scenario (tactics, drills, player development, match prep) |
| `generate_session_plan` | Complete training session plan with warm-up, main activities, and cool-down |
| `animate_drill` | Animated drill diagrams with player movements and ball paths (saved to your account) |
| `search_player_stats` | Real player statistics across 60+ leagues |
| `search_drills` | Search the drill database for specific activities |

## Usage Limits

- 100 API calls/day (resets midnight UTC)
- 10 animate_drill calls/day
- Maximum 3 active API keys

## Examples

- "Create a 60-minute session on defensive shape for 9v9"
- "How do I coach a diamond midfield in a 4-4-2?"
- "Animate a passing drill with 3 players in a triangle, one-touch passing"
- "Show me top Premier League scorers this season"
- "Find rondo drills for U12s"

## Links

- Website: [footballgpt.co](https://www.footballgpt.co)
- API docs: [Notion](https://kevinrmiddleton.notion.site/FootballGPT-API-Documentation-31ad14ad204281eb97c4c3427e94a2e1)
- Features: [footballgpt.co/features/api-access](https://www.footballgpt.co/features/api-access)
- ClawHub: [clawhub.ai/360tft/footballgpt](https://clawhub.ai/360tft/footballgpt)
