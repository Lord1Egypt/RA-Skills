## Description: <br>
Monitors OpenClaw cron job health, identifies failures, timeouts, and delivery issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qinthqod](https://clawhub.ai/user/qinthqod) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to check OpenClaw cron job run history, spot failures or timeouts, and verify that scheduled jobs are healthy after fixes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local OpenClaw cron job configuration and run logs, which may include operational status and error details. <br>
Mitigation: Use it only in environments where the agent is allowed to read and display local OpenClaw cron error logs. <br>
Risk: The release slug differs from the artifact metadata slug. <br>
Mitigation: Confirm the intended Fox Cron Health Check package and publisher before installing or scheduling recurring checks. <br>
Risk: Recurring execution can repeatedly inspect cron health without a manual trigger. <br>
Mitigation: Enable the recurring schedule only when periodic automated checks are desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qinthqod/fox-cron-health-check) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Plain text or JSON health report with status, issue summaries, suggested fixes, and process exit codes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can analyze a caller-selected time window and can be run manually or on a recurring schedule.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
