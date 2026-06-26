## Description: <br>
Guides agents through OpenClaw cron scheduling for one-shot reminders, recurring background tasks, session targeting, delivery modes, failure alerts, and troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fuzzyb33s](https://clawhub.ai/user/fuzzyb33s) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to create, inspect, update, and troubleshoot OpenClaw cron jobs for reminders, heartbeats, recurring checks, webhook notifications, and project digests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scheduled jobs may read workspace data or trigger actions repeatedly in the background. <br>
Mitigation: Confirm the schedule, data access, action scope, delivery mode, and disable or removal path before enabling each job. <br>
Risk: Webhook delivery can expose results or sensitive workspace context to external endpoints. <br>
Mitigation: Use only trusted webhook URLs and avoid sending secrets or sensitive workspace contents. <br>
Risk: Overly frequent recurring jobs can create unnecessary cost, noise, or operational load. <br>
Mitigation: Batch related checks, choose the least frequent practical schedule, and configure failure alerts with cooldowns for critical jobs. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/fuzzyb33s/fuzzy-cron-scheduler) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, code, shell commands] <br>
**Output Format:** [Markdown with cron_add examples and command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces scheduling recipes, cron expressions, OpenClaw cron function examples, and troubleshooting guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
