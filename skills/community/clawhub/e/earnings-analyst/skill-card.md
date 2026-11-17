## Description:

Research upcoming earnings events, analyze historical beat/miss patterns, and estimate post-earnings price reactions using the Finskills API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[finskills](https://clawhub.ai/user/finskills)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, financial analysts, and market researchers use this skill to prepare earnings calendars, per-stock earnings histories, estimate revision summaries, and options-implied move analysis before earnings events.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requests may share tickers, date ranges, and earnings-research context with the Finskills API.

Mitigation: Use an API key with only the required access level and avoid sending confidential trading plans or sensitive account information.

Risk: Earnings dates, options-implied moves, and estimate data can be stale, incomplete, or affected by market liquidity.

Mitigation: Verify earnings dates with company investor-relations sources and treat the skill output as research support rather than a sole basis for trading decisions.

## Reference(s):

- [ClawHub earnings-analyst listing](https://clawhub.ai/finskills/skills/earnings-analyst)
- [Finskills API](https://finskills.net)
- [Skill homepage](https://github.com/finskills/earnings-analyst)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown reports with tables, calculations, and concise narrative analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires FINSKILLS_API_KEY; calendar-only workflows can use the free plan, while full per-stock analysis may require Pro API access.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
