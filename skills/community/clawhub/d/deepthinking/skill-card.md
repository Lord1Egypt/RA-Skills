## Description:

A stateful, neuro-inspired thinking framework that guides users through excavation, architecture, and synthesis phases for complex problem-solving.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bruno-nimbledev](https://clawhub.ai/user/bruno-nimbledev)

### License/Terms of Use:


## Use Case:

External users use this skill to work through complex decisions, ambiguous ideas, and personal or professional uncertainty through structured coaching-style questions. It persists local session state and memory so the agent can pause, resume, and tailor later sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores and reuses sensitive personal reflections and inferred behavior patterns across sessions.

Mitigation: Review ~/.deepthinking regularly, inspect the semantic profile before relying on it, and delete or protect the directory when long-term memory is not desired.

Risk: Optional cron or systemd persistence can extend local memory consolidation beyond an interactive session.

Mitigation: Enable scheduled evolution only when needed, keep it under the normal user account, and avoid sudo for routine setup.

Risk: The skill has no server-provided license identifier.

Mitigation: Confirm license and terms before deployment or redistribution.

## Reference(s):

- [Cognitive Modules Reference](artifact/references/modules.md)
- [ClawHub skill page](https://clawhub.ai/bruno-nimbledev/skills/deepthinking)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and locally persisted state files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local files under ~/.deepthinking for session state, memory, archives, and evolution data.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
