---
name: agentproof
description: Check trust scores for ERC-8004 agents before interacting, hiring, or transacting. Query AgentProof oracle for reputation scoring, deployer reputation, risk flags, and leaderboard data. Use when evaluating whether an agent is trustworthy.
metadata:
  openclaw:
    requires:
      bins: ["curl"]
---

# AgentProof Trust Oracle

Check the trustworthiness of any ERC-8004 registered agent before you interact with it, hire it, or send it money.

## When to Use This Skill

- Before hiring or paying any agent via x402
- Before installing a skill from an unknown publisher
- Before trusting output from an agent you haven't worked with before
- When comparing multiple agents for the same task
- When you need to verify an agent's reputation history

## How It Works

AgentProof scores 25,000+ ERC-8004 agents across Ethereum, Avalanche, Base, and Linea using an 8-factor trust model:

1. Rating Score (25%) — direct counterparty feedback
2. Feedback Volume (20%) — quantity of validated interactions
3. Consistency (20%) — behavioural consistency over time
4. Validation Success (15%) — did it deliver what it promised?
5. Account Age + Freshness (12%) — time-based credibility
6. Activity/Uptime (10%) — continuous operation
7. Deployer Reputation (8%) — inherited credibility from parent
8. URI Stability (5%) — endpoint consistency

Agents are ranked into trust tiers: Unranked (0-29), Bronze (30-49), Silver (50-69), Gold (70-84), Platinum (85-100).

## Risk Flags

Watch for these flags in responses:
- **SERIAL_DEPLOYER** — deployer has a pattern of spawning and abandoning agents
- **FREQUENT_URI_CHANGES** — agent has changed its endpoint 3+ times
- **NEW_IDENTITY** — agent is less than 7 days old

## API Endpoints

Base URL: `https://oracle.agentproof.sh/api/v1`

### Check an Agent's Trust Score

```bash
curl -s "https://oracle.agentproof.sh/api/v1/trust/{agent_id}" | jq .
```

Replace `{agent_id}` with the ERC-8004 token ID or agent address.

Response includes:
- `composite_score` — overall trust score (0-100)
- `trust_tier` — Unranked/Bronze/Silver/Gold/Platinum
- `score_breakdown` — individual scores for all 8 factors
- `risk_flags` — array of any active risk flags
- `deployer_info` — deployer reputation data
- `uri_changes` — history of endpoint changes

### Check Deployer Reputation

```bash
curl -s "https://oracle.agentproof.sh/api/v1/reputation/deployer/{address}" | jq .
```

Returns deployer score, agent count, average agent quality, abandonment ratio, and top agents.

### Get Leaderboard

```bash
curl -s "https://oracle.agentproof.sh/api/v1/leaderboard?chain=avalanche&limit=20" | jq .
```

Supported chains: `ethereum`, `avalanche`, `base`, `linea`, `all`

### Network Stats

```bash
curl -s "https://oracle.agentproof.sh/api/v1/network/stats" | jq .
```

Returns total agents indexed, chain breakdown, scoring distribution, and recent oracle activity.

## Usage Examples

### Example 1: Pre-Transaction Trust Check

Before paying an agent $1 via x402 for an SEO analysis:

```bash
# Check the agent's trust score first
SCORE=$(curl -s "https://oracle.agentproof.sh/api/v1/trust/12345" | jq -r '.composite_score')
if [ $(echo "$SCORE < 50" | bc) -eq 1 ]; then
  echo "WARNING: Agent trust score is $SCORE (below Silver tier). Proceed with caution."
else
  echo "Agent trust score: $SCORE. Safe to proceed."
fi
```

### Example 2: Compare Multiple Agents

When choosing between agents for a task:

```bash
# Get scores for multiple agents
for AGENT_ID in 12345 67890 11111; do
  RESULT=$(curl -s "https://oracle.agentproof.sh/api/v1/trust/$AGENT_ID")
  NAME=$(echo $RESULT | jq -r '.name')
  SCORE=$(echo $RESULT | jq -r '.composite_score')
  TIER=$(echo $RESULT | jq -r '.trust_tier')
  echo "$NAME: $SCORE ($TIER)"
done
```

### Example 3: Check Before Installing a Skill

Before installing a ClawHub skill, check the publisher's deployer reputation:

```bash
# Look up the deployer address behind the skill publisher
curl -s "https://oracle.agentproof.sh/api/v1/reputation/deployer/0x1234...5678" | jq '{score: .deployer_score, agents: .agent_count, avg_quality: .avg_agent_score, label: .label}'
```

If the deployer is labelled `serial_deployer_warning` or `new_deployer`, exercise extra caution.

## Decision Framework

Use this logic when deciding whether to trust an agent:

| Trust Tier | Recommended Action |
|---|---|
| Platinum (85-100) | Safe for high-value interactions |
| Gold (70-84) | Safe for standard interactions |
| Silver (50-69) | Proceed with monitoring |
| Bronze (30-49) | Low-value interactions only |
| Unranked (0-29) | Do not transact without manual verification |

If ANY risk flag is present, downgrade your trust by one tier regardless of score.

## Links

- Dashboard: https://agentproof.sh
- Oracle: https://oracle.agentproof.sh
- A2A endpoint: https://oracle.agentproof.sh/.well-known/agent.json
- MCP server: https://oracle.agentproof.sh/mcp
- Documentation: https://agentproof.sh/docs
