## Description: <br>
Schedule OpenClaw tasks using natural language with cron lifecycle management, timezone support, failure alerts, and execution logs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mariusfit](https://clawhub.ai/user/mariusfit) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to schedule recurring OpenClaw tasks from plain-English recurrence expressions, inspect upcoming runs and logs, and manage the pause, resume, remove, and manual-run lifecycle for recurring automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent unattended execution through system cron can run scheduled tasks later without another prompt. <br>
Mitigation: Review each scheduled task before enabling it, confirm the schedule and task text, and keep jobs easy to list, inspect, pause, and remove. <br>
Risk: Broad task authority can make cleanup, deletion, or maintenance jobs affect unintended files or services. <br>
Mitigation: Use tightly scoped paths and commands, avoid broad deletion jobs unless backups exist, and verify sensitive jobs manually before scheduling. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mariusfit/clawhub-skill-smart-cron) <br>
- [Source Repository](https://github.com/mariusfit/smart-cron) <br>
- [Issue Tracker](https://github.com/mariusfit/smart-cron/issues) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell command examples and configuration JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create persistent local schedules, job configuration, and execution logs through system cron and OpenClaw orchestration.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version and artifact/skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
