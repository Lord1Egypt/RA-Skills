## Description:

Automatically extract key facts from conversation history and persist to local memory files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaobu2020](https://clawhub.ai/user/xiaobu2020)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to capture useful facts from recent conversations and keep local memory files current without manual note-taking. It is intended for local-first memory persistence in OpenClaw-style agent workspaces.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic memory capture may persist sensitive or unintended conversation content.

Mitigation: Install only when automatic local memory capture is desired, use dry-run before enabling scheduled extraction, and regularly inspect stored memory files.

Risk: Conversation-derived system rules may be written into agent instruction files and affect future agent behavior.

Mitigation: Review or disable automatic hooks and remove any route that writes extracted chat text to TOOLS.md or AGENTS.md unless explicitly needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiaobu2020/skills/conversation-saver)
- [README](artifact/README.md)
- [Chinese README](artifact/README-zh.md)
- [Configuration](artifact/config.json)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Text, Configuration]

**Output Format:** [Markdown memory entries, JSON-like ontology records, and terminal status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes are local file updates controlled by config.json; dry-run mode previews extracted facts without writing.]

## Skill Version(s):

0.1.1 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
