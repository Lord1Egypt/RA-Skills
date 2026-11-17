## Description:

Read-only Ethereum blockchain queries for blocks, transactions, balances, contracts, and logs via RPC and Etherscan APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apexfork](https://clawhub.ai/user/apexfork)

### License/Terms of Use:


## Use Case:

Developers and analysts use this skill to inspect Ethereum blockchain state, transactions, balances, contract data, logs, and gas information without wallet access or transaction signing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: RPC providers and Etherscan can observe addresses, contracts, transaction hashes, and API keys used in queries.

Mitigation: Use trusted providers for sensitive investigations and avoid unnecessary disclosure of sensitive query targets.

Risk: Wallet private keys are unnecessary for this skill and would create avoidable secret exposure.

Mitigation: Keep usage read-only and do not configure private keys, wallets, signing commands, or transaction submission.

Risk: Broad event log queries can exhaust RPC limits or fail on public endpoints.

Mitigation: Use specific contract addresses and narrow block ranges for event log requests.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/apexfork/skills/eth-readonly)
- [Publisher profile](https://clawhub.ai/user/apexfork)
- [Artifact skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires either cast or curl; RPC provider and Etherscan API keys are optional depending on query path.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
