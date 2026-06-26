## Description: <br>
Elephantastic is a Taskwarrior-based executive-function stack for AI agents that supports task capture, prioritization, session handoff, learning review, and vitality checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lux-sp4rk](https://clawhub.ai/user/lux-sp4rk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to give an AI agent a local, auditable task-management loop with Taskwarrior-backed next actions, error capture, periodic review, and session continuity. It is useful when an agent needs structured persistence across sessions instead of relying only on volatile context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The server security summary reports that this release presents a deprecated rename notice while still bundling active scripts that can read activity data and change or delete local Taskwarrior tasks. <br>
Mitigation: Install elephantastic directly when only the renamed skill is needed; otherwise review the bundled scripts before invocation and run them only against Taskwarrior data you are prepared to let the agent inspect or modify. <br>
Risk: The security guidance says the package can inspect Timewarrior or heartbeat activity and participate in scheduled monitoring if cron is configured. <br>
Mitigation: Configure heartbeat monitoring deliberately, review mission-hour and silence-threshold settings, and avoid enabling scheduled execution until local notification and privacy expectations are clear. <br>
Risk: Taskwarrior actions can modify or delete local tasks, including agent memory and operational backlog entries. <br>
Mitigation: Keep Taskwarrior backups or versioned exports, use gated tasks for actions requiring approval, and review proposed task changes before allowing destructive operations. <br>


## Reference(s): <br>
- [Elephantastic ClawHub listing](https://clawhub.ai/lux-sp4rk/elephantastic) <br>
- [Taskwarrior](https://taskwarrior.org) <br>
- [Taskwarrior Schema Reference](references/taskwarrior-schema.md) <br>
- [Periodic Review Runbook](references/review-runbook.md) <br>
- [Vitality Heartbeat](references/vitality-heartbeat.md) <br>
- [Sovereign Agent Executive Stack](references/executive-stack.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, Taskwarrior configuration snippets, and JSON command output from bundled helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read or update local Taskwarrior data and may inspect Timewarrior or heartbeat activity when configured.] <br>

## Skill Version(s): <br>
1.1.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
