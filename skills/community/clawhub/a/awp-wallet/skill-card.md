## Description:

AWP Wallet helps agents handle EVM wallet tasks such as balance checks, transfers, token approvals, message signing, gas estimation, and transaction history across EVM chains.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kilb](https://clawhub.ai/user/kilb)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill when an agent needs to check wallet state, prepare or submit EVM transactions, approve token spending, sign messages, estimate gas, or inspect transaction status. The skill is intended for wallet operations that require careful user confirmation because they can affect funds or authorizations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can move funds, approve token spending, or sign data.

Mitigation: Require explicit user confirmation that includes the chain, asset, amount, recipient or spender, and requested signing action before execution.

Risk: Installer and session handling are under-scoped for wallet authority.

Mitigation: Review before installing, do not run the installer with sudo, and use separate low-value wallet profiles until the installation and session handling concerns are resolved.

Risk: Secrets or session tokens may be exposed if passed in logged command lines.

Mitigation: Avoid passing seed phrases, passwords, API keys, or session tokens in logged command lines; prefer controlled environment handling and lock sessions when work is complete.

## Reference(s):

- [AWP Wallet ClawHub Skill](https://clawhub.ai/kilb/skills/awp-wallet)
- [AWP Wallet Homepage](https://github.com/awp-core/awp-wallet)
- [ClawHub Publisher Profile](https://clawhub.ai/user/kilb)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command examples; awp-wallet commands return JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local Node.js CLI installation and wallet/session configuration; operations may interact with live EVM networks.]

## Skill Version(s):

0.15.0 (source: package.json and ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
