## Description:

Use when an agent needs one universal entrypoint to discover and use the unified Clash of Coins gateway for sale and shop flows, choose the active protocol on the live instance, and execute purchase or integration flows without mixing sale and shop contracts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clash-deployer](https://clawhub.ai/user/clash-deployer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent operators use this skill to discover a live Clash of Coins gateway, select the correct sale or shop route, and produce endpoint, payload, payment retry, and status-check guidance before purchase execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The discovery helper accepts a caller-supplied origin and could probe non-public or untrusted services.

Mitigation: Restrict runs to trusted, known public HTTPS Clash of Coins gateway origins and do not use internal or local URLs.

Risk: Recipient identifiers and buy or fund steps can disclose sensitive purchase intent or trigger payment-related actions.

Mitigation: Require explicit user approval before recipient-scoped probes, buy calls, funding calls, or paid retries.

## Reference(s):

- [Clash of Coins - Agentic Gateway on ClawHub](https://clawhub.ai/clash-deployer/skills/clash-of-coins-agentic)
- [Discovery and Routing](references/discovery-and-routing.md)
- [Purchase Playbooks](references/purchase-playbooks.md)
- [Integration Playbook](references/integration-playbook.md)
- [Client Installation](references/client-installation.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with endpoint, payload, command, and validation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include JSON payload examples and route decision records grounded in live gateway discovery.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
