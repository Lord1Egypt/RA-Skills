## Description: <br>
Configure, diagnose, and fix OpenClaw cron jobs for scheduled tasks, periodic jobs, timing issues, and time-based automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mayf3](https://clawhub.ai/user/mayf3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to create, validate, troubleshoot, and repair cron job configurations for recurring agent tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cron repair scripts can modify OpenClaw scheduled job configuration and change recurring task behavior. <br>
Mitigation: Confirm the intended job scope before applying fixes, prefer the safe or validation-backed repair scripts, keep the generated backup, and validate the result before restarting the gateway. <br>
Risk: Timezone defaults may not match the user's intended schedule. <br>
Mitigation: Confirm the desired timezone before creating or fixing jobs and replace Asia/Shanghai when another timezone is intended. <br>
Risk: Stateless cron prompts can repeat work, lose context, or produce non-actionable output. <br>
Mitigation: Require each cron prompt to define state persistence through a cursor, checkpoint, append-only log, idempotent comparison, or similar file-backed mechanism. <br>


## Reference(s): <br>
- [Cron Job Syntax Guide](references/syntax-guide.md) <br>
- [Cron Job Troubleshooting Guide](references/troubleshooting.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/mayf3/cron-helper-mayf3) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with JSON and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May recommend bundled validation and repair scripts for OpenClaw cron job changes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
