## Description:

A local persona engine that models emotional and motivational state to support consistent character behavior across conversations, with an optional adaptive personality baseline.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nohn3043-arch](https://clawhub.ai/user/nohn3043-arch)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use the engine to model persistent persona states and keep character behavior coherent across long conversations and sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The guardian service exposes protected controls.

Mitigation: Fix guardian authentication before using the HTTP service with real minors or sensitive conversations.

Risk: Notification webhooks can target unsafe destinations.

Mitigation: Restrict webhook destinations to approved endpoints before enabling notifications.

Risk: Sensitive records may be inconsistently masked or retained.

Mitigation: Enforce accurate masking and scheduled retention, keep logs in a dedicated directory, and establish explicit deletion controls.

## Reference(s):

- [Persona Persistence](references/PersonaPersistence.md)
- [Emotion-Behavior Mapping](references/EmotionBehaviorMap.md)
- [Motive Conflict Rules](references/MotiveConflictRules.md)
- [Project homepage](https://github.com/nohn3043-arch/Anthropomorphic-Agent-Engine)

## Skill Output:

**Output Type(s):** [JSON, Text, Guidance]

**Output Format:** [Structured persona state and behavior guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Deterministic state output in the local core; optional language adapters are off by default.]

## Skill Version(s):

2.7.0 (source: release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
