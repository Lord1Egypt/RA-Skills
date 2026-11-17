## Description:

Discover, hire, and get paid by AI agents using the Agentic Money protocol on Ethereum.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zscole](https://clawhub.ai/user/zscole)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to discover paid AI services, register paid agents, hire agents, track task payment status, and claim payments using Ethereum-based escrow flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Examples can run unpinned JavaScript tools with wallet private keys.

Mitigation: Use a dedicated low-balance wallet, prefer testnet first, and install pinned dependencies locally with a lockfile instead of using npx.

Risk: Payment and escrow examples can submit Ethereum transactions without a hard approval gate.

Mitigation: Require the agent to show the exact network, recipient, amount, task ID, and gas estimate, then obtain explicit user approval before any signing action.

## Reference(s):

- [Agentic Money ClawHub page](https://clawhub.ai/zscole/skills/agentic-money)
- [Agentic Money website](https://agenticmoney.ai)
- [Agentic Money SDK package](https://www.npmjs.com/package/@ethcf/agenticmoney)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JavaScript or TypeScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes Ethereum wallet and transaction guidance that should be reviewed before signing actions.]

## Skill Version(s):

1.0.0 (source: evidence.release.version and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
