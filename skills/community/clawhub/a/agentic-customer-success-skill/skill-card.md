## Description:

Create CompleteTech LLC customer success and account management artifacts for agentic development clients, including account profiles, contact maps, approved email/contact routing, meeting notes, follow-up trackers, health scorecards, relationship risk logs, renewal readiness, expansion briefs, QBRs, support escalations, satisfaction surveys, testimonial/referral plans, executive check-ins, at-risk recovery, offboarding, stakeholder changes, communication cadence, success criteria reviews, and post-launch adoption check-ins.

This skill is ready for commercial/non-commercial use.

## Publisher:

[completetech](https://clawhub.ai/user/completetech)

### License/Terms of Use:

MIT-0

## Use Case:

External teams and customer-facing agents use this skill to draft customer success and account management artifacts for agentic development clients, including contact routing, follow-up tracking, health reviews, renewal planning, expansion briefs, QBRs, support escalations, and at-risk recovery plans.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated customer-success communications may contain unsupported account facts, sentiment, approvals, renewal intent, testimonials, referrals, email addresses, or business outcomes if user inputs are incomplete.

Mitigation: Treat generated artifacts as drafts, preserve TBD or open questions for missing evidence, verify contact routing and account facts, and require human review before sensitive, billing, legal, executive, support, renewal, testimonial, referral, or at-risk communications are sent.

Risk: Optional PNG preview generation and untrusted Markdown or logo inputs depend on pinned local rendering packages, including Pillow.

Mitigation: Review and update pinned rendering dependencies before processing untrusted inputs or using optional PNG preview generation.

## Reference(s):

- [Agentic Customer Success Skill Repository](https://github.com/CompleteTech-LLC/agentic-customer-success-skill)
- [Customer Success Catalog](references/customer-success-catalog.md)
- [Customer Success Lifecycle](references/customer-success-lifecycle.md)
- [Customer Success Positioning](references/customer-success-positioning.md)
- [Use Case Decision Table](references/use-case-decision-table.md)
- [Template Index](references/template-index.json)

## Skill Output:

**Output Type(s):** [text, markdown, files, shell commands, configuration, guidance]

**Output Format:** [Markdown drafts, branded PDF files, optional PNG previews, and local renderer commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Rendered artifacts are drafts that require verified account, contact, routing, support, renewal, and approval facts before use.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
