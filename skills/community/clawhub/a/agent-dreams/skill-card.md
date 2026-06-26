## Description: <br>
Strategies for productive agent idle time using heartbeats and cron jobs for proactive behaviors, scheduled background tasks, and agent work during idle periods. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JPaulGrayson](https://clawhub.ai/user/JPaulGrayson) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to define heartbeat checklists, cron schedules, and boundaries for proactive agent work such as inbox checks, memory maintenance, system monitoring, and recurring summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recurring background checks may access private accounts, local files, system state, and git activity without enough scoping or consent controls. <br>
Mitigation: Before enabling the skill, define exact heartbeat or cron tasks, approved accounts and folders, read/write limits, logging, expiration dates, and a clear off switch. <br>
Risk: Scheduled agent activity could send messages, post publicly, delete or reorganize files, commit git changes, make purchases, or take other irreversible actions. <br>
Mitigation: Require explicit approval before external communication, public posting, file deletion or reorganization, git commits, purchases, transfers, or any irreversible action. <br>


## Reference(s): <br>
- [Agent Dreams on ClawHub](https://clawhub.ai/JPaulGrayson/agent-dreams) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline code blocks and tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes heartbeat checklist, state-file template, cron expressions, proactive work categories, quiet-hours guidance, and setup steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
