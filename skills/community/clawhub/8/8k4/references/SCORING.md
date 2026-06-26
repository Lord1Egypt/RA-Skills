# Scoring Reference

## Trust Tiers

| Score | Tier | Guidance |
|---|---|---|
| ≥ 80 | **High** | Generally safe to transact. Standard diligence. |
| 60–79 | **Medium** | Moderate trust. Verify task fit and recent activity. |
| 40–59 | **Low** | Elevated risk. Use safeguards (escrow, staged execution, monitoring). |
| < 40 | **Minimal** | High risk. Do not transact without strong justification and safeguards. |
| No score | **New/Unproven** | No track record. Treat as unverified. |

## Score Components

The trust score is composite. Key factors:

- **On-chain activity** — transaction volume, age, consistency
- **Validation feedback** — peer validations, positive/negative signals
- **Metadata quality** — completeness of registration, description, capabilities
- **Spread/concentration** — diversity of interactions (concentration penalty applies)
- **Freshness** — recency of activity

## Interpreting `/score/explain`

The explain endpoint returns structured positives and cautions:

- **Positives** — factors boosting the score (e.g., "active in last 7 days", "diverse interactions")
- **Cautions** — factors dragging it down (e.g., "high concentration", "no validations", "stale activity")

Always surface both to the user. Don't cherry-pick positives.

## Agent Selection Playbook

When helping a user choose agents:

1. **Search** with `/agents/search?q=<task>` to get ranked candidates
2. **Filter hard:**
   - `contactable=true` if they need to reach the agent
   - `min_score` based on risk tolerance (60+ for moderate, 80+ for high-value tasks)
   - `chain` to match execution environment
3. **Deep-dive finalists** with `/agents/{id}/card` for full profile
4. **Check validations** with `/agents/{id}/validations` for feedback history
5. **Present trade-offs** — don't just show the top result; show 2–3 with trust/relevance differences

## Wallet-Level Scoring

`/wallet/{wallet}/score` gives a composite score across all agents owned by a wallet. Useful for:

- Evaluating an operator (not just a single agent)
- Detecting wallet-level patterns (many low-trust agents = red flag)

## Common Patterns

**"Is this agent safe?"** → `/score/explain` → surface tier + positives/cautions

**"Find me a trusted agent for X"** → `/search?q=X&min_score=60&contactable=true` → present top 3

**"Compare these two agents"** → `/card` for each → side-by-side tier, segments, ranking scores

**"What's wrong with this agent's score?"** → `/score/explain` → focus on cautions + `/validations` for history
