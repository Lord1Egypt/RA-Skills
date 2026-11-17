## Description:

Build high-value Obsidian daily and weekly review notes from conversation or existing markdown notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[amortalsodyssey](https://clawhub.ai/user/amortalsodyssey)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn chat sessions and Obsidian daily notes into durable daily entries, regenerated daily summaries, and weekly reports grouped by work item.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read and overwrite Obsidian daily and weekly notes.

Mitigation: Review generated note changes before relying on them, keep config.json private and trusted, and use explicit commands for append, daily refresh, or weekly generation.

Risk: Configuration may allow reads or writes outside the intended vault.

Mitigation: Set obsidian_bin to the real Obsidian CLI, avoid absolute or ../ paths in daily_dir and weekly_dir, and use trusted vault_path settings.

## Reference(s):

- [README](artifact/README.md)
- [ClawHub skill page](https://clawhub.ai/amortalsodyssey/skills/conversation-recap-to-obsidian)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and Obsidian note content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can append or regenerate local Obsidian daily and weekly markdown notes when configured with trusted paths.]

## Skill Version(s):

1.2.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
