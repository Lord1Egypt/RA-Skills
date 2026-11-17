## Description:

Mint a Claws NFT from the agent-only collection on Solana. Requires solving a challenge and a Solana wallet.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liboheng](https://clawhub.ai/user/liboheng)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to mint a Claws NFT on Solana by requesting a challenge, submitting the answer, signing the returned transaction locally, and submitting it.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence marks the release suspicious because the skill asks users to sign a server-created Solana transaction without requiring transaction validation first.

Mitigation: Use a dedicated wallet funded only with the minimum SOL needed, decode the transaction independently, verify expected mint programs, accounts, fees, and transfers, and abort if anything is unclear or extra.

Risk: Minting requires a funded Solana wallet and creates an on-chain transaction with fee and asset-transfer effects.

Mitigation: Confirm the wallet address, expected NFT mint, collection details, and network fees before signing and submitting the transaction.

## Reference(s):

- [Claws NFT website](https://clawsnft.com)
- [Claws NFT API base](https://clawsnft.com/api)
- [Published skill file](https://clawsnft.com/skill.md)
- [ClawHub skill page](https://clawhub.ai/liboheng/skills/claws-nft)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, API calls, configuration]

**Output Format:** [Markdown with curl commands, JavaScript snippets, and JSON API payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Solana wallet, challenge response, and at least 0.025 SOL.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
