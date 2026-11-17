## Description:

Audit and improve your OpenClaw setup with one skill by scoring agent health, auditing memory hygiene, checking cron reliability, and comparing installed skills against ClawHub with conservative fixes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zihaofeng2001](https://clawhub.ai/user/zihaofeng2001)

### License/Terms of Use:

CC BY-SA 4.0

## Use Case:

Developers and agent operators use this skill to audit an OpenClaw workspace, identify memory, cron, skill, security, and continuity issues, and generate prioritized recommendations or conservative cron fixes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill scans OpenClaw workspace memory, cron, skill metadata, and continuity files and writes audit reports into memory/.

Mitigation: Run it only in workspaces where these files may be inspected and retained as local diagnostic reports.

Risk: The skill comparator queries ClawHub with installed skill names to compare community signals.

Mitigation: Avoid running the comparator when installed skill names should not be sent to the public ClawHub API.

Risk: The cron optimizer can edit cron jobs when explicitly run with --fix.

Mitigation: Review proposed cron changes first and rely on the generated memory/cron-backup.json before accepting repairs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zihaofeng2001/skills/agent-health-optimizer)
- [ClawHub API](https://clawhub.ai/api/v1/)
- [proactive-agent](https://clawhub.ai/halthelobster/proactive-agent)
- [self-improving-agent](https://clawhub.ai/pskoett/self-improving-agent)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Console text and Markdown guidance with JSON report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes audit reports to memory/ and can modify cron jobs only when explicitly run with --fix.]

## Skill Version(s):

1.4.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
