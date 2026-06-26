# 🚪 Doorstep

**Get things done in the real world from your AI assistant.**

Pickups, deliveries, errands, gifts — describe what you need and a human tasker in San Francisco will do it.

> **Coverage: San Francisco only.** Doorstep dispatches local taskers across SF. Tasks outside San Francisco are not supported.

## How It Works

1. Tell your AI assistant what you need done in the physical world
2. Doorstep researches the request and returns a plan with pricing
3. You approve the quote — a tasker heads out and gets it done
4. Track progress and message your tasker in real time

## Examples

- "Pick up my prescription from Walgreens on Divisadero and bring it to my apartment"
- "Deliver a dozen roses to 456 Oak St in SF"
- "Grab coffee from Blue Bottle on Mint Plaza and bring it to my office"
- "Buy a birthday card near Union Square and drop it off at 789 Folsom"
- "Pick up my dry cleaning from the spot on Valencia"

## Pricing

Tasks start at **$5 labor** plus pass-through costs for any purchases at cost. You always see the full breakdown before approving — no surprise charges.

| Tier | Labor Cost | Best For |
|------|-----------|----------|
| Quick | $5 | Simple pickups, single-stop errands |
| Standard | $10 | Multi-stop runs, purchases with selection |
| Complex | $20 | Time-intensive tasks, multiple locations |

## Setup

### npx bridge (default for OpenClaw)

1. [Generate an API key](https://trydoorstep.app/dashboard/api-keys) (sign in first).
2. Add the Doorstep MCP server to your configuration:

```json
{
  "mcpServers": {
    "doorstep": {
      "command": "npx",
      "args": ["-y", "doorstep"],
      "env": {
        "DOORSTEP_API_KEY": "${DOORSTEP_API_KEY}"
      }
    }
  }
}
```

### HTTP (alternative)

For MCP clients that support HTTP transport (e.g. Claude Desktop):

```json
{
  "mcpServers": {
    "doorstep": {
      "url": "https://trydoorstep.app/mcp"
    }
  }
}
```

On first use you'll be prompted to log in via your browser. No API key needed.

## Safety

- You always see and approve the quote before anything is charged
- Your card on file is only billed the quoted amount
- Account and billing status can be checked at any time

## Links

- **Website**: [trydoorstep.app](https://trydoorstep.app)
