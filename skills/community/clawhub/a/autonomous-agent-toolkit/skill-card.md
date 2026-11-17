## Description:

Create, configure, and orchestrate autonomous AI agents on OpenClaw, including personas, memory systems, cron schedules, and multi-agent teams.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crispyangles](https://clawhub.ai/user/crispyangles)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to scaffold autonomous agent workspaces, define agent personas and memory files, configure scheduled OpenClaw cron jobs, and coordinate multi-agent teams.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled autonomous prompts can persistently modify files or trigger external actions with weak scope boundaries.

Mitigation: Restrict cron jobs to explicit read/write paths, require human approval for posting or external actions, and review each cron prompt before enabling it.

Risk: Generated agent rules may allow broad task execution or workspace changes unless customized.

Mitigation: Tighten SOUL.md and AGENTS.md red lines, scope limits, audit logging, and approval requirements before running the generated agent.

Risk: The generator's name and path handling may be unsafe for untrusted inputs.

Mitigation: Use trusted agent names and output paths, keep generated workspaces under version control, and patch or avoid the unsafe path handling before broader deployment.

## Reference(s):

- [Cron Patterns for Autonomous Agents](references/cron-patterns.md)
- [SOUL.md Patterns & Templates](references/soul-patterns.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and generated workspace files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces agent workspace files such as SOUL.md, AGENTS.md, HEARTBEAT.md, USER.md, MEMORY.md, and memory logs when the bundled generator is run.]

## Skill Version(s):

3.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
