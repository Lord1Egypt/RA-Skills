## Description: <br>
Local-first recurring schedule engine for reminders, repeated tasks, and time-based execution plans. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[panchenbo](https://clawhub.ai/user/panchenbo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to capture recurring local reminders, task schedules, and time-based execution plans, then review, pause, resume, or inspect upcoming runs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Job titles, notes, schedules, run history, and stats are stored locally under ~/.openclaw/workspace/memory/cron. <br>
Mitigation: Avoid storing secrets or highly sensitive details in scheduled job metadata. <br>


## Reference(s): <br>
- [Cron Philosophy](references/philosophy.md) <br>
- [ClawHub skill page](https://clawhub.ai/panchenbo/cron-scheduler-local) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text and JSON from local Python CLI scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores job, run, and stats data locally under ~/.openclaw/workspace/memory/cron.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
