## Description:

Monitor watchlist tickers for price changes, IV rank movement, unusual options activity, upcoming earnings, and score changes with support for custom lists and a default hot options list.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clementgu](https://clawhub.ai/user/clementgu)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to view and manage an AlphaGBM-style ticker watchlist, summarize active alerts, and track price, volatility, options-flow, and earnings signals for selected symbols.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Add and remove commands can change a saved ticker watchlist.

Mitigation: Review requested watchlist changes before execution and confirm ticker removals when the agent has not already asked.

Risk: Watchlist alerts and quick actions can affect trading decisions.

Mitigation: Treat generated summaries and suggested actions as informational support and verify market data and trade suitability before acting.

## Reference(s):

- [AlphaGBM](https://alphagbm.com)
- [ClawHub skill page](https://clawhub.ai/clementgu/skills/alphagbm-watchlist)
- [Publisher profile](https://clawhub.ai/user/clementgu)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown or plain text summaries with watchlist dashboards, alert lists, daily summaries, and suggested quick actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe add, remove, bulk-add, list, alert, and hot-options watchlist operations.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
