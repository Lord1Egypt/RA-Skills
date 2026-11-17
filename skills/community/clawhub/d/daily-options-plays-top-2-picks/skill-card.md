## Description:

Build a simple stock-options watchlist and paper-trade plan after the first 15 minutes of the market session.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jrmerced1292-commits](https://clawhub.ai/user/jrmerced1292-commits)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to create a concise daily options watchlist and paper-trade plan after the first 15 minutes of the U.S. market session. It is aimed at beginner-friendly planning with two ranked trade ideas, clear levels, contract guidance, and explicit risk reminders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may produce incorrect or stale market, options-chain, liquidity, or risk-level guidance if the agent lacks current reliable data.

Mitigation: Confirm market data, options chains, liquidity, and risk levels independently before acting on any plan.

Risk: Users could treat educational watchlist output as automatic trading advice.

Mitigation: Use the output as paper-trading market planning only, and do not grant brokerage credentials or live execution authority unless a separate trusted tool handles that with explicit consent.

## Reference(s):

- [Beginner Options Watchlist Framework](references/watchlist-framework.md)
- [Listing Copy](references/listing-copy.md)
- [ClawHub skill page](https://clawhub.ai/jrmerced1292-commits/skills/daily-options-plays-top-2-picks)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Concise watchlist output with market tone, macro or news context, up to two plays, risk notes, and a paper-trade reminder.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
