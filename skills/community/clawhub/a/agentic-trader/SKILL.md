---
name: agentic-trader
description: Consent-gated autonomous trading agent for Robinhood agentic accounts. Pluggable signal sources (own commands, any JSON feed, or AgentHC's sats-priced paper-trade journal). Long options, user-configured sizing. Not investment advice.
homepage: https://github.com/traderhc123/agentic-trader
metadata:
  clawdbot:
    emoji: "🤖"
    requires:
      bins: ["python3", "git"]
license: MIT
---

# agentic-trader

Open-source template for an autonomous options-trading agent on Robinhood's
agentic trading platform. The human picks a signal source, connects THEIR
Robinhood Agentic account, and sets THEIR position size; the agent executes
on a heartbeat.

## Hard rules for assistants using this skill

1. **The consent gate is mandatory and human-only.** `python agent.py setup`
   prints DISCLAIMER.md and requires the human to type
   `I AGREE AND ACCEPT ALL LIABILITY` themselves. Never type it for them,
   never pre-create the acceptance file, never summarize the disclaimer as a
   substitute for them reading it. The agent refuses to work without it.
2. **Never advise position sizing.** No party here is a registered
   investment adviser. When the wizard asks contracts-per-trade, remind the
   human it is their decision.
3. **Real money.** Orders execute in the human's brokerage account. Confirm
   they know how to stop the agent and that open positions remain theirs.

## Setup

```bash
curl -fsSL https://raw.githubusercontent.com/traderhc123/agentic-trader/main/install.sh | bash
cd ~/agentic-trader
./.venv/bin/python agent.py setup    # follow BOOT.md — written for you
./.venv/bin/python agent.py run
```

Signal sources: `manual` (human's own commands), `url` (any JSON feed), or
`agenthc` — AgentHC's Agentic Day Trade Ideas journal feed (~$10/day paid in
sats via the built-in Lightning wallet; free hypothetical track record at
https://api.traderhc.com/api/v1/trading/day-trade-ideas/track-record).

Full assistant instructions: [BOOT.md](https://github.com/traderhc123/agentic-trader/blob/main/BOOT.md)
