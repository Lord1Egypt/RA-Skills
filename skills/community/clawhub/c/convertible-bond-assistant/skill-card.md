## Description:

可转债打新助手为 A 股可转债投资者提供申购日历、新债分析、上市溢价预测、中签率查询和强赎/下修提醒。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoteng-qd](https://clawhub.ai/user/zhaoteng-qd)

### License/Terms of Use:

MIT

## Use Case:

External A-share convertible-bond investors use this skill to generate subscription calendars, bond analyses, listing premium estimates, and redemption or conversion-price revision alerts for review alongside official exchange or issuer sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Financial guidance could be misleading if demo, mock, delayed, or unofficial market data is treated as investment advice.

Mitigation: Verify outputs against official exchange, issuer, or data-provider sources and do not rely on the skill alone for investment decisions.

Risk: The artifact includes insecure HTTP data-source examples and a syntax error that can prevent normal execution.

Mitigation: Prefer a fixed release that passes syntax checks, pins dependencies, removes unused dependencies, and uses HTTPS-only data sources before deployment.

Risk: Documentation may overstate live financial capability relative to the demo-quality implementation.

Mitigation: Present outputs as informational assistance and disclose data-source and implementation limits to users.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zhaoteng-qd/skills/convertible-bond-assistant)
- [User Guide](references/USER_GUIDE.md)
- [Data Source API Notes](references/API.md)
- [Eastmoney Convertible Bond Data](http://data.eastmoney.com/kzz/)
- [Jisilu Convertible Bond Data](https://www.jisilu.cn/data/cbnew/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text and Markdown-style Chinese summaries with CLI command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are informational and may depend on mock, delayed, or unofficial financial data; users should verify results against official sources.]

## Skill Version(s):

1.0.0 (source: server release metadata, SKILL.md, README.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
