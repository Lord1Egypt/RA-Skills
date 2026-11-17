## Description:

Register sovereign domains (.badass, .forever, .fuck, .rebel, .pump, .hello, .howdy, .robo, .dnet, .f, bear emoji) on Ethereum mainnet via Impervious Domains contracts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[techno-hippies](https://clawhub.ai/user/techno-hippies)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to choose a label and supported TLD, then prepare a commit/reveal registration flow that mints an Ethereum mainnet domain as an ERC-721 NFT.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill prepares Ethereum mainnet transactions while exact contract addresses, ABIs, transaction values, chain ID, and confirmation rules are not bundled in the package.

Mitigation: Confirm all transaction details against integrity-pinned sources and show them clearly before any wallet signs a transaction.

Risk: The registration flow can spend real assets and mint irreversible on-chain records.

Mitigation: Require user confirmation for the selected label, TLD, recipient wallet, transaction value, and contract target before broadcast.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/techno-hippies/skills/buy-handshake-domain)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown guidance with command and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ETHEREUM_RPC_URL and user review of transaction details before signing.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
