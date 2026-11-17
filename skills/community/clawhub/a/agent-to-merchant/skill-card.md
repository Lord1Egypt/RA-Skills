## Description:

SynapseAI Merchant is an AI agent payment receiving layer for registering as a merchant, creating wallets, generating payment links and QR codes, receiving on-chain payments, and managing receiving status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pandagg110](https://clawhub.ai/user/pandagg110)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and AI-agent operators use this skill to guide agents through SynapseAI merchant receiving workflows, including wallet creation, payment-link generation, webhook setup, and payment history queries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents using this skill handle bearer tokens and webhook secrets for merchant receiving workflows.

Mitigation: Keep bearer tokens and webhook secrets private, and verify webhook signatures before acting on payment events.

Risk: The skill can guide agents to create wallets and public payment links, configure callback URLs, and change merchant receiving state in the provider account.

Mitigation: Install only for agents that are authorized to manage SynapseAI merchant receiving, and review wallet, payment-link, webhook, and toggle actions before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/pandagg110/skills/agent-to-merchant)
- [Publisher Profile](https://clawhub.ai/user/pandagg110)
- [SynapseAI Wallet](https://wallet.synapseai.pro)
- [SynapseAI Merchant API](https://wallet.synapseai.pro/api/merchant)

## Skill Output:

**Output Type(s):** [guidance, API calls, configuration, code]

**Output Format:** [Markdown with HTTP examples and JSON payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes bearer-token authenticated merchant API examples, webhook configuration guidance, supported network and currency values, and public payment-link lookup behavior.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
