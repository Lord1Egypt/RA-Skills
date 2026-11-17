## Description:

Persists Feishu group-chat context by saving and reloading structured conversation summaries for OpenClaw sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zzlqxbms](https://clawhub.ai/user/zzlqxbms)

### License/Terms of Use:

MIT-0

## Use Case:

External ClawHub users and OpenClaw operators use this skill to preserve continuity in Feishu group chats across session resets by saving, loading, and maintaining per-group conversation summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Ordinary chat messages prefixed with [SYSTEM] may trigger broad agent actions if the suggested handling rule is installed as written.

Mitigation: Do not install the [SYSTEM] handling rule as written; restrict internal commands to trusted sources and require explicit user confirmation for save/load operations.

Risk: Automatic save/load and diary copying can retain and later resurface group-chat summaries without all participants expecting persistent memory.

Mitigation: Use per-group opt-in, tell group participants that summaries may be retained, and keep memory files isolated by group.

## Reference(s):

- [Known Feishu Group IDs](references/group-ids.md)
- [ClawHub skill page](https://clawhub.ai/zzlqxbms/skills/feishu-group-memory-system)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with inline shell commands and memory-file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces per-group memory summaries keyed by Feishu chat_id.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
