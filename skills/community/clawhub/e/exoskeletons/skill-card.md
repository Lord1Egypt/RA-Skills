## Description:

Mint and manage onchain AI agent identity NFTs on Base with visual identity, messaging, storage, reputation, modules, wallet features, and marketplace workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[potdealer](https://clawhub.ai/user/potdealer)

### License/Terms of Use:

CC0

## Use Case:

Developers and agent operators use this skill to create and manage Exoskeleton identity NFTs, inspect public onchain profile and reputation data, and build transaction JSON for Base contract interactions. It supports minting, messaging, storage, module activation, token-bound wallets, marketplace listings, and escrow workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can build transactions that spend ETH or tokens and interact with live Base contracts through a third-party submission API.

Mitigation: Use wallet-native signing or a structured HTTPS client where possible, use a restricted Bankr key if Bankr is used, and verify destination contract, chain ID, value, and calldata before broadcasting.

Risk: The documented shell examples use curl and execSync patterns around transaction submission and API-key handling.

Mitigation: Avoid interpolating untrusted values into shell commands, keep API keys in a secret store or restricted environment variable, and prefer direct library calls for automated use.

Risk: Messages, storage values, listing metadata, and deliverables may be public and permanent when written onchain.

Mitigation: Do not put secrets, private user data, credentials, or sensitive deliverables into onchain fields; store only public data or pointers that are safe to disclose.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/potdealer/skills/exoskeletons)
- [Publisher profile](https://clawhub.ai/user/potdealer)
- [Exoskeletons website](https://exoagent.xyz)
- [The Board](https://exoagent.xyz/board)
- [ExoskeletonCore on Basescan](https://basescan.org/address/0x8241BDD5009ed3F6C99737D2415994B58296Da0d)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, JSON]

**Output Format:** [Markdown guidance with JavaScript examples, shell commands, CLI text output, and Bankr-compatible transaction JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces read results from Base RPC calls and unsigned transaction payloads for external signing or submission; it does not sign transactions itself.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
