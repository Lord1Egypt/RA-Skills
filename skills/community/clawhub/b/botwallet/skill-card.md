## Description:

Operate the Botwallet CLI so an agent can create a USDC wallet, make payments, create invoices, request funds, withdraw, and access paid APIs on Solana within human-managed guard rails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kasrazunnaiyyer](https://clawhub.ai/user/kasrazunnaiyyer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent users use this skill to give shell-capable agents a Botwallet-managed USDC wallet for payments, paylinks, x402 API purchases, fund requests, and withdrawals under owner-controlled spending limits and approvals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill operates a real-money wallet and can initiate invoices, payments, withdrawals, x402 purchases, and fund requests.

Mitigation: Use strict spending limits, merchant allowlists, and explicit human approval for invoices, payments, withdrawals, x402 purchases, and fund requests.

Risk: The install flow uses an unpinned global CLI package.

Mitigation: Prefer a pinned, verified CLI version and review the package source before installation.

Risk: Registration metadata can disclose host, environment, secret, or broad project details if used carelessly.

Mitigation: Avoid sending hostname, environment, secrets, or broad project metadata during registration.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kasrazunnaiyyer/skills/botwallet)
- [Botwallet website](https://botwallet.co)
- [Botwallet dashboard](https://app.botwallet.co)
- [Botwallet documentation](https://docs.botwallet.co)
- [Botwallet agent CLI source](https://github.com/botwallet-co/agent-cli)
- [Botwallet agent CLI on npm](https://www.npmjs.com/package/@botwallet/agent-cli)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with inline shell commands and JSON-oriented CLI responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may create local wallet configuration and key-share files and may initiate real-money USDC workflows that require owner guard rails and approvals.]

## Skill Version(s):

0.2.1 (source: server release metadata and claw.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
