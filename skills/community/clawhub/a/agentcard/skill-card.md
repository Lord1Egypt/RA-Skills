## Description:

Virtual MasterCards for AI agents with crypto payments, a USDC wallet, and autonomous card creation and management through the x402 protocol on Stellar.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asgcompute](https://clawhub.ai/user/asgcompute)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent builders use this skill to let AI agents create, fund, inspect, freeze, and unfreeze virtual MasterCard cards using USDC payments on Stellar. Typical uses include paying for API credits, cloud infrastructure, domains, SaaS subscriptions, and developer tooling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents receive autonomous payment-card authority and may spend funds or access sensitive card details.

Mitigation: Use a low-balance dedicated Stellar wallet and enforce strict spending and tool-use approvals in the client.

Risk: Wallet secrets and PAN/CVV data can be exposed through command-line use, configuration files, logs, or agent messages.

Mitigation: Avoid exposing wallet secrets in commands or config files where possible, restrict logging, and prevent agents from forwarding card details.

Risk: Unversioned npx onboarding can install package changes that have not been reviewed.

Mitigation: Use a pinned, reviewed package version for installation and upgrades.

## Reference(s):

- [ASG Card documentation](https://asgcard.dev/docs)
- [ASG Card homepage](https://asgcard.dev)
- [ASG Card OpenAPI specification](https://asgcard.dev/openapi.json)
- [ASG Card SDK on npm](https://npmjs.com/package/@asgcard/sdk)
- [ASG Card public repository](https://github.com/ASGCompute/asgcard-public)
- [x402 payment protocol](https://www.x402.org/)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, API Calls, Guidance]

**Output Format:** [Markdown with inline shell commands and MCP tool guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Stellar wallet secret or local wallet configuration; ClawHub metadata lists macOS, Linux, and Windows support.]

## Skill Version(s):

0.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
