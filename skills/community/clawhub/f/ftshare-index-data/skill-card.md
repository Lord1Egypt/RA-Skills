## Description:

Provides China A-share index data from market.ft.tech, including single-index details, paginated index lists, OHLC series, minute-level prices, and trade-date lookup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shawn92](https://clawhub.ai/user/shawn92)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve and summarize China A-share index market data for index lookups, index lists, K-line analysis, minute-level price checks, and trade-date calculations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends requested index symbols, filters, dates, and pagination parameters to market.ft.tech.

Mitigation: Use only intended market-data query parameters and avoid placing sensitive information in free-form filters or index lookup text.

Risk: The skill depends on the external market.ft.tech service for data availability and freshness.

Mitigation: Check returned data and service timestamps before relying on results for time-sensitive market analysis.

Risk: The interface and source skill documentation are primarily Chinese, which can increase the chance of parameter or output interpretation errors for non-Chinese users.

Mitigation: Confirm index codes, time ranges, and translated field meanings before presenting results or using them in downstream workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shawn92/skills/ftshare-index-data)
- [market.ft.tech service](https://market.ft.tech)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [JSON data from Python handlers, typically summarized for users as concise text or Markdown tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only GET requests to market.ft.tech; no API key environment variables were detected.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
