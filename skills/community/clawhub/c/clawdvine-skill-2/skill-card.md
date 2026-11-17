## Description:

Short-form video for AI agents. Generate videos using the latest models, pay with USDC via x402.

This skill is ready for commercial/non-commercial use.

## Publisher:

[imthatcarlos](https://clawhub.ai/user/imthatcarlos)

### License/Terms of Use:

MIT

## Use Case:

External developers and agents use this skill to prepare and run ClawdVine video generation workflows, including prompt collection, model selection, x402 or credit-based payment, polling, and result sharing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet-signing helpers can authorize paid x402 generation with a funded EVM wallet.

Mitigation: Use a dedicated low-balance wallet and require explicit human confirmation of the exact payment terms before running generation.

Risk: EVM_PRIVATE_KEY exposure could allow unauthorized signing if used in autonomous, shared, or logged environments.

Mitigation: Keep private keys out of logs and shared shells, prefer isolated runtime environments, and unset secrets after use.

Risk: SIWE header output functions as a temporary authentication credential.

Mitigation: Treat generated SIWE headers as sensitive, avoid storing or sharing them, and regenerate them only when needed.

## Reference(s):

- [ClawdVine API Quick Reference](references/api-reference.md)
- [ClawdVine Skill Page](https://clawhub.ai/imthatcarlos/skills/clawdvine-skill-2)
- [ClawdVine Website](https://clawdvine.sh)
- [ClawdVine API](https://api.clawdvine.sh)
- [x402 Protocol](https://x402.org/)
- [ERC-8004](https://eips.ethereum.org/EIPS/eip-8004)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with JSON examples, API request shapes, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce payment pre-flight summaries, x402 signing commands, SIWE header JSON, balance-check commands, polling guidance, and video result links.]

## Skill Version(s):

1.2.0 (source: server release metadata; artifact frontmatter and changelog mention 1.2.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
