## Description:

Use in Feishu chats when the assistant should stay responsive while longer work continues in the background by spawning one sub-agent task per substantial user prompt.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wd041216-bit](https://clawhub.ai/user/wd041216-bit)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill in Feishu-based agent chats to keep the foreground conversation responsive while substantial work continues asynchronously. It guides the agent to acknowledge quickly, spawn one child task per meaningful prompt, and report each task result independently.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Substantial Feishu requests may be moved to asynchronous child tasks, which can surprise users who expected a synchronous answer.

Mitigation: Tell users when work is being handled asynchronously and honor explicit requests for a synchronous response.

Risk: Long-running child tasks can leave users uncertain about progress.

Mitigation: Use periodic progress updates and inspect active child sessions when users ask for status.

## Reference(s):

- [OpenClaw Session Tool documentation](https://docs.openclaw.ai/session-tool)
- [ClawHub skill page](https://clawhub.ai/wd041216-bit/skills/feishu-parallel-dispatch)

## Skill Output:

**Output Type(s):** [Guidance, Text]

**Output Format:** [Markdown guidance with short acknowledgement examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces procedural dispatch guidance for spawning and tracking background child tasks; it does not generate code or configuration files.]

## Skill Version(s):

1.0.1 (source: server release evidence and artifact/skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
