## Description:

Guide for developing with the Arkade TypeScript SDK (@arkade-os/sdk) \u2014 Bitcoin wallets, Lightning, smart contracts, and stablecoin swaps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tiero](https://clawhub.ai/user/tiero)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to build Arkade-based Bitcoin applications with wallet creation, VTXO balance and payment flows, onchain ramps, Lightning swaps, smart contracts, and BTC-to-stablecoin swap guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes examples for irreversible Bitcoin, Lightning, and stablecoin transactions that may move real funds.

Mitigation: Use testnet, signet, mutinynet, or regtest first, and require explicit amount, network, token, fee, and destination-address checks before authorizing any payment, offboard, or swap.

Risk: Example code shows private-key and wallet setup patterns that could expose real credentials if copied directly.

Mitigation: Never paste real private keys into example code; use secure key management and reviewed environment-specific secret handling.

Risk: SDK, swap, and network dependencies can affect transaction behavior and fund safety.

Mitigation: Pin and review dependency versions and verify provider endpoints before using the guidance in production.

## Reference(s):

- [Arkade documentation](https://docs.arkadeos.com)
- [Arkade technical primer](https://docs.arkadeos.com/primer)
- [Arkade Wallet SDK v0.3 setup](https://docs.arkadeos.com/wallets/v0.3/setup)
- [Arkade smart contracts overview](https://docs.arkadeos.com/contracts/overview)
- [Arkade Lightning swaps](https://docs.arkadeos.com/contracts/lightning-swaps)
- [Arkade LLM-friendly documentation index](https://docs.arkadeos.com/llms.txt)
- [ClawHub skill page](https://clawhub.ai/tiero/skills/bitcoin-arkade)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with TypeScript and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes financial transaction examples that require explicit review before use with real funds.]

## Skill Version(s):

0.2.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
