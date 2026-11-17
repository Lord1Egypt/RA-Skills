## Description:

Get real-time stock, ETF, and crypto prices. Compare tickers, check market cap and volume. Uses Yahoo Finance - no API key required.

This skill is ready for commercial/non-commercial use.

## Publisher:

[josephflu](https://clawhub.ai/user/josephflu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to fetch current stock, ETF, and crypto quotes, compare multiple tickers, and inspect market state, volume, market cap, and 52-week range data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Ticker symbols requested by the user are sent to Yahoo Finance when quotes are fetched.

Mitigation: Use only when sharing requested ticker symbols with Yahoo Finance is acceptable.

Risk: Python dependencies are resolved at runtime when the command is run with uv.

Mitigation: Pin and review dependency versions before use in stricter environments.

Risk: Remote quote metadata is rendered in terminal Rich markup.

Mitigation: Escape ticker and remote metadata before rendering in environments where terminal markup injection is a concern.

## Reference(s):

- [Common Tickers Quick Reference](references/common-tickers.md)
- [ClawHub Skill Page](https://clawhub.ai/josephflu/skills/eagerbots-stock-quote)
- [Publisher Profile](https://clawhub.ai/user/josephflu)
- [Project Homepage](https://github.com/josephflu/clawhub-skills)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Terminal text with Rich panel or comparison table output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fetches quote data from Yahoo Finance and can report not-found or fetch-failed ticker results.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
