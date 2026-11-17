## Description:

Daily report generator that summarizes today's tasks from OpenClaw memory or user input and produces formatted daily reports with optional Markdown and Word export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[youyancheng1](https://clawhub.ai/user/youyancheng1)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and developers use this skill to turn daily task memory or manually supplied work items into shareable daily reports. It supports quick status summaries, report archival, and Word document export for formal updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated reports may include confidential details from local OpenClaw memory files.

Mitigation: Review the report content before sharing, exporting, or archiving it.

Risk: DOCX or other exported report files may be saved to the Desktop or another user-selected path.

Mitigation: Choose an appropriate output location and verify the generated file before distribution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/youyancheng1/skills/dailys-report)
- [Daily Report Config Schema](artifact/references/config-schema.json)
- [Daily Report Workflows](artifact/references/workflows.md)

## Skill Output:

**Output Type(s):** [text, markdown, files, shell commands, configuration]

**Output Format:** [Plain text, Markdown, and DOCX report files, with optional JSON configuration.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can read local OpenClaw memory files and write report files to user-selected paths or the Desktop.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
