## Description:

ARCHITECT helps an OpenClaw agent decompose high-level goals into dependency-aware tasks, execute them with validation, adapt on failure, and synthesize complete results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[contrario](https://clawhub.ai/user/contrario)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to turn a high-level goal into a scoped mission brief, task graph, execution loop, validation steps, and final deliverable. It is intended for agents that should work more proactively while still requiring confirmation for irreversible or external actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill encourages broad autonomous planning and execution, which can lead an agent to take a more proactive posture than a user expects.

Mitigation: Use it only when proactive planning is desired, state the scope up front, and require confirmation before memory writes or sensitive work.

Risk: Agent outputs may include proposals to send, publish, delete, use credentials, or otherwise change external state.

Mitigation: Require explicit user approval before any external, irreversible, credentialed, or state-changing action.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/contrario/skills/agent-architect)
- [Publisher Profile](https://clawhub.ai/user/contrario)
- [README](artifact/README.md)
- [Examples](artifact/EXAMPLES.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown text with structured task headers, plans, findings, code blocks, shell commands, and final deliverables as needed.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No bundled code, dependencies, environment variables, or hidden install behavior; the skill changes agent behavior through prompt instructions.]

## Skill Version(s):

1.0.4 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
