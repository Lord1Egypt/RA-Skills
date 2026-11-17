## Description:

Analyze and explain one or two EVM transactions using live Etherscan data and human-verifiable Etherscan evidence links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[etherscan](https://clawhub.ai/user/etherscan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, support teams, and security reviewers use this skill to explain a specific EVM transaction or compare two transactions from Etherscan evidence, including status, calls, asset movements, failures, and verification links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill queries Etherscan-family explorers and may use configured Etherscan CLI credentials.

Mitigation: Use approved explorer/API access, and keep API keys out of prompts, reports, and saved artifacts.

Risk: Partial internal transaction data, labels, decoded token metadata, or missing traces can lead to overconfident conclusions.

Mitigation: Preserve confidence ratings, distinguish observed, derived, and inferred facts, and state when a full trace or verified metadata is unavailable.

## Reference(s):

- [Etherscan Transaction Debugger on ClawHub](https://clawhub.ai/etherscan/skills/etherscan-transaction-debugger)
- [Evidence Collection](references/evidence-collection.md)
- [Execution Semantics](references/execution-semantics.md)
- [Failure Analysis](references/failure-analysis.md)
- [Reporting](references/reporting.md)
- [Regression Cases](references/regression-cases.md)
- [Transaction Report Template](assets/transaction-report-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with Etherscan evidence links; optional JSON evidence bundles and summaries from bundled scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include confidence and limitations; bundled scripts may produce reproducible JSON bundles and summaries.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
