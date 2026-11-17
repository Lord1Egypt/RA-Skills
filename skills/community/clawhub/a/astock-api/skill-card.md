## Description:

A股实时行情、K线技术指标、资金流向、财务数据查询。支持任意A股代码，返回结构化数据。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wsyy002](https://clawhub.ai/user/wsyy002)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, quantitative analysts, and agent builders use this skill to query A-share, Hong Kong stock, ETF, and macroeconomic market data for trading assistants, market-monitoring tools, and automated review workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled script uses an undocumented embedded default API token.

Mitigation: Require users to provide their own API key and store it outside the skill before operational use.

Risk: Tokens may be passed in URL parameters or command-line arguments.

Mitigation: Prefer an authorization header or another non-URL secret transport if the API supports it, and avoid exposing private keys in shell history or logs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wsyy002/skills/astock-api)
- [A-Share Stock Data API homepage](https://api.jyfg.de5.net:2096)

## Skill Output:

**Output Type(s):** [API calls, JSON, Text, Shell commands]

**Output Format:** [Structured API responses and formatted text from command-line examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns market data fields with request timing when provided by the API.]

## Skill Version(s):

1.0.1 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
