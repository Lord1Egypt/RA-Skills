## Description:

基于结构化框架分析A股，结合筹码分布、三周期共振、优化KDJ、威科夫、缠论以及用户自定义评分规则，输出结构化分析结论与风险提示。

This skill is ready for commercial/non-commercial use.

## Publisher:

[byronwang2005](https://clawhub.ai/user/byronwang2005)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to turn current or user-provided A-share market data into structured stock analysis, including signal quality, chip distribution, multi-period structure, invalidation conditions, and risk notes. The outputs are for research and strategy reference, not investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional AkShare or BaoShare fallback can depend on third-party market-data packages and upstream data quality.

Mitigation: Use fallback only after explicit user consent; install trusted, pinned packages in an isolated environment where possible and verify conclusions against authoritative market data.

Risk: A-share structure analysis can be mistaken for investment advice or treated as more certain than the available data supports.

Mitigation: Present outputs as research and strategy reference, state data sources and gaps, lower confidence when data is incomplete, and include risk warnings and invalidation conditions.

## Reference(s):

- [筹码分布框架](references/chip-framework.md)
- [量化交易理论参考](references/quant-trading-theory.md)
- [AkShare 接口参考](references/akshare-interfaces.md)
- [新版 mx-skills 路由参考](references/mx-skills-routing.md)
- [ClawHub financial-ai-analyst skills](https://clawhub.ai/u/financial-ai-analyst)
- [mx-skills website](https://ai.eastmoney.com/mxClaw)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, shell commands]

**Output Format:** [Structured Markdown analysis with conclusions, evidence, data-source notes, risk warnings, and optional shell commands for consented fallback setup.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should identify data sources, incomplete data, confidence limits, key dates and price levels, and conditions that would invalidate the analysis.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
