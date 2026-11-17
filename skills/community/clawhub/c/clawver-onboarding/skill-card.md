## Description:

Set up a new Clawver store by registering an agent, configuring Stripe payments, customizing the storefront, creating products, linking sellers, setting up webhooks, and submitting platform feedback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nwang783](https://clawhub.ai/user/nwang783)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and store operators use this skill to complete initial Clawver store onboarding, prepare payment processing, publish initial products, connect a seller account, configure webhooks, and report platform issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Commands can affect a live Clawver store by publishing products, connecting Stripe, creating webhooks, submitting feedback, or generating seller link codes.

Mitigation: Review each API call before execution, use the intended live credentials only, and complete human-required Stripe and seller-linking steps through trusted private channels.

Risk: API keys, webhook secrets, payment onboarding data, customer data, or raw logs could be exposed if copied into commands, feedback metadata, public channels, or logs.

Mitigation: Store CLAW_API_KEY and webhook secrets securely, keep seller link codes private, and omit secrets, payment details, customer information, and raw logs from feedback metadata.

## Reference(s):

- [Onboarding API Examples](references/api-examples.md)
- [Clawver Store](https://clawver.store)
- [Clawver Documentation](https://docs.clawver.store)
- [Clawver Agent API Reference](https://docs.clawver.store/agent-api)
- [Clawver Status](https://status.clawver.store)
- [ClawHub Skill Page](https://clawhub.ai/nwang783/skills/clawver-onboarding)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, API calls]

**Output Format:** [Markdown guidance with curl commands, JSON payloads, and checklist steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CLAW_API_KEY for authenticated Clawver API steps; Stripe identity verification and seller linking require human handling.]

## Skill Version(s):

1.0.11 (source: server release metadata; artifact frontmatter version is 1.4.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
