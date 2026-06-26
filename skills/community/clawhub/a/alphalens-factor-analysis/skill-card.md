## Description: <br>
Analyzes alpha factors against forward returns and produces quantile returns, information coefficient, turnover, and related reports for factor research and event analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tangweigang-jpg](https://clawhub.ai/user/tangweigang-jpg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External quant researchers and developers use this skill to prepare market data, evaluate alpha factors with Alphalens-style forward return analysis, run related backtests, and generate markdown or code guidance for reports and tear sheets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill behaves as a broad quant-workflow assistant rather than a narrow read-only factor-analysis helper. <br>
Mitigation: Review the seed and reference files before use, scope each request narrowly, and require explicit confirmation before non-analysis actions. <br>
Risk: Generated workflows may include package installs, code execution, data recorder runs, or persistence actions. <br>
Mitigation: Use an isolated Python environment and require confirmation before running commands, writing files, or saving generated skills. <br>
Risk: Broker or paid-provider credentials could be requested for some data sources or trading-related workflows. <br>
Mitigation: Avoid broker and paid-provider credentials unless they are explicitly needed for the task and approved by the operator. <br>
Risk: Backtest and factor-analysis outputs can be misleading if look-ahead, data alignment, T+1 trading, or transaction-cost constraints are ignored. <br>
Mitigation: Apply the documented semantic locks and preconditions before treating generated analysis as decision-support output. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/tangweigang-jpg/alphalens-factor-analysis) <br>
- [Human Summary](artifact/human_summary.md) <br>
- [Known Use Cases](artifact/references/USE_CASES.md) <br>
- [Semantic Locks and Preconditions](artifact/references/LOCKS.md) <br>
- [Component Capability Map](artifact/references/COMPONENTS.md) <br>
- [Constraints](artifact/references/CONSTRAINTS.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline code, shell commands, configuration guidance, and analysis narrative] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May ask for market, data provider, strategy type, date range, and target entity IDs before producing code or analysis guidance.] <br>

## Skill Version(s): <br>
0.3.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
