## Description: <br>
Provides guidance for GARCH-family volatility modeling and forecasting, Sharpe ratio bootstrap inference, SPA model comparison, and related quant-strategy workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tangweigang-jpg](https://clawhub.ai/user/tangweigang-jpg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and quant analysts use this skill to generate guidance, code, shell commands, and configuration for backtest-only volatility modeling, statistical inference, model comparison, and ZVT data or strategy workflows across global financial markets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The advertised GARCH analysis purpose is mixed with broader ZVT data collection, backtesting, broker-adjacent, and trading-execution instructions. <br>
Mitigation: Keep use backtest-only by default, review generated workflows before execution, and require separate confirmation and controls before any broker-connected or live-trading action. <br>
Risk: Some workflows may involve paid data providers, QMT broker connectivity, or local market-data setup. <br>
Mitigation: Run setup in an isolated Python environment, use least-privilege credentials only when explicitly needed, and avoid storing broker or paid-provider secrets in generated files. <br>
Risk: The artifact reports quality gaps and may have uncaptured requirement gaps. <br>
Mitigation: Validate critical model assumptions, data sources, trading constraints, and statistical outputs against the referenced source files before relying on results. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/tangweigang-jpg/arch-garch-volatility) <br>
- [Skill Definition](artifact/SKILL.md) <br>
- [Human Summary](artifact/human_summary.md) <br>
- [Known Use Cases](artifact/references/USE_CASES.md) <br>
- [Semantic Locks and Preconditions](artifact/references/LOCKS.md) <br>
- [Anti-Patterns](artifact/references/ANTI_PATTERNS.md) <br>
- [Component Capability Map](artifact/references/COMPONENTS.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline code and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May ask for market, data provider, strategy type, date range, and entity identifiers before producing workflow guidance.] <br>

## Skill Version(s): <br>
0.3.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
