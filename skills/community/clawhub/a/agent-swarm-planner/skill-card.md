## Description:

Designs multi-agent system architectures with agent roles, communication paths, memory design, escalation protocols, operational schedules, and risk maps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[filipbl4gojevic](https://clawhub.ai/user/filipbl4gojevic)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, architects, and teams designing multi-agent workflows use this skill to turn a goal or workflow into a structured swarm architecture with roles, communication paths, memory, escalation, schedules, and risks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A generated architecture may allow a workflow to auto-proceed after a review timeout.

Mitigation: For swarms that affect money, users, accounts, production systems, or private data, require affirmative approval or halt on timeout.

Risk: Generated templates may include Resomnium branding or contact text.

Mitigation: Review generated documents and remove or replace third-party branding before adoption.

## Reference(s):

- [Agent Swarm Failure Patterns](artifact/references/failure-patterns.md)
- [Swarm Architecture Template](artifact/templates/swarm-architecture-template.md)
- [Agent Swarm Planner on ClawHub](https://clawhub.ai/filipbl4gojevic/skills/agent-swarm-planner)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown architecture document with tables, checklists, and structured sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No code execution; planning output should be reviewed before deployment.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
