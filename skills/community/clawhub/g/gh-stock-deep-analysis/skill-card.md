## Description:

Provides a structured stock-analysis framework for A-share, Hong Kong, and U.S. equities using current market, financial, news, filing, and research inputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ghgh2026](https://clawhub.ai/user/ghgh2026)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to request structured stock reports by company name or ticker, covering market context, business breakdown, orders and capacity, financials, valuation, shareholder structure, risks, catalysts, and investment guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Completed analyses may be saved locally, added to an analysis history index, published through Feishu Wiki, and announced to a specified Feishu group without clear user approval.

Mitigation: Require explicit confirmation and destination selection before any file write, document publication, Wiki move, or group message.

Risk: The skill produces investment guidance such as ratings, target prices, stop-loss levels, and position suggestions that may be stale, incomplete, or unsuitable for a user's circumstances.

Mitigation: Treat generated reports as informational, verify cited sources and dates, and retain the disclaimer that outputs do not constitute investment advice.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ghgh2026/skills/gh-stock-deep-analysis)

## Skill Output:

**Output Type(s):** [markdown, text, guidance]

**Output Format:** [Markdown stock analysis report with tables, source/date labels, risk analysis, and disclaimer text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language output; may include target prices, stop-loss levels, position suggestions, and cited data dates.]

## Skill Version(s):

1.1.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
