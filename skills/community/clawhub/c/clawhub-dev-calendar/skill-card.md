## Description:

Create detailed ClawHub skill development calendars with milestones, Saskatchewan holidays, America/Regina timezone, and export to ICS, PDF, HTML, or visuals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skunnyo](https://clawhub.ai/user/skunnyo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill authors use this skill to plan ClawHub/OpenClaw skill development timelines, client delivery schedules, and calendar exports for project milestones.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated ICS files may contain unsafe or malformed calendar text when created from untrusted project JSON.

Mitigation: Use trusted project data, review generated .ics content before importing or sharing it, and update the generator to escape ICS text fields and use opaque UIDs when handling untrusted input.

## Reference(s):

- [ClawHub Dev Calendar release page](https://clawhub.ai/skunnyo/skills/clawhub-dev-calendar)
- [ClawHub Skill Development Milestones](references/dev_milestones.md)
- [Saskatchewan statutory holidays](references/sask_holidays.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with inline shell commands, JSON project configuration, and generated calendar files such as ICS, HTML, PDF, PNG, or text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated ICS calendars include project milestones and Saskatchewan statutory holidays; generated content should be reviewed before importing or sharing.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
