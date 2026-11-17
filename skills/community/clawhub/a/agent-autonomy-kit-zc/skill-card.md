## Description:

Stop waiting for prompts. Keep working.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lean-zhouchao](https://clawhub.ai/user/lean-zhouchao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to set up a task queue, proactive heartbeat routine, and scheduled work patterns so agents can continue research, writing, analysis, code review, and coordination between prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled autonomous runs can continue work across sessions without a fresh human prompt.

Mitigation: Enable cron examples only where autonomous work is intended, prefer isolated sessions for scheduled jobs, and document how to list and remove those jobs.

Risk: A mutable task queue can cause agents to pick up work that has not been reviewed or approved.

Mitigation: Review queue items before execution, keep approval-dependent work in a blocked state, and require clear task ownership before moving items into progress.

Risk: Long-running autonomous work can consume tokens or runtime unexpectedly.

Mitigation: Cap runtime and token use, schedule active hours, and require handoff notes before the agent sleeps or reaches limits.

Risk: Autonomous workflows may expose sensitive workspace data if enabled in a privileged environment.

Mitigation: Restrict the agent's permissions, avoid sensitive credentials in the workspace, and install only in environments intended for autonomous operation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lean-zhouchao/skills/agent-autonomy-kit-zc)
- [Publisher profile](https://clawhub.ai/user/lean-zhouchao)
- [Homepage listed in skill metadata](https://github.com/itskai-dev/agent-autonomy-kit)
- [Agent Autonomy Kit repository linked in README](https://github.com/reflectt/agent-autonomy-kit)
- [Agent Memory Kit](https://github.com/reflectt/agent-memory-kit)
- [Agent Team Kit](https://github.com/reflectt/agent-team-kit)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell and JSON-style configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes queue and heartbeat templates plus guidance for scheduled autonomous work.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
