## Description:

Use the a2a-wallet CLI to interact with A2A agents, discover agents in the registry, manage tasks, sign x402 payments, and manage local wallets.

This skill is for research and development only.

## Publisher:

[ost006](https://clawhub.ai/user/ost006)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to run a2a-wallet CLI workflows for A2A messaging, registry discovery, task management, wallet setup, balance checks, and x402 payment signing for agents. It is appropriate for testing and development workflows involving small micro-payments, not production funds or significant on-chain assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill drives an experimental wallet CLI for payment signing and wallet management.

Mitigation: Use it only for testing and development with small micro-payment amounts, and do not import or fund wallets that hold significant assets.

Risk: The documented macOS/Linux install path pipes a remote installer script into a shell.

Mitigation: Review the installer or use a pinned and verified release before installation.

Risk: Local wallets store private keys as plain files on disk under the user's home directory.

Mitigation: Create dedicated low-value test wallets only, restrict filesystem access where possible, and avoid importing existing funded wallets.

Risk: Wallet import/export, payment signing, configuration changes, and unknown agent URLs can expose funds or credentials to irreversible loss.

Mitigation: Require explicit user confirmation before these actions and inspect the target agent card before sending messages or payments.

Risk: Custodial wallet use depends on a third-party key-management service and the a2a-wallet web service.

Mitigation: Treat custodial wallets as low-value test wallets and avoid relying on them for production funds.

## Reference(s):

- [a2a-wallet repository](https://github.com/planetarium/a2a-x402-wallet)
- [a2a-x402 specification v0.2](https://github.com/google-agentic-commerce/a2a-x402/blob/main/spec/v0.2)
- [a2a-wallet releases](https://github.com/planetarium/a2a-x402-wallet/releases/latest)
- [Privy](https://privy.io)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include CLI commands that interact with external A2A agents, registries, wallet services, and x402 payment signing flows.]

## Skill Version(s):

1.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
