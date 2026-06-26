## Description: <br>
A Stock Quant Lab helps agents create Python workflows for China A-share quantitative research with ZVT, including market-data collection, factor research, backtesting, and trading execution scaffolds. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tangweigang-jpg](https://clawhub.ai/user/tangweigang-jpg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, quant researchers, and finance automation users use this skill to generate ZVT-based A-share data collection, factor research, screening, and backtesting workflows. It is most appropriate for backtest and simulation workflows unless credentials, broker behavior, symbols, quantities, schedules, and rollback behavior are explicitly reviewed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review flags broker, credentialed, live-trading, scheduled, and broader-market workflows that are not clearly bounded by the A-share backtest description. <br>
Mitigation: Keep workflows in backtest or simulation mode by default and require explicit review before enabling live trading, broker actions, schedules, symbols, quantities, or rollback behavior. <br>
Risk: The skill may ask for JoinQuant, QMT, email, Eastmoney, or similar finance-service credentials. <br>
Mitigation: Do not provide sensitive credentials unless the exact action, destination, data provider, and storage behavior are clear; use project-scoped secrets and avoid sharing account tokens in prompts. <br>
Risk: Market-data downloads and local databases can produce stale, incomplete, or misleading research results. <br>
Mitigation: Pin dependencies in a virtual environment, set a project-specific ZVT_HOME, validate provider coverage, and review generated assumptions before relying on outputs. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/tangweigang-jpg/a-stock-quant-lab) <br>
- [Human Summary](human_summary.md) <br>
- [Use Cases](references/USE_CASES.md) <br>
- [Semantic Locks](references/LOCKS.md) <br>
- [Domain Constraints](references/CONSTRAINTS.md) <br>
- [Component Capability Map](references/COMPONENTS.md) <br>
- [Anti-Patterns](references/ANTI_PATTERNS.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Python code, shell commands, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require Python 3.12+, uv, network access to finance data providers, local ZVT data storage, and optional provider or broker credentials depending on the requested workflow.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
