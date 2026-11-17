## Description:

Teaches when to recall from long-term memory before acting and when to save durable decisions, corrections and failures afterwards. Use when a memory tool or MCP memory server is connected but the agent is not using it consistently, when the user complains that the assistant forgets preferences, conventions or past decisions between sessions, or when setting up persistent memory for a project. Works with any memory backend: a folder of Markdown files, a local MCP server, or a managed service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[olyati](https://clawhub.ai/user/olyati)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams configuring agents with persistent memory use this skill to make recall and memory writeback consistent across sessions while avoiding stale, unsafe, or overly broad memories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A memory backend can persist secrets, tokens, personal data, project decisions, or user preferences beyond the current task.

Mitigation: Use a trusted backend and do not save secrets, tokens, personal data, temporary task details, or information the user marked as transient.

Risk: Outdated or conflicting memories can lead an agent to apply stale conventions or silently choose between incompatible instructions.

Mitigation: Close superseded memories instead of overwriting them, keep dates and sources, and surface conflicting memories for user review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/olyati/skills/agent-memory-discipline)
- [Mnemoverse](https://mnemoverse.com)

## Skill Output:

**Output Type(s):** [Guidance, Markdown]

**Output Format:** [Markdown guidance and checklist text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Backend-agnostic memory usage rules; no code execution.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact metadata version 1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
