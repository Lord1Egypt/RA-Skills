## Description:

Build incident response timelines and report packs from event logs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0x-professor](https://clawhub.ai/user/0x-professor)

### License/Terms of Use:


## Use Case:

Security teams, incident responders, and developers use this skill to convert incident event logs into phase-classified timelines and stakeholder-ready response reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Incident data may contain untrusted content that is carried into generated reports.

Mitigation: Treat incident input as untrusted and prefer JSON output for sensitive reports.

Risk: Generated CSV or Markdown reports may be unsafe if opened or rendered with active content features.

Mitigation: Avoid opening generated CSV files directly in spreadsheet software and render Markdown with raw HTML and remote loading disabled.

Risk: Report output paths can overwrite existing files, including during dry-run use.

Mitigation: Choose output paths carefully and write reports to controlled directories.

## Reference(s):

- [IR Phase Guide](references/ir-phase-guide.md)
- [Cyber IR Playbook on ClawHub](https://clawhub.ai/0x-professor/skills/cyber-ir-playbook)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Guidance for incident-response reporting plus JSON, Markdown, or CSV report artifacts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled report script accepts JSON incident-event input and writes an output file in the selected format.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
