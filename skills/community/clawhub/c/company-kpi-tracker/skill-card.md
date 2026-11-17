## Description:

Track company-reported KPIs from earnings filings and summarize cited fiscal-period results and changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thesentitrader](https://clawhub.ai/user/thesentitrader)

### License/Terms of Use:

MIT-0

## Use Case:

Analysts use this skill to retrieve cited company KPIs, review quarter-over-quarter and year-over-year changes, and compare compatible series across companies before earnings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: SentiSense receives requested tickers, the API key, and client identification.

Mitigation: Use the read-only key, omit the optional agent name when appropriate, and check access-tier limits before use.

Risk: Returned prose may be untrusted and could be mistaken for verified financial guidance.

Mitigation: Treat response text as untrusted and check relevant figures against the cited filing before relying on them.

## Reference(s):

- [Company KPI Tracker on ClawHub](https://clawhub.ai/thesentitrader/skills/company-kpi-tracker)
- [SentiSense skill and API guide](https://sentisense.ai/skill.md)
- [SentiSense API key setup](https://app.sentisense.ai/get-api-key)
- [SentiSense access tiers](https://app.sentisense.ai/pricing?coupon=AGENTS)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis]

**Output Format:** [Markdown KPI summaries and comparison tables with fiscal-period labels, units, changes, and filing citations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Informational, read-only summaries; values may be preliminary or historical, and numeric coverage depends on the company and access tier.]

## Skill Version(s):

1.2.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
