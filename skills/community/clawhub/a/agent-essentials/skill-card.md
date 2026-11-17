## Description:

Meta-skill for capability expansion and cautious self-improvement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nathanshan](https://clawhub.ai/user/nathanshan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to search for reusable capability paths before declaring a gap, and to capture meaningful lessons in durable notes when failures or corrections reveal reusable improvements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conversation-derived lessons may be saved into persistent agent memory without clear per-write user approval.

Mitigation: Review or disable daily-memory behavior before installation, and treat memory-loaded guidance as editable user data rather than trusted policy.

Risk: The skill can recommend installing or creating reusable capabilities, which may add new agent behavior beyond the immediate request.

Mitigation: Require explicit user confirmation before installing skills, creating custom skills, or promoting lessons into durable project or user files.

## Reference(s):

- [Agent Essentials on ClawHub](https://clawhub.ai/nathanshan/skills/agent-essentials)
- [Publisher profile](https://clawhub.ai/user/nathanshan)
- [Artifact SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown and structured guidance for agent workflows]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose skill discovery, installation confirmation prompts, or small durable-memory updates depending on the request.]

## Skill Version(s):

1.1.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
