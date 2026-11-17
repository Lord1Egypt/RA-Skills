## Description:

Convert chat conversations into structured Markdown knowledge-base files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[extraterrest](https://clawhub.ai/user/extraterrest)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn selected chat conversations into reusable Markdown knowledge-base notes after previewing the generated content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected conversation content may include sensitive or private details that would be saved into local Markdown files.

Mitigation: Review the generated preview and destination path before saving, use dry-run or cancel for sensitive chats, and avoid exporting secrets unless the storage location is appropriate.

Risk: The skill can create or update files in a configured knowledge-base folder.

Mitigation: Resolve the save path through configuration or user confirmation, preserve backups when configured, and require confirmation before writing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/extraterrest/skills/chat2kb)
- [Publisher profile](https://clawhub.ai/user/extraterrest)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with YAML frontmatter and concise status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local Markdown files after user preview and confirmation; supports dry-run behavior through configuration or environment variables.]

## Skill Version(s):

0.0.4 (source: server release metadata and clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
