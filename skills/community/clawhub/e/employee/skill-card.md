## Description:

Create and manage virtual AI employees with persistent memory, defined roles, and graduated autonomy for hiring, training, and delegating tasks to specialized workers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to define, train, route tasks to, evaluate, and retire role-scoped virtual AI employees with persistent local memory and graduated autonomy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent local employee profiles, task logs, and memory may retain sensitive project or user context.

Mitigation: Review and prune memory and logs regularly, define retention rules, and avoid training employees on sensitive material without explicit controls.

Risk: Training documents or linked skills may influence delegated agents in unsafe or unintended ways.

Mitigation: Filter training inputs for prompt injection, pin or verify skill sources, and review employee memory before use on sensitive work.

Risk: High-autonomy employees can take file, messaging, spawning, or external actions beyond the user's intent if permissions are too broad.

Mitigation: Keep employees at draft-only or review autonomy until file access, messaging, spawning, and escalation rules are tightly scoped and tested.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/skills/employee)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON examples and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local employee profile, memory, registry, routing, and lifecycle guidance for an agent.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
