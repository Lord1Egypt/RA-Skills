## Description:

Faq Distiller turns support conversations, comments, tickets, and chat logs into categorized FAQ drafts by user stage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

Support, documentation, and knowledge-base teams use this skill to turn provided customer-support material into reviewable FAQ drafts, including frequent questions, staged categories, standard answers, escalation items, missing documentation, and maintenance suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Support records may contain personal, customer, credential, or regulated data.

Mitigation: Redact sensitive data before using the skill and review generated FAQ drafts before sharing or publishing them.

Risk: Generated FAQ drafts may misstate policy, support commitments, or escalation paths if the input material is incomplete.

Mitigation: Treat outputs as reviewable drafts and confirm missing information, escalation items, and standard answers with the responsible support or documentation owner.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/52yuanchangxing/skills/faq-distiller)
- [Publisher profile](https://clawhub.ai/user/52yuanchangxing)
- [Artifact README](artifact/README.md)
- [Output template](artifact/resources/template.md)
- [Structured skill spec](artifact/resources/spec.json)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown draft by default, with optional JSON wrapper from the bundled local script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are intended as reviewable drafts from user-provided local input; the bundled script can write to an output file when requested.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
