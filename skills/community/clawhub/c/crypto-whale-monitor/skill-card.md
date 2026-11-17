## Description:

Monitors large cryptocurrency wallet balances on-chain using Web3 RPC to detect potential market-moving activity and can read wallet addresses from references/wallets.md or custom inputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[waleolapo](https://clawhub.ai/user/waleolapo)

### License/Terms of Use:

ISC

## Use Case:

Developers, analysts, and operators use this skill to monitor configured Ethereum wallet addresses for large ETH balances and review console alerts that may indicate market-moving wallet activity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet addresses monitored by the skill are sent to the default or configured Ethereum RPC provider.

Mitigation: Review the wallet list and RPC_URL before running, and use a trusted provider when monitored addresses are sensitive.

Risk: Scheduled runs can create recurring network requests to the selected RPC endpoint.

Mitigation: Review cron frequency and endpoint limits before enabling automated monitoring.

Risk: Balance alerts may be incomplete or misleading if the RPC endpoint is unavailable, delayed, or returns errors.

Mitigation: Treat output as monitoring guidance and verify important findings against an independent chain explorer or RPC provider.

## Reference(s):

- [Known Whale Wallet Addresses](references/wallets.md)
- [Default Ethereum RPC endpoint](https://eth.llamarpc.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Console text with wallet address, ETH balance, and alert status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses configured or default wallet lists, an RPC_URL environment override, and a fixed 100 ETH alert threshold.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
