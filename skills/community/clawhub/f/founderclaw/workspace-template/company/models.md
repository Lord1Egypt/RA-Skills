# Models — FounderClaw

Configure your model tiers during install.

## Tiers

| Tier | Purpose | Example |
|---|---|---|
| Fast | Quick tasks, mechanical work | openrouter/anthropic/claude-haiku-4 |
| Best | Strategy, deep thinking, orchestration | openrouter/anthropic/claude-sonnet-4 |
| Vision | Image analysis | openrouter/xiaomi/mimo-v2-omni |

## Assignment

| Agent | Tier |
|---|---|
| FounderClaw Main (CEO) | Best |
| Strategy | Best |
| Shipper | Fast |
| Tester | Vision |
| Safety | Fast |
| Observer | Best |

## Notes

- If you only have one model, all agents use that model
- Vision is used via sub-agent spawning, not as a primary model
- You can override per agent in the OpenClaw config
