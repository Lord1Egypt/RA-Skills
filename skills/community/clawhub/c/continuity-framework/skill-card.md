## Description:

Continuity Framework supports asynchronous post-session reflection, structured memory extraction, question generation, and identity-state updates for agents that intentionally use persistent cross-session memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[riley-coyote](https://clawhub.ai/user/riley-coyote)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to add opt-in cross-session continuity workflows that reflect on recent sessions, persist structured memories and questions, and surface relevant context when a user returns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent cross-session memory may store conversation-derived identity, relationship, question, and reflection data without clear retention or deletion controls.

Mitigation: Install only when users intentionally opt into cross-session memory, treat the memory directory as sensitive, and periodically review or delete stored files.

Risk: Heartbeat reflection can analyze sessions after idle time and persist derived questions or identity notes.

Mitigation: Enable heartbeat reflection only with clear user opt-in, configure reflection thresholds and question limits, and avoid using it for sensitive sessions unless retention expectations are clear.

## Reference(s):

- [Continuity Framework reference](references/framework.md)
- [ClawHub skill page](https://clawhub.ai/riley-coyote/skills/continuity-framework)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [CLI text plus Markdown and JSON memory files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes persistent memory files under CONTINUITY_MEMORY_DIR or ~/clawd/memory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
