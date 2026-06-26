## Description: <br>
Complex task orchestration and subagent command framework. Execute multi-stage complex tasks via subagent (sessions_spawn), including task breakdown, state management, checkpoint-driven, timeout retry, auto-progress and sync. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[miyan1221](https://clawhub.ai/user/miyan1221) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to coordinate long-running, multi-stage agent work with task breakdown, checkpoints, retries, progress monitoring, and unattended continuation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unattended subagent automation may continue work, trigger cron or heartbeat tasks, or make operational changes without timely user review. <br>
Mitigation: Install only in a controlled workspace, review each scheduled task before enabling it, and require explicit approval for commits, pushes, external messaging, gateway restarts, and account or admin changes. <br>
Risk: Timeout-based fallback or silent device approval can weaken user control over sensitive decisions. <br>
Mitigation: Do not enable silent device auto-approval and do not treat timeout as consent for sensitive actions. <br>
Risk: Shared agent configuration can expose credentials or broaden credential scope. <br>
Mitigation: Keep API keys out of shared configuration when possible and scope any required secrets to the minimum workspace and task. <br>
Risk: Generated shell commands and configuration edits can affect local agent, cron, heartbeat, cache, notification, or gateway behavior. <br>
Mitigation: Review proposed commands and configuration diffs manually before execution, especially changes that restart services or alter automation permissions. <br>


## Reference(s): <br>
- [Complex Task Subagent on ClawHub](https://clawhub.ai/miyan1221/complex-task-subagent) <br>
- [Publisher profile](https://clawhub.ai/user/miyan1221) <br>
- [Quick Start](references/quick-start.md) <br>
- [Advanced Patterns](references/advanced-patterns.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, configuration examples, and operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose unattended cron, heartbeat, checkpoint, notification, and cache-management workflows for an agent environment.] <br>

## Skill Version(s): <br>
2.0.1 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
