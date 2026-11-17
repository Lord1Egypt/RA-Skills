## Description:

A股多空辩论深度分析 - 多空研究员对抗辩论式个股深度研究，输出结构化投资简报

This skill is ready for commercial/non-commercial use.

## Publisher:

[jioup777](https://clawhub.ai/user/jioup777)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to analyze A-share equities by gathering market, K-line, fund-flow, and financial data, then generating bull and bear arguments, a trading posture, risk notes, and a non-advice disclaimer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill starts a local proxy binary from `/tmp`, which could execute unintended code or affect other network traffic.

Mitigation: Use a trusted, verified proxy binary and configuration outside `/tmp`, and track and stop only the proxy process started for this skill.

Risk: The data collection flow executes Python using user-supplied stock identifiers.

Mitigation: Validate stock identifiers against the expected A-share formats before execution.

Risk: Stock queries, collected market data, and generated analysis may be sent to BigModel/GLM.

Mitigation: Disclose external API use to users, protect `GLM_API_KEY`, and avoid sending sensitive portfolio or account information.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jioup777/skills/a-stock-debate)
- [BigModel API base URL](https://open.bigmodel.cn/api/paas/v4)
- [Tencent Finance quote endpoint](https://qt.gtimg.cn/q={prefix}{code})
- [Tencent K-line endpoint](https://web.ifzq.gtimg.cn/appstock/app/fqkline/get)
- [Eastmoney fund-flow endpoint](https://push2his.eastmoney.com/api/qt/stock/fflow/daykline/get)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown report with tables, structured analysis, risk notes, and inline shell/Python snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a stock code, name, or shorthand as input; may call external market data services and BigModel/GLM; final reports include an investment-advice disclaimer.]

## Skill Version(s):

2.1.0 (source: release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
