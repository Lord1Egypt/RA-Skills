## Description: <br>
Generates AMLSim-compatible synthetic transaction datasets from logs, partitions accounts by bank ID, combines AMLSim outputs, and builds transaction-network graphs for anti-money-laundering system testing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tangweigang-jpg](https://clawhub.ai/user/tangweigang-jpg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, data scientists, and compliance engineers use this skill to prepare synthetic AML datasets and validation artifacts for anti-money-laundering detection workflows. Review use carefully because the artifact also contains quant-trading and backtesting guidance beyond the AML data-generation purpose. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release is advertised as an AML data generator, but artifact instructions also steer agents toward stock and crypto quant trading, backtesting, provider setup, and market-data collection. <br>
Mitigation: Use the skill only for intentionally reviewed AMLSim or ZVT workflows, and keep trading or backtesting tasks separate from AML data-generation tasks unless that mixed behavior is desired. <br>
Risk: The artifact can lead an agent to install packages or configure broker, provider, paid-data, recorder, or trading-related dependencies. <br>
Mitigation: Run in a sandbox with non-sensitive data, review every generated command before execution, and do not provide broker credentials, paid-provider credentials, or production trading access. <br>
Risk: AMLSim graph and alert outputs can be invalid if required topology, account, amount, or pattern constraints are not checked. <br>
Mitigation: Validate generated datasets against the artifact's semantic locks, anti-patterns, and alert-validation references before using the outputs in compliance testing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tangweigang-jpg/aml-data-generator) <br>
- [Known Use Cases](references/USE_CASES.md) <br>
- [Semantic Locks and Preconditions](references/LOCKS.md) <br>
- [Component Capability Map](references/COMPONENTS.md) <br>
- [Anti-Patterns](references/ANTI_PATTERNS.md) <br>
- [Cross-Project Wisdom](references/WISDOM.md) <br>
- [Constraints](references/CONSTRAINTS.md) <br>
- [Seed Metadata](references/seed.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with code snippets and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose AMLSim data-processing steps and, where triggered by the artifact, ZVT market-data or backtesting setup commands.] <br>

## Skill Version(s): <br>
0.3.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
