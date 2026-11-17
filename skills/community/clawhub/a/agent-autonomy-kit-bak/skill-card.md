## Description:

Helps agent operators configure persistent task queues, proactive heartbeat routines, and scheduled work triggers for self-directed agent progress.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lean-zhouchao](https://clawhub.ai/user/lean-zhouchao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to set up a persistent task queue, heartbeat checklist, and scheduled routines for agents that continue meaningful work between direct human prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring unattended jobs may cause an agent to act beyond the intended scope.

Mitigation: Enable heartbeat or cron routines only after restricting session scope, tools, filesystem access, network access, messaging access, queue writers, runtime, and worker spawning.

Risk: Queued tasks can become instructions that drive file-changing workflows without immediate human review.

Mitigation: Review queued tasks before execution, keep human requests and blockers prioritized, and require clear Done or Blocked updates in the queue.

Risk: Scheduled autonomous work can continue after it is no longer desired.

Mitigation: Document a clear pause or removal path for scheduled jobs before enabling recurring triggers.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lean-zhouchao/skills/agent-autonomy-kit-bak)
- [Publisher profile](https://clawhub.ai/user/lean-zhouchao)
- [README](artifact/README.md)
- [Proactive heartbeat template](artifact/templates/HEARTBEAT.md)
- [Task queue template](artifact/templates/QUEUE.md)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes queue and heartbeat templates for agent workflow setup.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
