## Description:

auto_dream helps agents append memory logs and periodically consolidate them into categorized long-term memory files and an index.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cyunxh](https://clawhub.ai/user/cyunxh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users can use this skill to manage durable memory by appending daily log entries, reviewing memory freshness, rebuilding a MEMORY.md index, and preparing Dream-mode consolidation prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dream mode can scan recent conversations and aggregate sensitive session details into a prompt file or durable memories.

Mitigation: Review the memory directory and generated prompt before consolidation, and avoid placing private or sensitive data in logs and sessions.

Risk: The skill can delete or rewrite prior memory files during consolidation workflows.

Mitigation: Keep backups or version control for the memory directory and manually review proposed memory changes before relying on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cyunxh/skills/dreamclaw)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with CLI commands and generated memory files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes append-only logs, categorized Markdown memory files, MEMORY.md indexes, and Dream-mode prompt text under the user's OpenClaw workspace.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
