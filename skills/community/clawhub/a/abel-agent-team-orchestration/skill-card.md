## Description:

Orchestrates multi-agent teams with defined roles, task lifecycles, handoff protocols, and review workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abeltennyson](https://clawhub.ai/user/abeltennyson)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to set up sustained multi-agent workflows with clear roles, task states, handoffs, shared artifacts, and review gates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Model prompts and task context may be routed through the SkillBoss API Hub, including proprietary code, customer data, credentials, or internal business context.

Mitigation: Use the skill only where this third-party routing is approved, and define redaction, retention, approved endpoints, and data-handling boundaries before use.

Risk: Recurring operations patterns can dispatch work or summarize team state on a schedule without clear operating boundaries.

Mitigation: Define schedule limits, approved actions, escalation paths, and owner review before enabling recurring standups, dispatch, or health checks.

Risk: Multi-agent handoffs can lose context or artifacts, leading to incomplete or incorrect work.

Mitigation: Require exact output paths, handoff summaries, verification commands, known-issue notes, and reviewer approval before marking work done.

## Reference(s):

- [Team Setup](references/team-setup.md)
- [Task Lifecycle](references/task-lifecycle.md)
- [Communication](references/communication.md)
- [Patterns](references/patterns.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with templates, checklists, task flows, and inline command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce role definitions, spawn prompts, task-state templates, handoff checklists, review workflows, and operating procedures.]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
