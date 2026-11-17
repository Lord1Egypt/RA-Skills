## Description:

Decentralized AI inference via Bittensor SN64 (43+ chat models) and SN19 (image gen) plus embeddings -- OpenAI-compatible, paid in USDC on Base/Solana via Spraay x402.

This skill is ready for commercial/non-commercial use.

## Publisher:

[plagtech](https://clawhub.ai/user/plagtech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to route chat completions, image generation, model listing, and embeddings through Bittensor-backed decentralized inference endpoints when decentralized or Web3-aligned infrastructure is desired.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, text, and image requests are sent to Spraay and Bittensor miners.

Mitigation: Avoid sending sensitive or proprietary data unless the user has accepted that external processing risk.

Risk: Each endpoint call may spend USDC through x402 micropayments.

Mitigation: Use a dedicated low-balance wallet and review the documented endpoint prices before running calls.

Risk: The artifact documents a helper command path, but no executable helper script is bundled in the artifact.

Mitigation: Verify the runtime integration or helper script availability before relying on the documented shell commands.

## Reference(s):

- [Bittensor AI ClawHub Skill](https://clawhub.ai/plagtech/skills/bittensor-x402)
- [Spraay Gateway](https://gateway.spraay.app)

## Skill Output:

**Output Type(s):** [Text, Image URLs, Embeddings, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline bash and JSON examples; API responses use OpenAI-compatible JSON shapes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires bash and curl; calls may spend USDC through x402 micropayments.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
