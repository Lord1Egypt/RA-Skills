## Description:

Dida Agent Optimizer helps diagnose OpenClaw agent execution failures across cron jobs, tool calls, interrupted workflows, performance degradation, and system health, then proposes repairs and captures reusable lessons.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tuobadaidai](https://clawhub.ai/user/tuobadaidai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to triage OpenClaw runtime issues, inspect logs and health checks, prepare repair commands, and verify fixes after human approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled self-update behavior can persistently change skill behavior or references.

Mitigation: Require human review before enabling cron or heartbeat integration and review any web-derived update content before applying it.

Risk: Repair commands can modify cron jobs, restart services, run Docker cleanup, or delete local files.

Mitigation: Require explicit approval for service restarts, cron changes, Docker cleanup, SKILL.md or references changes, and any file deletion.

Risk: Diagnostic or repair guidance may be incorrect for the local OpenClaw environment.

Mitigation: Treat outputs as proposals, apply the smallest reversible change, and verify results with the listed health checks and run history.

## Reference(s):

- [Dida Agent Optimizer on ClawHub](https://clawhub.ai/tuobadaidai/skills/dida-agent-optimizer)
- [Trigger Integration](TRIGGER-INTEGRATION.md)
- [Anthropic Engineering Patterns](references/anthropic-patterns.md)
- [OpenAI Agent Engineering Best Practices](references/openai-patterns.md)
- [Error Taxonomy and Handling Strategies](references/error-taxonomy.md)
- [Common Fix Templates](references/fix-templates.md)
- [Self-Evolution Workflow](references/self-evolution.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands and checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include diagnostic decision trees, repair proposals, verification steps, and concise reports.]

## Skill Version(s):

1.1.0 (source: server release evidence; artifact version table lists v1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
