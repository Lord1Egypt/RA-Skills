## Description:

Create polished, review-ready sales and lifecycle email sequences for agentic development services, then export them as branded PDF artifacts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[completetech](https://clawhub.ai/user/completetech)

### License/Terms of Use:

MIT-0

## Use Case:

Sales, delivery, and customer-lifecycle teams use this skill to draft review-ready outreach, follow-up, proposal, close, kickoff, retention, referral, and win-back email copy for agentic development services. It can also render selected drafts as local Markdown, PDF, and optional PNG artifacts for review before sending.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated email copy may include inaccurate, unsupported, or misleading prospect claims if the user supplies unverified context.

Mitigation: Review every draft before external use and replace placeholders only with verified buyer, workflow, offer, proof, CTA, and routing details.

Risk: Generated Markdown, PDF, or PNG outputs can contain sensitive prospect or client information stored in local files.

Mitigation: Use non-sensitive inputs where possible, choose output paths deliberately, and handle generated local artifacts according to the user's data-handling requirements.

Risk: The optional PDF and PNG rendering path depends on pinned Python packages.

Mitigation: Review the pinned dependencies before installation and install the optional PNG preview stack only when preview generation is needed.

Risk: Drafts are not sent by the skill and may still require recipient, routing, compliance, and approval checks.

Mitigation: Keep a human approval step before sending and verify recipients, opt-out language, and channel-specific requirements outside the skill.

## Reference(s):

- [Agentic Email Skill on ClawHub](https://clawhub.ai/completetech/skills/agentic-email-skill)
- [Project Homepage](https://github.com/CompleteTech-LLC/agentic-email-skill)
- [Project README](https://github.com/CompleteTech-LLC/agentic-email-skill#readme)
- [Agentic Development Email Positioning](references/positioning.md)
- [Email Use-Case Decision Table](references/use-case-decision-table.md)
- [Agentic Development Email Sequence Blueprints](references/sequence-blueprints.md)
- [Near-Exhaustive Agentic Development Email Catalog](references/email-catalog.md)
- [Template Index](references/template-index.json)

## Skill Output:

**Output Type(s):** [text, markdown, files, shell commands, guidance]

**Output Format:** [Markdown prose with optional local Markdown, PDF, and PNG artifact files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated drafts require human review and verified prospect, client, offer, proof, CTA, and routing details before external sending.]

## Skill Version(s):

1.0.9 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
