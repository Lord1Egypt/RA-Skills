## Description:

Agent resilience patterns for surviving context loss, capturing critical details, and self-improvement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xinian5216](https://clawhub.ai/user/xinian5216)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to preserve task state, capture important corrections and decisions, recover after context loss, and improve agent behavior during complex or long-running work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to persist broad conversation details and raw exchanges in local memory files, which can expose sensitive data if used in unsuitable workspaces.

Mitigation: Use only in workspaces where persistent local notes are acceptable, and avoid recording secrets, credentials, private URLs, regulated data, or sensitive personal or business information.

Risk: Recovered notes may carry stale or overbroad context into later work.

Mitigation: Scope session state to the active task, reset it for unrelated work, and review recovered notes before acting on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xinian5216/skills/agent-resilience)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Text]

**Output Format:** [Markdown guidance and local memory notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce persistent local session-state and working-buffer notes when used by an agent.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
