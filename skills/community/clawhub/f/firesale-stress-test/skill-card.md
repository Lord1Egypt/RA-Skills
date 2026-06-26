## Description: <br>
Advertised to run bank system-level stress tests using EBA 2018 data to compute CET1 and leverage ratios and simulate balance-sheet resilience under firesale scenarios. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tangweigang-jpg](https://clawhub.ai/user/tangweigang-jpg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Risk, compliance, and finance developers use this skill to request stress-test or market-simulation guidance around firesale scenarios, leverage constraints, market clearing, defaults, and related code-generation workflows. Reviewers should note that the artifact content also steers agents toward quant-trading and backtesting workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan says the skill is advertised as bank stress testing while artifacts repeatedly steer the agent toward quant-trading, backtesting, broker or provider use, package installation, and persistent skill creation. <br>
Mitigation: Install only when that broader behavior is intended, review generated code and package installs before execution, and keep workflows simulation-only unless explicitly approved. <br>
Risk: Broker, provider, or paid data-source access could enable financial actions, account changes, purchases, or sensitive data exposure. <br>
Mitigation: Do not provide broker credentials or live-account access unless every transaction is confirmed by a human and the workflow has been reviewed for permissions, logging, and rollback. <br>
Risk: Generated stress-test or trading calculations can be invalid if inputs, leverage formulas, market-clearing assumptions, or entity identifiers are wrong. <br>
Mitigation: Validate inputs, run preconditions, inspect semantic locks, and compare outputs against trusted financial controls before relying on results. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/tangweigang-jpg/firesale-stress-test) <br>
- [Semantic locks and preconditions](artifact/references/LOCKS.md) <br>
- [Component capability map](artifact/references/COMPONENTS.md) <br>
- [Anti-patterns](artifact/references/ANTI_PATTERNS.md) <br>
- [Cross-project wisdom](artifact/references/WISDOM.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with generated code snippets, shell commands, configuration checks, and workflow steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May ask for target market, data provider, strategy type, time range, and entity IDs before producing code or execution guidance.] <br>

## Skill Version(s): <br>
0.3.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
