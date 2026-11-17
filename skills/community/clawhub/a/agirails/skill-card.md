## Description:

Trustless payment protocol for AI agents - ACTP escrow plus x402 instant payments, settled in USDC on Base L2.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unima3x](https://clawhub.ai/user/unima3x)

### License/Terms of Use:

MIT

## Use Case:

Developers and external agent operators use this skill to let agents earn, pay, and settle USDC transactions through ACTP escrow or x402 instant payment flows. It provides onboarding, wallet setup, provider and requester templates, OpenClaw configuration, validation patterns, and test commands for mock, testnet, and mainnet use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents can receive real-money wallet authority for mainnet USDC payments.

Mitigation: Use mock or testnet first, require explicit human approval for mainnet payments, enforce spending limits, and keep provider and x402 destination allowlists.

Risk: Wallet secrets and keystore passwords may be exposed if placed in broad configuration, logs, or raw private key environment variables.

Mitigation: Prefer encrypted keystores, keep passwords out of general config files when possible, avoid raw private keys, and review secret handling before deployment.

Risk: Installation and package execution paths can introduce supply-chain risk.

Mitigation: Pin package versions, verify downloaded content before using remote install paths, and review the skill before installing.

Risk: x402 instant payments are final and ACTP real-network escrow requires explicit release after delivery verification.

Mitigation: Use ACTP escrow for work with deliverables, verify delivery before release, and limit x402 to approved low-value endpoints.

## Reference(s):

- [ClawHub Skill Listing](https://clawhub.ai/unima3x/skills/agirails)
- [AGIRAILS Documentation](https://docs.agirails.io)
- [AGIRAILS FAQ](https://agirails.app/faq)
- [AGIRAILS SDK for Node.js](https://www.npmjs.com/package/@agirails/sdk)
- [AGIRAILS SDK for Python](https://pypi.org/project/agirails/)
- [ACTP State Machine](references/state-machine.md)
- [Requester Agent Template](references/requester-template.md)
- [Provider Agent Template](references/provider-template.md)
- [OpenClaw Security Checklist](openclaw/security-checklist.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with TypeScript, JavaScript, Python, JSON, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces agent-facing setup flows, payment templates, configuration snippets, validation patterns, and operational checklists.]

## Skill Version(s):

3.0.12 (source: ClawHub release metadata; source files declare 3.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
