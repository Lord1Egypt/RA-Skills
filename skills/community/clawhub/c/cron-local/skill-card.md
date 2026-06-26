## Description: <br>
Local-first recurring schedule engine for reminders, repeated tasks, and time-based execution plans. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[morrison230](https://clawhub.ai/user/morrison230) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to capture recurring local reminders, repeated tasks, and time-based execution plans, then inspect, pause, resume, and list those schedules. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Schedule titles or notes may contain sensitive personal or operational details because job records are stored locally on disk. <br>
Mitigation: Avoid putting secrets or sensitive details in job titles or notes, and review local schedule records when handling sensitive workflows. <br>
Risk: An agent may create, pause, or resume schedules when a user only casually mentions timing. <br>
Mitigation: Confirm user intent before allowing the agent to create, pause, or resume schedules. <br>


## Reference(s): <br>
- [Cron Philosophy](references/philosophy.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration] <br>
**Output Format:** [Plain text and JSON-backed local schedule records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates local JSON files under ~/.openclaw/workspace/memory/cron; no external sync or third-party cron service is described.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
