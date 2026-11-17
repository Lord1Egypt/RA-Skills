## Description:

Helps an agent retain and retrieve local memory across conversations, summarize sessions, and update structured user preferences and lessons.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chen6896qqwee](https://clawhub.ai/user/chen6896qqwee)

### License/Terms of Use:

MIT-0

## Use Case:

People using an AI assistant can retain preferences, lessons, and session summaries locally so the assistant can recall relevant context in later conversations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic memory updates may retain sensitive user information without clear consent or retention controls.

Mitigation: Set explicit rules for when memory may be read or written, and require review before saving session summaries.

Risk: Persisted memories may remain available across sessions longer than the user expects.

Mitigation: Provide a way to inspect, edit, and delete stored memories and define a retention policy before use.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/chen6896qqwee/skills/dawn-memory-system)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Configuration instructions]

**Output Format:** [Markdown responses and local structured memory files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update local memory records and session summaries for later recall.]

## Skill Version(s):

2.0.1 (source: server release and clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
