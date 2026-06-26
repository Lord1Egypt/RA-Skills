## Description: <br>
Helps agents support climate ESG investing analysis with Fama-French factor workflows, monthly stock data collection, factor correlation, OLS diagnostics, and significance screening. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tangweigang-jpg](https://clawhub.ai/user/tangweigang-jpg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and finance analysts use this skill to generate guidance, code, shell commands, and configuration for climate ESG factor analysis, ZVT-based quant strategy research, data collection, backtesting, and regression diagnostics. It is most relevant for A-share workflows, with stated support for HK and crypto and limited US stock coverage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can move beyond ESG analysis into broader quant strategy, backtesting, and broker-adjacent workflows. <br>
Mitigation: Use research or paper/backtest mode unless broker integration, credentials, order permissions, budget limits, and confirmation flows have been separately reviewed. <br>
Risk: Generated setup commands or skill files may affect the user's environment or future agent invocations. <br>
Mitigation: Use a virtual environment, pin and verify external packages, and review generated .skill files before reuse. <br>
Risk: Financial factor workflows can produce misleading results when data quality, observation counts, timing, or factor units are wrong. <br>
Mitigation: Check data schemas, use next-bar execution, enforce sufficient regression observations, and verify percentage-to-decimal factor conversion before relying on outputs. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/tangweigang-jpg/climate-esg-investing) <br>
- [Human Summary](artifact/human_summary.md) <br>
- [Known Use Cases](artifact/references/USE_CASES.md) <br>
- [Semantic Locks and Preconditions](artifact/references/LOCKS.md) <br>
- [Anti-Patterns](artifact/references/ANTI_PATTERNS.md) <br>
- [Component Capability Map](artifact/references/COMPONENTS.md) <br>
- [Source Seed](artifact/references/seed.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with code snippets and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose ZVT, data-provider, backtesting, and factor-analysis workflows; financial outputs require review before trading.] <br>

## Skill Version(s): <br>
0.3.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
