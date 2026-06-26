## Description: <br>
Autonomous agent health, optimization, and cleanup for scheduled maintenance, manual health checks, stale session cleanup, context compaction, process monitoring, and performance reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[robshabbir](https://clawhub.ai/user/robshabbir) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to monitor OpenClaw agent health, clean up stale sub-agents and long-running processes, report session health, and record periodic retrospectives. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recurring autonomous maintenance can terminate sub-agents or processes without enough scoping or approval controls. <br>
Mitigation: Start with manual or dry-run operation, require confirmation before termination actions, and limit cleanup to resources clearly owned by this workflow. <br>
Risk: A frequent cron schedule can repeatedly grant the skill authority to clean up resources and write memory notes. <br>
Mitigation: Review the cron configuration before enabling it and audit any memory files or schedules the skill creates. <br>


## Reference(s): <br>
- [Agent Self-Care on ClawHub](https://clawhub.ai/robshabbir/agent-self-care) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown report with inline shell commands and JSON cron configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports sub-agent status, process cleanup, context usage, health state, and retrospective status.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
