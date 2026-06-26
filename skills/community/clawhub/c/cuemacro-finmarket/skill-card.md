## Description: <br>
A finance-market backtesting skill for FX G10 technical-indicator strategies, ArcticDB tick data storage, S3 storage, and market data fetching and caching from providers such as Quandl. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tangweigang-jpg](https://clawhub.ai/user/tangweigang-jpg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and quantitative-finance users use this skill to generate guidance, code, and commands for market data collection, storage, technical-indicator strategy backtesting, and trade analysis. Reviewers should confirm whether a task is intended for the advertised FX/finmarketpy scope or the ZVT/A-share workflow described in the artifact before relying on generated output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The advertised FX/finmarketpy scope may not match the ZVT/A-share operational instructions in the artifact. <br>
Mitigation: Confirm the intended market, framework, data source, and storage path before following generated guidance or running generated code. <br>
Risk: Generated finance workflows may involve sensitive provider keys, broker integrations, S3 buckets, or local market-data stores. <br>
Mitigation: Use an isolated Python environment, prefer read-only credentials, avoid live trading credentials, and choose storage paths and buckets deliberately. <br>
Risk: Backtesting or trading code can produce misleading results if it uses look-ahead signals, incorrect execution timing, or invalid market assumptions. <br>
Mitigation: Review generated code before execution and verify next-bar execution, data schema, transaction-cost assumptions, and market-specific trading rules. <br>


## Reference(s): <br>
- [Cuemacro Finmarket ClawHub Page](https://clawhub.ai/tangweigang-jpg/cuemacro-finmarket) <br>
- [Human Summary](human_summary.md) <br>
- [Known Use Cases](references/USE_CASES.md) <br>
- [Semantic Locks and Preconditions](references/LOCKS.md) <br>
- [Constraints](references/CONSTRAINTS.md) <br>
- [Anti-Patterns](references/ANTI_PATTERNS.md) <br>
- [Component Capability Map](references/COMPONENTS.md) <br>
- [Cross-Project Wisdom](references/WISDOM.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with code and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May ask for market, data provider, strategy type, time range, and entity IDs before producing workflow-specific output.] <br>

## Skill Version(s): <br>
0.3.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
