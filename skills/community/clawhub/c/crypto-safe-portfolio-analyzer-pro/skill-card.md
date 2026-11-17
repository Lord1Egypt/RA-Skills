## Description:

Safe cryptocurrency portfolio tracking and P&L analysis that monitors portfolio value, calculates profit and loss with custom cost basis, tracks live prices via CoinGecko, and generates detailed reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iamcooper2026](https://clawhub.ai/user/iamcooper2026)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to analyze cryptocurrency holdings, monitor live portfolio value, calculate cost-basis profit and loss, review allocations, and produce text or JSON portfolio reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release includes trading alert code and aggressive strategy examples beyond basic portfolio tracking.

Mitigation: Review generated market signals before use and do not treat them as financial advice.

Risk: Portfolio holdings, wallet addresses, and cost-basis data may expose sensitive financial information if shared through reports or automation.

Mitigation: Keep holdings and cost-basis files private and avoid posting detailed portfolio reports to shared channels.

Risk: Live market data and third-party API availability can affect report accuracy or completeness.

Mitigation: Check source data and API status before relying on generated portfolio or market summaries.

## Reference(s):

- [Usage Examples](references/usage-examples.md)
- [Configuration Example](references/config-example.json)
- [ClawHub Skill Page](https://clawhub.ai/iamcooper2026/skills/crypto-safe-portfolio-analyzer-pro)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON configuration examples, and text or JSON analysis reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include live market data, portfolio values, P&L calculations, allocation breakdowns, and market-signal summaries.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
