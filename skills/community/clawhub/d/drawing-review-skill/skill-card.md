## Description:

Guides AI agents through a structured preliminary review of construction drawings and project documents, helping identify cross-discipline coordination issues and prepare a traceable review report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fanshengrong2022-lgtm](https://clawhub.ai/user/fanshengrong2022-lgtm)

### License/Terms of Use:

MIT-0

## Use Case:

Project managers, engineers, and design reviewers use the skill to prepare drawing sets, check cross-discipline interfaces, reconcile drawings with schedules and other project documents, and draft a preliminary review report for human-led coordination.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The review flow requires cloud submissions and does not itself ensure the author's service is approved for confidential project data.

Mitigation: Confirm the service is approved for the project and redact submitted items; do not submit sensitive materials without approval.

Risk: The security review flags script scans that may exceed the intended folder limits.

Mitigation: Set explicit target and output paths, and approve or restrict font scans outside the project.

Risk: Drawing extraction and checking coverage is incomplete, so automated review may miss issues or produce unreliable conclusions.

Mitigation: Have a qualified person verify the conclusions and coverage before relying on the report.

## Reference(s):

- [Method library index](artifact/references/00-索引.md)
- [Review preparation and scope](artifact/references/02-preparation.md)
- [Drawing data and technical paths](artifact/references/03-tech-path.md)
- [Five-step review process](artifact/references/04-five-steps.md)
- [Coverage self-check](artifact/references/05-self-check.md)
- [Quality rules](artifact/references/06-quality-rules.md)
- [Issue wording standards](artifact/references/08-表述规范.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown preliminary review report with summary tables, itemized follow-up issues, coverage checks, and practical command examples.]

**Output Parameters:** [A scoped set of construction drawings and related project materials, such as DWG/DXF/PDF files, material schedules, quantity lists, contract documents, and review criteria.]

**Other Properties Related to Output:** [Produces preliminary findings; extraction and checking coverage is incomplete, so conclusions require review by a qualified person. Cloud review calls require an API key.]

## Skill Version(s):

1.2.2

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
