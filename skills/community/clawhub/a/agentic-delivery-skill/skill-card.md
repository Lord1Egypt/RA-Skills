## Description:

Create CompleteTech LLC delivery execution artifacts for approved agentic development engagements, including kickoff agendas, access checklists, project plans, milestone trackers, status updates, decision logs, risk/issue logs, change request intake, prototype review, evaluation reports, acceptance packets, launch readiness, monitoring, support, handoff, runbooks, quickstarts, closeout, post-launch review, and escalation procedures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[completetech](https://clawhub.ai/user/completetech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, delivery leads, and service teams use this skill after proposal, SOW, or contract approval to draft bounded delivery artifacts for agentic workflow engagements. It supports kickoff, project control, evaluation, launch readiness, handoff, support, and closeout while preserving approval gates and evidence requirements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated delivery artifacts can overstate approval, acceptance, launch readiness, or completion if placeholders or claims are not verified.

Mitigation: Review all placeholders, approval-sensitive claims, evaluation evidence, and launch gates before sending, storing, or relying on generated documents.

Risk: The optional PNG preview path depends on the Pillow package pin identified in server security guidance.

Mitigation: Omit PNG preview generation or update the Pillow dependency according to the user's approved dependency policy before using that optional path.

Risk: The skill writes user-selected output files, so an incorrect output path can place drafts in the wrong location.

Mitigation: Use explicit output paths and review generated Markdown, PDF, or PNG files before distribution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/completetech/skills/agentic-delivery-skill)
- [OpenClaw Homepage](https://github.com/CompleteTech-LLC/agentic-delivery-skill)
- [Delivery Positioning](references/delivery-positioning.md)
- [Use-Case Decision Table](references/use-case-decision-table.md)
- [Delivery Lifecycle](references/delivery-lifecycle.md)
- [Delivery Catalog](references/delivery-catalog.md)
- [Template Index](references/template-index.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown delivery drafts with optional PDF and PNG file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated artifacts are drafts and may include placeholders until verified by the delivery owner.]

## Skill Version(s):

1.0.9 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
