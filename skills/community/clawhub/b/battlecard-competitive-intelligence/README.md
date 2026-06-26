# Battlecard: Competitive Intelligence for OpenClaw

Know your competitor's weaknesses before the call starts. Practice your pitch against an AI buyer who fights back. Capture what you learn after every deal.

## Try it now

```bash
./scripts/get_battle_card.sh "YourCompany" "Competitor"
```

No API key needed. No signup. Free tier gives you 4 battle cards, 2 text simulations, and 1 voice simulation.

## What you get

### Before the call
- **Battle cards** - strengths, weaknesses, positioning strategy, objection handlers, and pricing comparison for any company vs any competitor
- **Multi-competitor comparison** - side-by-side matrix for up to 5 competitors in one query
- **Pre-call briefings** - focused preparation docs combining battle card data with field intelligence for a specific upcoming meeting

### During the call
- **Text simulations** - practice selling against an AI prospect who uses real competitor data to challenge you. Get scored on objection handling, positioning, discovery, and closing
- **Voice simulations** - same as above, but the prospect talks back with a real voice. Audio responses you can play in Telegram, Slack, or any client that supports audio

### After the call
- **Capture call intelligence** - paste your call notes, the AI extracts competitor mentions, objections, pricing data, and stores it (Pro+)
- **Field intelligence** - aggregate patterns from real sales conversations across all users. Most common objections, win/loss reasons, pricing trends (Team)

## Example prompts

"Get me a battle card for Notion vs Confluence"

"I have a demo tomorrow against HubSpot. The prospect is a 200-person fintech company. Prep me."

"Start a simulation selling Datadog against New Relic. Medium difficulty."

"Extract the competitive intel from these call notes: [paste notes]"

"What are the most common objections when selling against Salesforce?"

## Pricing

| | Free | Starter $49/mo | Pro $99/mo | Team $149/mo |
|---|---|---|---|---|
| Battle cards | 4 lifetime | 50/day | 500/day | 2,000/day |
| Text simulations | 2 lifetime | 5/day | 20/day | Unlimited |
| Voice simulations | 1 lifetime | 3/day | 15/day | Unlimited |
| Capture intelligence | - | - | Yes | Yes |
| Field intelligence | - | - | - | Yes |

Free tier requires no signup and no API key.

## Setup

### Quick start (no config needed)

```bash
clawhub install battlecard-competitive-intelligence
```

Then run any script in the `scripts/` folder directly.

### MCP configuration (for full access)

Get your API key at [battlecard.northr.ai/signup](https://battlecard.northr.ai/signup), then add to your MCP config:

```json
{
  "mcpServers": {
    "battlecard": {
      "url": "https://battlecard.northr.ai/mcp",
      "headers": {
        "X-Battlecard-Key": "bc_live_your_key_here"
      }
    }
  }
}
```

## All 11 tools

| Tool | What it does | Tier |
|---|---|---|
| get_battle_card | Compare two companies | Free |
| compare_competitors | Multi-competitor matrix (up to 5) | Free |
| get_objection_handlers | Rebuttals for a specific competitor | Free |
| generate_pre_call_briefing | Preparation doc for an upcoming meeting | Pro+ |
| start_simulation | Begin a text-based sales simulation | Free (2) |
| continue_simulation | Send your response during a text simulation | - |
| end_simulation | Finish simulation and get scored | - |
| start_simulation_voice | Begin a voice simulation (audio responses) | Free (1) |
| continue_simulation_voice | Send response, get audio reply | - |
| capture_call_intelligence | Extract intel from call notes | Pro+ |
| get_field_intelligence | Aggregate patterns from real conversations | Team |

Full docs: [battlecard.northr.ai/connect](https://battlecard.northr.ai/connect)

Built by [Northr AI](https://battlecard.northr.ai)
