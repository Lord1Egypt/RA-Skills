## Description: <br>
Local-first recurring schedule engine for reminders, repeated tasks, and time-based execution plans. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ProjectSnowWork](https://clawhub.ai/user/ProjectSnowWork) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, developers, and personal automation users use this skill to capture recurring reminders, repeated tasks, routines, and time-based plans as local schedules with next-run visibility and pause/resume controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill records job titles, notes, tags, and schedule metadata in persistent local JSON files. <br>
Mitigation: Avoid storing secrets in job text, review local file permissions, and clear or archive the cron memory files when the data is no longer needed. <br>
Risk: The skill computes and stores schedules but is not itself a background runner or system cron replacement. <br>
Mitigation: Use a separate reviewed execution service if jobs must run automatically, and treat this skill as schedule memory unless that service is added. <br>


## Reference(s): <br>
- [Cron Philosophy](artifact/references/philosophy.md) <br>
- [ClawHub skill page](https://clawhub.ai/ProjectSnowWork/cron) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON, guidance] <br>
**Output Format:** [Markdown guidance with Python CLI command examples and JSON-backed schedule records.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local schedule-management commands and status summaries; bundled scripts persist job, run, and stats JSON under ~/.openclaw/workspace/memory/cron.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact/skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
