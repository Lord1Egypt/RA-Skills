## Description:

Generate branded invoice and billing-document PDFs for agentic development services, including deposits, milestones, retainers, change orders, pass-through expenses, credits, receipts, refunds, and closeout billing from verified contract, SOW, milestone, and payment facts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[completetech](https://clawhub.ai/user/completetech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, consultants, and operations staff use this skill to choose and draft invoice, receipt, credit, refund, and closeout billing documents for agentic development engagements from verified commercial facts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated invoices may contain incorrect payment, tax, accounting, client, or contract facts if placeholders or user-provided facts are not reviewed.

Mitigation: Treat generated invoices as drafts and verify all payment, tax, accounting, client, and contract details before sending or posting.

Risk: Optional PNG and logo rendering may process untrusted files through an image dependency that the security guidance flags for caution.

Mitigation: Avoid optional PNG/logo rendering with untrusted files unless the Pillow pin is updated and the runtime environment is controlled.

## Reference(s):

- [Project homepage](https://github.com/CompleteTech-LLC/agentic-invoice-skill)
- [ClawHub skill page](https://clawhub.ai/completetech/skills/agentic-invoice-skill)
- [Agentic Development Invoice Positioning](references/invoice-positioning.md)
- [Invoice Use-Case Decision Table](references/use-case-decision-table.md)
- [Agentic Development Invoice Lifecycle](references/invoice-lifecycle.md)
- [Near-Exhaustive Agentic Development Invoice Catalog](references/invoice-catalog.md)
- [Template index](references/template-index.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Guidance]

**Output Format:** [Markdown guidance with local shell commands; rendered artifacts may include PDF, Markdown, and optional PNG files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated invoices are drafts and require verified client, contract, payment, tax, and accounting facts before use.]

## Skill Version(s):

1.0.10 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
