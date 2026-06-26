## Description: <br>
Runs classic dual moving-average crossover backtests with event-driven signal and position simulation, then produces PyFolio performance reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tangweigang-jpg](https://clawhub.ai/user/tangweigang-jpg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and quantitative researchers use this skill to draft and review Backtrader or ZVT-style market backtesting workflows for A-share, Hong Kong, and crypto strategies. It focuses on SMA crossover backtests, OHLC feed inspection, data ingestion, factor computation, order execution rules, and performance reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Server security review marks the release suspicious because the advertised narrow backtesting helper is broader than the artifacts imply. <br>
Mitigation: Review the manifest, summary, and seed together before installation; split unrelated server, training, research, collection, and persistence behavior into separately reviewed skills if needed. <br>
Risk: The skill may suggest installs, data collection, server starts, training, research, or skill-writing actions that affect the local environment. <br>
Mitigation: Run only in an isolated environment and require explicit user confirmation before installing dependencies, collecting market data, starting services, training, or writing skills. <br>
Risk: Backtesting guidance can produce misleading financial conclusions if data alignment, look-ahead bias, transaction costs, slippage, or market-specific trading rules are mishandled. <br>
Mitigation: Apply the artifact's fatal locks and domain constraints: next-bar execution, T+1 rules where applicable, explicit transaction costs and slippage, warmup handling, point-in-time universes, and data quality checks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tangweigang-jpg/backtrader-event-driven) <br>
- [Human Summary](human_summary.md) <br>
- [Known Use Cases](references/USE_CASES.md) <br>
- [Semantic Locks and Preconditions](references/LOCKS.md) <br>
- [Domain Constraints](references/CONSTRAINTS.md) <br>
- [Component Capability Map](references/COMPONENTS.md) <br>
- [Anti-Patterns](references/ANTI_PATTERNS.md) <br>
- [Cross-Project Wisdom](references/WISDOM.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with code and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include backtesting workflow steps, market data preconditions, strategy logic, execution constraints, and reporting guidance.] <br>

## Skill Version(s): <br>
0.3.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
