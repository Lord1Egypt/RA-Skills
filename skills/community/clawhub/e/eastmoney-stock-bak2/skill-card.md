## Description:

Queries stock and sector market data through Eastmoney and Sina endpoints to answer price, change, volume, turnover, and sector-ranking questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[make453](https://clawhub.ai/user/make453)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to ask for stock quotes, price movement summaries, trading volume and amount, and A-share sector rankings. Outputs should be treated as informational market summaries, not verified live quotes or investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Market data may be inaccurate, delayed, stale, or sourced from a provider different from what the skill description implies.

Mitigation: Disclose the actual Eastmoney and Sina data sources, label delay expectations, and verify material financial outputs against an independent trusted market-data source.

Risk: Hardcoded or fixed-date sector outputs and prescriptive allocation suggestions can be mistaken for current investment advice.

Mitigation: Remove or clearly label fixed-date examples, avoid portfolio allocation recommendations unless explicitly scoped, and present stock outputs as informational only.

Risk: Some artifact code uses HTTP market-data requests for Eastmoney endpoints.

Mitigation: Use HTTPS endpoints where available and review network behavior before deployment in environments that rely on data integrity.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/make453/skills/eastmoney-stock-bak2)
- [Sina quote endpoint used by artifact](https://hq.sinajs.cn/list={code})
- [Eastmoney sector ranking endpoint used by artifact](http://push2.eastmoney.com/api/qt/clist/get)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown-style text with tabular market summaries and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Financial data may be delayed, stale, hardcoded, or sourced from multiple public market-data endpoints.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
