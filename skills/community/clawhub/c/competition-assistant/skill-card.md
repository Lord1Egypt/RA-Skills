## Description:

Competition Assistant helps college students build competition calendars from official sources and manage local team-matching requests with masked contact details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smallkeyboy](https://clawhub.ai/user/smallkeyboy)

### License/Terms of Use:

MIT-0

## Use Case:

External users, especially college students and campus competition participants, use this skill to find upcoming competitions, verify dates against official sources, and identify potential teammates by competition, skill fit, and availability.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores raw phone, email, QQ, or WeChat details in persistent local team-matching records, and helper outputs can expose complete personal records.

Mitigation: Review before installing; avoid real contact details unless persistent local storage is acceptable, and add explicit consent, retention, deletion, restrictive file permissions, and masked-only list and match outputs before broad use.

## Reference(s):

- [Competition Reference List](artifact/references/competitions.md)
- [Teaming Data Schema and Matching Rules](artifact/references/teaming-schema.md)
- [ClawHub Skill Page](https://clawhub.ai/smallkeyboy/skills/competition-assistant)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown tables and concise guidance, with optional JSON from the local teaming helper.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Competition dates should be verified against official sources; team-matching output should mask contact details.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
