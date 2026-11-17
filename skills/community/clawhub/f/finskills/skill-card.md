## Description:

Finskills gives agents real-time financial data API access for stock quotes, OHLCV history, fundamentals, macro indicators, commodities, SEC filings, and financial news used in systematic investment research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[finskills](https://clawhub.ai/user/finskills)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to connect an agent to the Finskills API for factual financial research, including stock screening, factor analysis, macro overlays, filings research, and market risk review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installer examples can fetch mutable remote instructions into persistent agent rule files.

Mitigation: Review the packaged SKILL.md before installation and prefer the packaged local file over curl-based installation from a mutable URL.

Risk: The skill requires a Finskills API key for requests.

Mitigation: Use a revocable API key, avoid hardcoding it in shared files, and rotate it if it is exposed.

Risk: Financial prompts may include confidential holdings, proprietary trading ideas, or regulated investment data.

Mitigation: Do not send sensitive financial information to the external Finskills service unless approved for that data flow.

Risk: Financial data and derived metrics can be mistaken for investment advice.

Mitigation: Present data factually, include units and freshness, and avoid buy or sell recommendations.

## Reference(s):

- [Finskills homepage](https://finskills.net)
- [Finskills API documentation](https://finskills.net/documentation)
- [Finskills skill page](https://finskills.net/skill)
- [ClawHub skill page](https://clawhub.ai/finskills/skills/finskills)
- [ClawHub publisher profile](https://clawhub.ai/user/finskills)

## Skill Output:

**Output Type(s):** [Text, Markdown, API calls, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown or text responses with API request paths, JSON-derived financial summaries, and occasional shell commands for installation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should include units, data freshness, and factual presentation rather than investment advice.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
