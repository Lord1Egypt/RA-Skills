## Description:

Research Polymarket market identity, resolution rules and bounded order-book depth without placing orders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[galleonlabs](https://clawhub.ai/user/galleonlabs)

### License/Terms of Use:

MIT

## Use Case:

Researchers and developers use this skill to identify a Polymarket question and outcome, check its resolution criteria, and assess time-bounded hypothetical liquidity using public market data without trading or a signing key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stale or unknown market data may be mistaken for a current quote.

Mitigation: Check provider and retrieval timestamps, reject stale or unknown quotes, and present depth only as hypothetical research.

Risk: Research may be mistaken for authorization to trade or supply credentials.

Mitigation: Use public read-only data; do not provide private keys or run wallet, approval, trading, proposal, dispute or redemption commands.

Risk: Ambiguous outcome identity or resolution rules can lead to misleading conclusions.

Mitigation: Verify the market version, exact outcome identifier and resolution source; state unresolved gaps rather than presenting a tradable price.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/galleonlabs/skills/galleon-prediction-market-research)
- [Polymarket market discovery documentation](https://docs.polymarket.com/market-data/discover-markets)
- [Polymarket prices and order books documentation](https://docs.polymarket.com/market-data/prices-order-books)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown research summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes market and outcome identifiers, dated observations, resolution criteria, hypothetical depth and material uncertainties; not an executable quote.]

## Skill Version(s):

0.1.1 (source: frontmatter and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
