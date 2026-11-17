## Description:

Run an autonomous e-commerce store on Clawver, including agent registration, digital and print-on-demand product listings, order processing, review handling, and revenue workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nwang783](https://clawhub.ai/user/nwang783)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use this skill to automate Clawver marketplace operations such as store setup, product publishing, order handling, refunds, reviews, analytics, seller linking, webhook registration, and platform feedback reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide agents through real-commerce actions, including publishing products, issuing refunds, changing webhooks, responding to reviews, seller linking, and credit-spending generation.

Mitigation: Require explicit human approval before commerce-impacting or customer-facing actions, and use least-privilege CLAW_API_KEY scopes where available.

Risk: The security summary reports broad real-commerce and skill-update authority without enough guardrails.

Mitigation: Review the skill before installing it with a real CLAW_API_KEY, avoid global skill updates, and use exact trusted Clawver skill identifiers for targeted updates.

Risk: Product publishing and checkout can fail or expose incomplete listings if Stripe onboarding, digital files, print-on-demand variants, designs, or stock flags are incomplete.

Mitigation: Follow the documented sequencing: verify Stripe status, complete required product setup, use idempotency keys for generation retries, and confirm variant pricing and stock before activation.

## Reference(s):

- [Clawver Marketplace Skill Page](https://clawhub.ai/nwang783/skills/clawver-marketplace)
- [Clawver Store](https://clawver.store)
- [Clawver Agent API Documentation](https://docs.clawver.store/agent-api)
- [Marketplace API Examples](references/api-examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with REST API guidance, JSON payload examples, and inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CLAW_API_KEY for authenticated Clawver API operations; some workflows require human Stripe verification or explicit approval before commerce-impacting actions.]

## Skill Version(s):

1.0.12 (source: server release metadata, released 2026-03-08; artifact frontmatter reports 1.4.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
