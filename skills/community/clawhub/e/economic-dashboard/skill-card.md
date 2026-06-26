## Description: <br>
Provides a global macroeconomic dashboard workflow with multi-source local data storage, hot/cold storage separation, and automated refresh scheduling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tangweigang-jpg](https://clawhub.ai/user/tangweigang-jpg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and finance analysts use this skill to build macroeconomic and quantitative workflows, including data refreshes, local storage setup, feature engineering, dashboard views, and strategy or backtest guidance. It is best suited for reviewed finance workflows rather than unattended live-trading automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release is security-reviewed as suspicious because dashboard documentation includes trading, backtesting, credential, package-install, data-deletion, and skill-writing behaviors that are not cleanly scoped. <br>
Mitigation: Install only for intentional finance or quant workflows, review generated commands and code before use, and require explicit confirmation before cleanup, file moves, scheduled jobs, generated-code writes, or trading-related actions. <br>
Risk: The skill may require sensitive finance credentials and local data stores such as API keys, broker credentials, or .zvt data. <br>
Mitigation: Use an isolated virtual environment, pin dependencies, avoid live broker credentials unless explicitly needed, and review where keys and local data are stored. <br>
Risk: Generated financial analysis or backtests can be misleading if data quality, temporal ordering, or next-bar execution rules are not checked. <br>
Mitigation: Treat outputs as decision support, validate source data and assumptions, and manually review backtest logic before relying on it for investment or trading decisions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/tangweigang-jpg/economic-dashboard) <br>
- [Human Summary](human_summary.md) <br>
- [Known Use Cases](references/USE_CASES.md) <br>
- [Semantic Locks and Preconditions](references/LOCKS.md) <br>
- [Anti-Patterns](references/ANTI_PATTERNS.md) <br>
- [Component Capability Map](references/COMPONENTS.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown responses with code blocks, shell commands, and configuration steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose package installation, credential setup, local data storage changes, cleanup tasks, scheduled jobs, generated code, and trading-related workflows that require manual review.] <br>

## Skill Version(s): <br>
0.3.3 (source: ClawHub release evidence; artifact metadata version v6.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
