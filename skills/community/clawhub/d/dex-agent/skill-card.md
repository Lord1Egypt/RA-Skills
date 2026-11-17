## Description:

DEX Agent helps agents manage a self-custodial Base-chain trading wallet, quote prices, execute Uniswap V3 swaps, and monitor stop-loss and take-profit orders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[avmw2025](https://clawhub.ai/user/avmw2025)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to run direct DeFi trading workflows on Base, including wallet setup, price checks, swap quotes, swap execution, and order monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can operate as a high-risk mainnet trading tool.

Mitigation: Use a test wallet with tiny amounts until the operator has reviewed the code, dependencies, and trading behavior.

Risk: Generated wallet private keys are stored locally in plaintext.

Mitigation: Avoid funding the generated wallet with meaningful assets unless encrypted key storage or another protected custody method is added.

Risk: Token approvals may grant broad spending permission.

Mitigation: Prefer exact approvals and periodically revoke allowances that are no longer needed.

Risk: Automated trades may be sent without pre-broadcast confirmation or complete enforced risk controls.

Mitigation: Add explicit confirmations and enforced slippage, drawdown, and position limits before using the skill with material funds.

## Reference(s):

- [DEX Agent on ClawHub](https://clawhub.ai/avmw2025/skills/dex-agent)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown or terminal text with command invocations and JSON configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local wallet, order, and configuration JSON files, and may submit Base-chain transactions when trading commands are run.]

## Skill Version(s):

1.1.0 (source: server release metadata and artifact manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
