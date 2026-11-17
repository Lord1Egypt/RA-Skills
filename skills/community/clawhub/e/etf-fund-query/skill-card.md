## Description:

帮助用户查询和比较场内 ETF 的基本信息、持仓、历史表现及市场行情。

This skill is ready for commercial/non-commercial use.

## Publisher:

[e-fintech](https://clawhub.ai/user/e-fintech)

### License/Terms of Use:

MIT-0

## Use Case:

普通投资者和研究人员可按名称、代码或主题查找场内 ETF，并比较规模、费率、持仓、收益和行情；结果仅供信息参考，不构成投资建议。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using the ETF service requires an API key and network access.

Mitigation: Install only if comfortable granting access; keep the API key in the protected local credential file and use the default skills directory unless needed.

Risk: Delayed or incomplete market data could be mistaken for current prices or investment guidance.

Mitigation: Show the data date and quote time, disclose missing data, and present comparisons without personalized investment advice.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/e-fintech/skills/etf-fund-query)
- [Index Hub help guide](https://cdn.efunds.com.cn/eda/h5/itcenter/pd/ai-skills-doc/help.pdf)
- [ETF data and field reference](references/catalog-etf.md)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Concise Chinese prose with tables or lists when useful]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes data dates or quote times, relevant caveats and a non-advice disclaimer.]

## Skill Version(s):

1.0.5 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
