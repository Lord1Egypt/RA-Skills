## Description: <br>
基于结构化框架分析A股，结合筹码分布、三周期共振、优化KDJ、威科夫、缠论以及用户自定义评分规则，输出结构化分析结论与风险提示。 <br>

This skill is for research and development only. <br>

## Publisher: <br>
[byronwang2005](https://clawhub.ai/user/byronwang2005) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn A-share market data or user-provided stock context into structured technical analysis, risk notes, invalidation conditions, and follow-up observation points. It is intended as research support and strategy review, not investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Stock-analysis output may be mistaken for investment advice or may rely on incomplete, stale, or source-limited market data. <br>
Mitigation: Treat results as research support, verify data sources and dates, review confidence warnings, and make financial decisions outside the skill. <br>
Risk: Optional AkShare, BaoShare, package installation, or external-source fallback can access third-party data sources or change the local environment. <br>
Mitigation: Use those fallbacks only after explicit user consent and only for the minimum data needed for the current question. <br>


## Reference(s): <br>
- [A股信号 ClawHub page](https://clawhub.ai/byronwang2005/a-share-signal) <br>
- [mx-skills official site](https://ai.eastmoney.com/mxClaw) <br>
- [Financial AI Analyst ClawHub page](https://clawhub.ai/u/financial-ai-analyst) <br>
- [AkShare interface reference](references/akshare-interfaces.md) <br>
- [Chip distribution framework](references/chip-framework.md) <br>
- [mx-skills routing reference](references/mx-skills-routing.md) <br>
- [Quant trading theory reference](references/quant-trading-theory.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Guidance, Shell commands] <br>
**Output Format:** [Markdown text with structured sections and occasional inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should identify data sources, confidence limits, incomplete data, risk warnings, and invalidation conditions.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
