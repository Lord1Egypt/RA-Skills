## Description:

Agent memory management protocol. Activate for any memory read, write, or update operation. Defines six-category write spec, L0 sync rules, and dedup strategy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ottoprua](https://clawhub.ai/user/ottoprua)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to keep OpenClaw agent memory structured across sessions, projects, preferences, entities, events, cases, and reusable patterns. It helps agents decide what to persist, where to write it, and how to retrieve it without reading every memory file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Durable memory can persist personal, project, and agent-behavior data too automatically.

Mitigation: Use explicit write triggers where possible, require approval before writes, and avoid storing secrets or regulated personal data.

Risk: Local memory, blackboard, lcm.db, and .learnings records can retain sensitive conversation or project history.

Mitigation: Define deletion and audit procedures for persistent records before installing the skill in sensitive workspaces.

Risk: External retrieval and compression tools affect how stored memory is indexed and recovered.

Mitigation: Pin and review qmd, LosslessClaw, and related OpenClaw configuration before deployment.

## Reference(s):

- [ClawHub: Agent Memory Protocol](https://clawhub.ai/ottoprua/skills/agent-memory-protocol)
- [MEMORY-STACK.md](MEMORY-STACK.md)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [OpenClaw Docs](https://docs.openclaw.ai)
- [qmd](https://github.com/tobilen/qmd)
- [LosslessClaw](https://github.com/martian-engineering/lossless-claw)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown protocol guidance with file paths, tables, and inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill directs agents to create or update structured memory, blackboard, event, case, pattern, and configuration records.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
