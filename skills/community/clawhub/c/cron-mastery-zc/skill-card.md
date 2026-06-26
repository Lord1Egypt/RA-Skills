## Description: <br>
Master OpenClaw's timing systems. Use for scheduling reliable reminders, setting up periodic maintenance (janitor jobs), and understanding when to use Cron vs Heartbeat for time-sensitive tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lean-zhouchao](https://clawhub.ai/user/lean-zhouchao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to choose between OpenClaw Cron and Heartbeat timing patterns, schedule reliable reminders, configure recurring tasks, and troubleshoot cron delivery behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reusable templates include a fixed Telegram recipient and could send reminders or summaries to the wrong destination if copied unchanged. <br>
Mitigation: Replace every recipient value with a verified destination before scheduling any delivery job. <br>
Risk: The email-summary example can trigger mailbox access and external message delivery. <br>
Mitigation: Use the email-summary pattern only after explicitly approving mailbox access, delivery channel, recipient, and schedule. <br>
Risk: Janitor and state-file deletion guidance can remove scheduled jobs or cron state. <br>
Mitigation: Back up cron state and confirm which jobs may be deleted before running cleanup or state-file deletion steps. <br>


## Reference(s): <br>
- [Cron Examples & Templates](references/templates.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/lean-zhouchao/cron-mastery-zc) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, shell commands] <br>
**Output Format:** [Markdown with JSON examples and troubleshooting steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes reusable cron payload templates for reminders, maintenance jobs, and recurring asynchronous tasks.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
