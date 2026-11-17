## Description:

Research public casino game catalogs and source-published game descriptions from FanDuel and DraftKings. Use for game-category or feature lookups, not wagering strategy or recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

People looking up public casino game information can use this skill to browse FanDuel categories and listed game attributes, along with selected DraftKings slot categories and written guides. It presents source-listed details without recommending games, bets, strategies, or expected returns.

### Deployment Geography for Use:

Global; FanDuel catalog coverage is limited to the Michigan and Ontario lobbies, while DraftKings coverage is limited to the documented public pages.

## Known Risks and Mitigations:

Risk: Lookup parameters are sent to Crawlora, and API use can consume service credits.

Mitigation: Use a dedicated Crawlora API key, limit requests to the public catalog information needed, and do not include casino logins or personal account information.

Risk: Source-reported game attributes, especially volatility, could be mistaken for probabilities or predictions.

Mitigation: Keep attributes attributed to their source and state that volatility is not a probability or a forecast of an outcome.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/crawlora-org/skills/casino-game-research)
- [Endpoint reference](reference/endpoints.md)
- [Crawlora API](https://api.crawlora.net/api/v1)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Concise informational text or Markdown summaries of source-listed casino game categories and attributes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves provider, region, studio, category, badge, and observation time when available; reports source limitations.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
