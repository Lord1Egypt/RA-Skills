## Description:

A股量化数据分析工具，基于AkShare库获取A股行情、财务数据、板块信息等。用于回答关于A股股票查询、行情数据、财务分析、选股等问题。

This skill is for research and development only.

## Publisher:

[hexx89](https://clawhub.ai/user/hexx89)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and market-data analysts use this skill to query A-share quotes, historical K-line data, financial indicators, sector data, fund flow, IPO data, and stock search results through AkShare. Outputs should be treated as informational research data, not investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AkShare dependency changes or upstream website changes may make market-data calls fail or return unexpected fields.

Mitigation: Install in a virtual environment, pin and review the AkShare version, and add local error handling and retries before operational use.

Risk: The bundled fund-flow command may fail because the implementation calls the fund-flow function without the AkShare namespace.

Mitigation: Fix and test the fund-flow command before relying on that action.

Risk: Market-data outputs can be misread as investment recommendations.

Mitigation: Treat results as informational research data only and validate them against authoritative sources before making financial decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hexx89/skills/akshare-stock-tmp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python and shell code blocks; the bundled CLI prints JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language market-data guidance; outputs are informational and may depend on AkShare and upstream website availability.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
