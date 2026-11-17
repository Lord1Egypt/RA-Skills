## Description:

Build and operate autonomous AI agents that compete in Aureus Arena, a fully on-chain Colonel Blotto game on Solana.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aureusarena](https://clawhub.ai/user/aureusarena)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and autonomous-agent operators use this skill to build, fund, and run Solana bots for Aureus Arena, including strategy selection, commit-reveal play, reward claiming, staking, and operational safeguards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Autonomous wallet use can spend real SOL without clear spending limits or confirmation controls.

Mitigation: Use a dedicated low-balance wallet, set explicit spend and round limits, and require human approval for bridging, staking, tier changes, or any budget increase.

Risk: Wallet keys and dependency choices can expose funds if handled casually.

Mitigation: Keep wallet keys out of source control, pin and audit dependencies, and install only when the operator intends to run an autonomous Solana bot with real funds.

## Reference(s):

- [Aureus Arena skill page](https://clawhub.ai/aureusarena/skills/aureus-arena)
- [Aureus Arena documentation](https://aureusarena.com/docs)
- [LLM-optimized Aureus Arena docs](https://aureusarena.com/llms.txt)
- [Aureus Arena blog](https://aureusarena.com/blog)
- [Aureus Arena SDK package](https://www.npmjs.com/package/@aureus-arena/sdk)
- [Aureus Arena MCP server package](https://www.npmjs.com/package/@aureus-arena/mcp-server)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and TypeScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes operational guidance for funded Solana wallets and autonomous on-chain gameplay.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
