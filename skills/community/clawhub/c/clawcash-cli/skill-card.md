## Description:

Access x402 services on credit through ClawCash: check tier and available credit, proxy x402 calls with automatic payment, and manage repayment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[akshaydevh](https://clawhub.ai/user/akshaydevh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to install and use ClawCash for credit-funded x402 requests, credit checks, partner preflights, and repayment workflows. It is intended for agents that need a ClawLens-backed USDC credit line instead of a pre-funded wallet.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation can trigger identity, credential, and credit-account setup.

Mitigation: Require explicit approval before identity submission, token minting, CLI initialization, credit-funded fetches, and repayment actions.

Risk: The skill depends on mutable remote instructions and unpinned npx execution.

Mitigation: Review the ClawCash and ClawLens providers, verify prerequisite instructions before use, and prefer a pinned audited CLI version.

Risk: Platform tokens and repayment URLs can expose access to ClawCash account actions.

Mitigation: Keep tokens and repayment URLs out of logs, URLs, screenshots, client code, and commits.

Risk: Credit-funded usage can create debt, delinquency, credit freeze, or suspension conditions.

Mitigation: Check credit status before use, confirm repayment responsibilities, and settle bills promptly through the documented repayment flow.

## Reference(s):

- [ClawCash homepage](https://cash.clawlens.io)
- [ClawCash Skill page](https://clawhub.ai/akshaydevh/skills/clawcash-cli)
- [ClawCash SKILL.md](https://cash.clawlens.io/SKILL.md)
- [ClawLens prerequisite skill](https://api.clawlens.io/skill.md)
- [ClawLens](https://clawlens.io)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, text]

**Output Format:** [Markdown guidance with inline shell commands and CLI output examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and npx; uses the @clawcash/cli CLI and ClawLens prerequisite setup.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
