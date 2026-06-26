## Description: <br>
Calculates portfolio risk metrics such as annualized return, Sharpe ratio, Sortino ratio, maximum drawdown, and Calmar ratio, with rolling-window statistics and NaN handling for multi-market data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tangweigang-jpg](https://clawhub.ai/user/tangweigang-jpg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and quantitative researchers use this skill for portfolio risk metrics, factor research, and backtesting guidance across multi-market data. The release should be scoped carefully because the evidence also includes trading, data-fetching, and documentation automation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review found mixed signals between a narrow risk-metrics purpose and broader trading, backtesting, data-fetching, and documentation workflows. <br>
Mitigation: Confirm the intended scope with the publisher before installation and restrict use to the approved risk-metrics or backtesting workflow. <br>
Risk: The artifact asks about market data providers and strategy execution details, which could lead an agent toward live trading or broad market-data access. <br>
Mitigation: Do not provide brokerage credentials, live trading authority, broad market-data access, or persistent cache write permissions unless the user explicitly requests and bounds those actions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/tangweigang-jpg/empyrical-risk-metrics) <br>
- [Skill definition](SKILL.md) <br>
- [Human summary](human_summary.md) <br>
- [Component capability map](references/COMPONENTS.md) <br>
- [Use cases](references/USE_CASES.md) <br>
- [Semantic locks](references/LOCKS.md) <br>
- [Domain constraints](references/CONSTRAINTS.md) <br>
- [Anti-patterns](references/ANTI_PATTERNS.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline code, command snippets, and configuration details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3.12+ with uv when generated workflows depend on the referenced Python ecosystem.] <br>

## Skill Version(s): <br>
0.3.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
