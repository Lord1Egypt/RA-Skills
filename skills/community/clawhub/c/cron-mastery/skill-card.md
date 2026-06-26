## Description: <br>
Master OpenClaw's timing systems. Use for scheduling reliable reminders, setting up periodic maintenance (janitor jobs), and understanding when to use Cron vs Heartbeat for time-sensitive tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[i-mw](https://clawhub.ai/user/i-mw) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to choose between heartbeat checks and cron schedules, build reliable reminders, configure recurring summaries or maintenance jobs, and troubleshoot cron timing issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scheduled jobs can wake an agent later or send external notifications without additional context. <br>
Mitigation: Require explicit user approval for recurring email, news, or notification jobs and review destination fields before scheduling. <br>
Risk: Examples include hard-coded external delivery details. <br>
Mitigation: Replace hard-coded Telegram IDs before use and avoid publishing personal identifiers in job templates. <br>
Risk: Troubleshooting and maintenance examples include privileged cleanup and destructive cron state recovery. <br>
Mitigation: Preview janitor cleanup, back up jobs.json, and treat cron state deletion as privileged maintenance. <br>


## Reference(s): <br>
- [Cron Examples & Templates](references/templates.md) <br>
- [Cron Mastery on ClawHub](https://clawhub.ai/i-mw/cron-mastery) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Configuration] <br>
**Output Format:** [Markdown with JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include OpenClaw cron job payloads, timezone reminders, and maintenance guidance.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
