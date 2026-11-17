## Description:

Creates structured escalation briefs from user-provided issue context, impact, prior attempts, blockers, support needs, and supporting evidence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

Support, customer-success, incident, and cross-team collaboration users use this skill to turn incomplete issue material into reviewable Markdown escalation briefs and next-step checklists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Escalation inputs can include personal, confidential, or customer-sensitive information.

Mitigation: Provide only material intended for the brief, redact sensitive details before use, and review the generated draft before sharing.

Risk: A brief generated from incomplete input can omit important context or overstate certainty.

Mitigation: Use the skill's missing-information section and require human review before sending or acting on the brief.

Risk: The bundled script includes unused audit-oriented capabilities beyond simple brief drafting.

Mitigation: Keep those capabilities disabled unless they are intentionally reviewed, documented, and needed for the workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/52yuanchangxing/skills/escalation-brief-writer)
- [Publisher profile](https://clawhub.ai/user/52yuanchangxing)
- [README](artifact/README.md)
- [Output template](artifact/resources/template.md)
- [Structured brief spec](artifact/resources/spec.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown by default, with optional JSON from the local script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill can produce reviewable drafts, missing-information lists, next-step checklists, stdout output, or a local output file.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
