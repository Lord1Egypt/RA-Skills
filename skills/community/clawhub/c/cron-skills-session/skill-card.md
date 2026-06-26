## Description: <br>
Standardizes OpenClaw cron job entries to always use the current user session as target when creating or editing scheduled tasks, reminders, or recurring checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thegoaldev](https://clawhub.ai/user/thegoaldev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and agent operators use this skill to create or update local OpenClaw cron jobs that deliver scheduled agent turns to the active user session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates persistent local scheduled agent turns by editing OpenClaw cron configuration and restarting the gateway. <br>
Mitigation: Install only when local OpenClaw cron management is intended; review scheduled jobs periodically and remove or disable entries that are no longer wanted. <br>
Risk: Incorrect schedule, payload, or session-target values can cause missed, repeated, or misdirected reminders. <br>
Mitigation: Validate ~/.openclaw/cron/jobs.json after edits, keep the required user-session target, and update nextRunAtMs when changing recurring intervals. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thegoaldev/cron-skills-session) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Directs edits to ~/.openclaw/cron/jobs.json and validation before gateway restart.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
