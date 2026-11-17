## Description:

Email assistant for Romain at ArcaScience that reads and triages inbox messages, drafts context-aware replies using pharma sales context, and manages outreach with suggested attachments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[atomus42](https://clawhub.ai/user/atomus42)

### License/Terms of Use:

MIT-0

## Use Case:

Business development users at ArcaScience use this skill to review email, identify messages needing replies, and prepare relationship-aware outreach for pharma prospects, clients, internal colleagues, and institutional contacts. It supports draft review workflows and requires explicit confirmation before sending.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads full email bodies and uses sensitive business context, sales materials, and stakeholder dossiers.

Mitigation: Install only for the intended ArcaScience mailbox and limit access to required email, dossier, and sales-material sources.

Risk: Email content and linked content can contain malicious or misleading instructions.

Mitigation: Treat inbound and linked content as untrusted and keep system and user instructions above email-provided instructions.

Risk: Automatic daily workflows may create drafts from sensitive or stale mailbox content.

Mitigation: Make the daily cron workflow opt-in and expose review controls before any draft is sent.

Risk: Incorrect attachments could disclose internal documents, contracts, or confidential business information.

Mitigation: Require explicit approval before web lookups and sensitive attachments, never attach internal-only material to external contacts, and cap attachments to focused, reviewed selections.

Risk: Gmail sending can create irreversible external communications.

Mitigation: Require explicit user confirmation for each send action and show the final recipients, body, and attachments before sending.

## Reference(s):

- [Arcascience Email on ClawHub](https://clawhub.ai/atomus42/skills/arcascience-email)
- [ArcaScience Email Assistant Instructions](artifact/SKILL.md)
- [ArcaScience Company Context & Positioning](artifact/references/arcascience-context.md)
- [ArcaScience Sales Package - Platform & Product Reference](artifact/references/sales-package-platform.md)
- [ArcaScience Sales Package - Client Proposals & BRA Analysis](artifact/references/sales-package-proposals.md)
- [ArcaScience Sales Package - Operations & Contracts](artifact/references/sales-package-operations.md)
- [ArcaScience Sales Package - Buyer Personae Analysis](artifact/references/sales-package-personae.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown email triage tables, reply drafts, attachment suggestions, and confirmation prompts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Drafts may include recipient, subject, detected language, tone, dossier status, and attachment recommendations; sending requires explicit user confirmation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
