## Description:

A股量化数据分析工具，基于AkShare库获取A股、港股、美股行情、财务数据、板块分析等，用于回答关于股票查询、行情数据、财务分析、资金流向、龙虎榜、涨停跌停、新股IPO、融资融券等问题。

This skill is for research and development only.

## Publisher:

[awsl1414](https://clawhub.ai/user/awsl1414)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and research users can use this skill to query AkShare-based market data and generate guidance for A-share, Hong Kong stock, and U.S. stock行情, financial data, sector analysis, fund flows, IPOs, margin trading, and related stock research questions. The skill output should be treated as research data, not investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AkShare dependency or market-data behavior can change over time.

Mitigation: Pin AkShare to a reviewed version or use a lockfile before installation.

Risk: The skill and bundled CLI make outbound requests to public market-data sources.

Mitigation: Run in an environment where outbound data-source access is expected and permitted.

Risk: Market data can be incomplete, delayed, or unsuitable for investment decisions.

Mitigation: Treat outputs as research data and do not use them as investment advice.

Risk: The bundled fund-flow CLI command may fail without correction.

Mitigation: Review and fix the fund-flow CLI implementation before relying on that command.

## Reference(s):

- [AkShare 股票相关接口完整列表](artifact/references/api-reference.md)
- [ClawHub skill page](https://clawhub.ai/awsl1414/skills/akshare-a-stock)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands, configuration]

**Output Format:** [Markdown with Python and shell code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce AkShare API calls and JSON-style CLI output examples; market-data responses depend on external public data sources.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
