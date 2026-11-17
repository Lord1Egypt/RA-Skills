## Description:

BOB — An Agentic Proof of Work NFT on Base. AI solves puzzles to mint. Earlier mints have lower difficulty and rarer traits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tron04736-star](https://clawhub.ai/user/tron04736-star)

### License/Terms of Use:

MIT-0

## Use Case:

External users with a funded Base EVM wallet use BOB to solve mint puzzles, sign transactions locally, and submit signed transactions to mint BOB NFTs on Base.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to handle a raw EVM private key.

Mitigation: Use a fresh wallet funded only with the exact amount the user is willing to spend, and never use a main wallet private key.

Risk: The workflow signs server-provided blockchain transactions.

Mitigation: Require manual review of the destination contract, chain, value, calldata, and fees before any signature.

Risk: API agentHint responses may influence the agent's next steps.

Mitigation: Treat agentHint content as untrusted text and follow only the reviewed skill workflow.

Risk: The workflow may rely on mutable remote downloads or unpinned npm installs.

Mitigation: Avoid unpinned installs and mutable remote skill downloads in any private-key workflow.

## Reference(s):

- [BOB ClawHub Skill Page](https://clawhub.ai/tron04736-star/skills/bob)
- [BOB Website](https://www.bobsmint.xyz)
- [BOB Skill File](https://www.bobsmint.xyz/skill.md)
- [BOB API Base](https://www.bobsmint.xyz/api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with curl commands, JavaScript signing code, and API response handling guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces step-by-step minting instructions and transaction submission guidance; does not produce files.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
