## Description:

基于缠中说禅理论为 A 股股票自动识别分型、笔、线段、中枢和背驰，并生成技术分析报告与可视化图表。

This skill is for research and development only.

## Publisher:

[laigen](https://clawhub.ai/user/laigen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technically skilled market researchers can use this skill to run ChanLun-style A-share analysis from a stock code and produce chart-backed Markdown reports. The generated analysis is for learning and research use and should not be treated as investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Tushare Pro API token and the packaged documentation suggests storing it in shell startup files.

Mitigation: Use a restricted virtual environment and provide the token only for the active session or through a managed secret store; avoid writing TUSHARE_TOKEN to ~/.bashrc.

Risk: The security evidence reports an under-disclosed automatic Yahoo Finance fallback, which may send stock queries to an additional external service.

Mitigation: Review network behavior before use and remove or explicitly control the fallback if only Tushare access is expected.

Risk: The generated technical analysis can include operational trading suggestions even though the artifact disclaims investment advice.

Mitigation: Treat outputs as research material and review results alongside independent financial analysis before making decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/laigen/skills/chanlun-technical-analysis)
- [Tushare Pro registration](https://tushare.pro/register)

## Skill Output:

**Output Type(s):** [Markdown, Files, Code, Shell commands, Guidance]

**Output Format:** [Markdown report, PNG chart, optional JSON, and command-line guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a stock code, supports period and output-directory options, and writes generated artifacts under the configured output directory.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
