## Description:

Saves, restores, and lists local Markdown summaries for chat-session handoffs and project continuity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bayllech](https://clawhub.ai/user/bayllech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to preserve work state across account switches, cleared sessions, new chats, or project handoffs by saving concise local session or project summaries and restoring them later.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe slot or project names could cause the agent to read or overwrite unintended Markdown files.

Mitigation: Use simple names without slashes, '..', or other path characters, and verify resolved paths remain inside the intended handoff or project directories before reading or writing.

Risk: Default overwrite behavior could replace an existing saved context unexpectedly.

Mitigation: Confirm the target slot or project name before saving and ask before overwriting existing files when the prior content may matter.

Risk: Saved summaries could accidentally include secrets or sensitive account material.

Mitigation: Exclude tokens, keys, cookies, complete credentials, and other sensitive values from generated summaries.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bayllech/skills/context-handoff)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Guidance]

**Output Format:** [Markdown summaries and concise text responses with local file paths or shell commands when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes or reads local Markdown files for session slots and project summaries; default behavior overwrites the current saved summary unless the user asks to append.]

## Skill Version(s):

0.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
