## Description:

Complex Task Subagent helps agents orchestrate multi-stage OpenClaw tasks with subagents, checkpoints, timeout retries, progress monitoring, and recovery-oriented state management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[miyan1221](https://clawhub.ai/user/miyan1221)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to coordinate long-running or multi-phase OpenClaw work through subagents, task progress files, checkpoints, cron or heartbeat scheduling, and recovery workflows. It is suited to serial or staged automation where the agent needs explicit state tracking and restartable progress.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can configure persistent unattended agent behavior that may continue after user silence.

Mitigation: Use it only in a test or tightly controlled OpenClaw environment, and require an expiry and rollback plan for task-specific heartbeat instructions.

Risk: The skill includes guidance that weakens device pairing through silent device auto-approval.

Mitigation: Do not enable silent device auto-approval unless a human reviewer has accepted the operational risk for a controlled environment.

Risk: Timeout-based escalation can shift important decisions into unattended execution.

Mitigation: Do not allow timeout-based escalation for critical actions; require explicit user approval before those actions proceed.

Risk: Bundled scripts and reference snippets are flagged as unsafe until path validation, eval removal, and credential-handling guidance are fixed.

Mitigation: Review and scan the skill before deployment, validate paths before running scripts, and avoid using real credentials in examples or test runs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/miyan1221/skills/complex-task-subagent)
- [Quick Start](references/quick-start.md)
- [Advanced Patterns](references/advanced-patterns.md)
- [Troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON snippets, shell command examples, and configuration instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide creation of task progress, checkpoint, cache, notification, and OpenClaw configuration files when the user executes the provided commands.]

## Skill Version(s):

2.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
