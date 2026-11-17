## Description:

Asynchronous reflection and memory integration for genuine AI development. Use on heartbeat to reflect on recent sessions, extract structured memories with confidence scores, generate follow-up questions, and surface those questions when the user returns. Transforms passive logging into active development.

This skill is ready for commercial/non-commercial use.

## Publisher:

[riley-coyote](https://clawhub.ai/user/riley-coyote)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to add a local continuity workflow that reflects on recent sessions, extracts structured memories, tracks identity notes, and surfaces follow-up questions at the start of later sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may retain personal conversation-derived memories across sessions.

Mitigation: Enable it only with explicit intent, use a dedicated memory directory, and review stored questions, identity notes, and reflection logs.

Risk: Persistent memory files may contain secrets, regulated data, or stale personal context if users place sensitive material in sessions.

Mitigation: Avoid storing secrets or regulated data and define a deletion or retention process before using heartbeat-based reflection.

## Reference(s):

- [The Continuity Framework](references/framework.md)
- [Continuity Framework on ClawHub](https://clawhub.ai/riley-coyote/skills/continuity)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash commands, environment configuration, and local text or JSON memory files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local memory state, pending questions, identity notes, and reflection logs under the configured continuity memory directory.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
