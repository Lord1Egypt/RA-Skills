## Description:

Provides best practices and code patterns for building, scaling, and operating production Stripe payment systems from checkout to enterprise billing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1kalin](https://clawhub.ai/user/1kalin)

### License/Terms of Use:


## Use Case:

Developers, SaaS teams, founders, and marketplace builders use this skill to design and review Stripe checkout, subscription billing, webhooks, Connect, tax, testing, and production operations workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe payment idempotency examples may be copied into production Stripe integrations.

Mitigation: Review and correct generated Stripe code so all mutating API calls use stable, persisted order, checkout, subscription, or usage-batch identifiers instead of time-derived keys.

Risk: Broad production-impacting guidance may lead an agent to propose live Stripe account changes without enough context.

Mitigation: Require explicit test or live environment selection and user confirmation before account-changing actions such as subscription updates, cancellations, refunds, usage reporting, or Connect transfers.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/1kalin/skills/afrexai-stripe-production)
- [Artifact README](artifact/README.md)
- [Artifact skill source](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with TypeScript, YAML, checklist, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include production readiness checklists, Stripe integration snippets, webhook patterns, and operational review steps.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
