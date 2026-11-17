## Description:

Creates CompleteTech LLC discovery and scoping artifacts that help Codex gather verified facts for bounded agentic workflow services before proposal, contract, invoice, or delivery work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[completetech](https://clawhub.ai/user/completetech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, consultants, and delivery teams use this skill to qualify agentic workflow opportunities, run structured discovery, capture readiness and risk facts, and prepare proposal or SOW handoff material.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated discovery PDFs may carry CompleteTech branding or default footer and watermark values that are inappropriate for a user's organization or client.

Mitigation: Review generated PDFs before sending them externally and override branding, footer, watermark, and metadata values where appropriate.

Risk: Optional PNG preview dependencies may not satisfy strict dependency-hygiene policies in every environment.

Mitigation: Update, pin, or disable optional PNG preview dependencies when operating in environments with stricter package controls.

Risk: Discovery artifacts are drafts and may include placeholders or unverified assumptions if used without review.

Mitigation: Replace placeholders with verified facts, keep unknowns marked as TBD or open questions, and review outputs before proposal, contract, invoice, launch, or public use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/completetech/skills/agentic-discovery-skill)
- [OpenClaw homepage](https://github.com/CompleteTech-LLC/agentic-discovery-skill)
- [Discovery use-case decision table](references/use-case-decision-table.md)
- [Agentic development discovery lifecycle](references/discovery-lifecycle.md)
- [CompleteTech LLC discovery positioning](references/discovery-positioning.md)
- [Near-exhaustive agentic development discovery catalog](references/discovery-catalog.md)
- [Template index](references/template-index.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown drafts, branded PDF artifacts, optional PNG previews, and command-line rendering guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated discovery artifacts are drafts and must be reviewed, completed with verified client facts, and checked before external use.]

## Skill Version(s):

1.0.3 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
