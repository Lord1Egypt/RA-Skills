## Description:

Helps agents prepare cold email outreach with Resend, CSV lead input, template personalization, deliverability guidance, and campaign sending.

This skill is ready for commercial/non-commercial use.

## Publisher:

[merjua14](https://clawhub.ai/user/merjua14)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to prepare and run small cold email campaigns from CSV leads, personalize template copy, configure sender-domain basics, and review deliverability practices before sending through Resend.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send real cold emails through a Resend account and process recipient contact data.

Mitigation: Run dry-run first, use explicit low sending limits, verify the sender domain, confirm a lawful basis for each contact, and provide unsubscribe, bounce handling, and data-retention controls before live sending.

Risk: Some advertised pipeline features are not present in the provided artifact.

Mitigation: Treat the included campaign sender and reference guides as the implemented surface, and verify or add missing follow-up, enrichment, tracking, and suppression workflows before relying on them.

Risk: Weak guardrails and a sending bug could cause unintended emails.

Mitigation: Use a small test list, review the recipient CSV and rendered messages manually, and do not rely on --limit 0 as a stop control.

## Reference(s):

- [Proven Cold Email Templates](references/templates.md)
- [Email Deliverability Guide](references/deliverability.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with inline bash and JavaScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include operational steps that send real email through a Resend account; use dry-run and explicit sending limits before live use.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
