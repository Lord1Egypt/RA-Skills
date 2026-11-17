## Description:

Create CompleteTech LLC agentic development proposals, statements of work, discovery recaps, pilot recommendations, evaluation plans, risk/control plans, implementation roadmaps, acceptance criteria, change orders, retainer proposals, and procurement-ready scope summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[completetech](https://clawhub.ai/user/completetech)

### License/Terms of Use:

MIT-0

## Use Case:

External consultants, sales engineers, and delivery teams use this skill to turn verified discovery facts into buyer-facing proposals, SOW attachments, pilot recommendations, evaluation plans, risk/control plans, and procurement-ready scope summaries for bounded agentic workflow services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated proposals and SOW drafts may include placeholders, assumptions, pricing, acceptance criteria, or commercial terms that are incomplete or incorrect.

Mitigation: Review and replace placeholders with verified client, scope, timeline, pricing, risk, approval, and acceptance details before sending or using the output as contract or invoice input.

Risk: The local PDF/PNG renderer and quality validator rely on Python dependencies.

Mitigation: Use a locked environment or pinned dependencies before running the renderer or validator for release-quality artifacts.

Risk: Proposal language could overstate autonomy, regulated-use readiness, savings, legal claims, or client facts if the user supplies insufficient evidence.

Mitigation: Keep humans in the loop for external communications, production changes, purchases, data export, and material business decisions, and use TBD or ask for facts instead of inventing proof or regulated-use assurances.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/completetech/skills/agentic-proposal-skill)
- [Project Homepage](https://github.com/CompleteTech-LLC/agentic-proposal-skill)
- [Proposal Positioning](artifact/references/proposal-positioning.md)
- [Use-Case Decision Table](artifact/references/use-case-decision-table.md)
- [Proposal Lifecycle](artifact/references/proposal-lifecycle.md)
- [Template Index](artifact/references/template-index.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown proposal drafts with optional branded PDF or PNG rendering through local shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated drafts may contain placeholders and commercial terms, and should be reviewed before they are sent or used as contract or invoice inputs.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
