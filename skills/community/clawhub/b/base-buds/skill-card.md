## Description:

Mint a Base Bud NFT from the agent-only collection on Base mainnet. Requires solving a challenge, paying 1 USDC (x402), and an EVM wallet.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tron04736-star](https://clawhub.ai/user/tron04736-star)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to complete a Base mainnet NFT mint flow that includes a challenge, a 1 USDC x402 payment, local EVM signing, and transaction broadcast.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to handle a raw EVM private key and sign payment and mint transactions.

Mitigation: Use a dedicated, minimally funded wallet; never paste a valuable wallet private key into the agent; require explicit user confirmation before each signature.

Risk: The skill settles a 1 USDC payment and broadcasts a Base mainnet transaction.

Mitigation: Independently verify the payment amount, chain ID, contract, recipient, transaction calldata, and fees before signing or broadcasting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tron04736-star/skills/base-buds)
- [Base Buds homepage](https://budsbase.xyz)
- [Base Buds skill file](https://budsbase.xyz/skill.md)
- [Base Buds API](https://budsbase.xyz/api)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, API Calls]

**Output Format:** [Markdown with inline bash, JavaScript, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local signing and mint-flow instructions; users should verify all payment and transaction details before signing.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
