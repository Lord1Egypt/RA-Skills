## Description: <br>
Builds and backtests multi-strategy portfolios with the bt framework, including risk parity, equal risk contribution, inverse-volatility allocation, and simulated government bond rolling strategies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tangweigang-jpg](https://clawhub.ai/user/tangweigang-jpg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and quant strategy practitioners use this skill to generate code and guidance for portfolio backtests across A-share, HK, crypto, and selected fixed-income scenarios, including data preparation, factor logic, portfolio allocation, execution constraints, and result analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release presents as a bt portfolio backtest helper while evidence.security reports broader ZVT data collection, provider or broker credential use, and local persistence behavior. <br>
Mitigation: Review before installing, run package installation, zvt.init_dirs, recorder, and provider commands in an isolated environment, and avoid broker-linked credentials unless explicitly needed. <br>
Risk: Recorder or provider workflows may collect data or save generated skill files locally. <br>
Mitigation: Require user confirmation before data collection or file persistence and review generated code before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tangweigang-jpg/bt-portfolio-backtest) <br>
- [Known Use Cases](references/USE_CASES.md) <br>
- [Semantic Locks](references/LOCKS.md) <br>
- [Domain Constraints](references/CONSTRAINTS.md) <br>
- [Component Capability Map](references/COMPONENTS.md) <br>
- [Anti-Patterns](references/ANTI_PATTERNS.md) <br>
- [Source-of-Truth Seed](references/seed.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with code and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May ask for market, provider, strategy type, time range, and target entity IDs before generating backtest workflow guidance.] <br>

## Skill Version(s): <br>
0.3.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
