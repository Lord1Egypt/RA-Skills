## Description:

Organizes customer information from sales to delivery into a structured handoff package, highlighting committed items, implementation prerequisites, promise risks, confirmations, and next steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

Customer-success, delivery, and implementation teams use this skill to turn sales opportunity details, commitments, and customer background into review-ready handoff drafts. It is intended for transparent handoffs that expose risks and missing confirmations rather than hiding unfavorable information or replacing contract text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Customer handoff inputs may contain customer, commercial, or personal information.

Mitigation: Use only files intentionally selected for summarization, review the generated draft before sharing, and redact sensitive material when appropriate.

Risk: The generated handoff could be treated as final operational or contractual truth.

Mitigation: Keep the output as a reviewable draft, confirm missing details, and do not use it as a substitute for contract text or approved system changes.

Risk: The local script accepts arbitrary input and output paths.

Mitigation: Run it only on intended local files and choose output paths deliberately.

## Reference(s):

- [Account Handoff Builder ClawHub Page](https://clawhub.ai/52yuanchangxing/skills/account-handoff-builder)
- [Skill Specification](artifact/resources/spec.json)
- [Output Template](artifact/resources/template.md)
- [Example Input](artifact/examples/example-input.md)
- [Example Output](artifact/examples/example-output.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown structured brief, with optional JSON wrapper when the local script is run with JSON output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces review-ready drafts from local input; the bundled script can write to a user-selected output path.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
