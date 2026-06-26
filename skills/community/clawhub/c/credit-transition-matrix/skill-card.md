## Description: <br>
Supports credit rating transition matrix workflows, including Not-Rated state redistribution, annual-to-monthly matrix conversion, state-space definition, dataset characterization, and matrix analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tangweigang-jpg](https://clawhub.ai/user/tangweigang-jpg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and credit-risk practitioners use this skill to prepare, validate, estimate, transform, and explain credit rating transition matrices for risk modeling and reporting workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence reports a suspicious mismatch: the skill is packaged as a credit-risk matrix helper, but artifacts also steer agents toward quant trading, market data collection, backtesting, and broker/provider workflows. <br>
Mitigation: Before allowing execution, review generated scripts and confirm any package installs, market-data downloads, local ZVT writes, paid-provider use, broker-related steps, or trading/order-related logic. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/tangweigang-jpg/credit-transition-matrix) <br>
- [Use Cases](artifact/references/USE_CASES.md) <br>
- [Components](artifact/references/COMPONENTS.md) <br>
- [Semantic Locks and Preconditions](artifact/references/LOCKS.md) <br>
- [Constraints](artifact/references/CONSTRAINTS.md) <br>
- [Anti-Patterns](artifact/references/ANTI_PATTERNS.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with generated code snippets, shell commands, and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May ask for market, data provider, strategy type, time range, and target entity IDs when the requested workflow requires them.] <br>

## Skill Version(s): <br>
0.3.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
