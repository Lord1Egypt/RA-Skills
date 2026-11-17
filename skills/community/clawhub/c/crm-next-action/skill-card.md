## Description:

Generates reviewable next actions, follow-up rationale, and non-advancement reasons for CRM opportunity pools or customer lists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

Sales, customer success, and revenue teams use this skill to turn CRM opportunity or customer-list inputs into reviewable Markdown guidance with summaries, next actions, rationale, non-advancement reasons, risks, and priorities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local helper reads CRM or opportunity files supplied by the user and can write a report file.

Mitigation: Use appropriate local input files, avoid unnecessary sensitive data, and review the generated report before sharing or acting on it.

Risk: Generated next-action recommendations could be mistaken for approved CRM updates or customer communications.

Mitigation: Keep the output as a reviewable draft and require human approval before CRM writes, messages, or other external actions.

Risk: The package includes unused audit modes that may confuse operators about supported behavior.

Mitigation: Publishers should document or remove unused modes, and users should rely on the documented CRM next-action workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/52yuanchangxing/skills/crm-next-action)
- [README](artifact/README.md)
- [Output template](artifact/resources/template.md)
- [Specification](artifact/resources/spec.json)
- [Example input](artifact/examples/example-input.md)
- [Example output](artifact/examples/example-output.md)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Files, Shell commands, Guidance]

**Output Format:** [Structured Markdown report, with an optional JSON wrapper from the local helper script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads local CRM or opportunity input and may write a report file when an output path is provided.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
