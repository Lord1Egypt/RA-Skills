## Description:

Daily Plan Orchestrator creates PostgreSQL-backed daily plans from active task templates, carries unfinished work forward for up to 30 days, resets DRR scheduling state, and moves circuit-breaker tasks into half-open recovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to generate scheduled daily work plans, instantiate queued tasks from templates, handle carryover, and reset scheduling state for a multi-tenant task orchestration system.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill needs system-level PostgreSQL access that can read cross-tenant operational memory and task execution logs.

Mitigation: Install only where that access is intended, and require the publisher to document those reads and add tenant scoping or aggregate-only inputs before broad deployment.

Risk: The skill can automatically change queued task priorities based on growth insights.

Mitigation: Gate the growth-priority behavior behind explicit configuration and review its audit output before enabling it in production scheduling.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/daily-plan-orchestrator)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [JSON execution result with command-line invocation examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires PostgreSQL connection configuration through PG_DSN or DATABASE_URL.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
