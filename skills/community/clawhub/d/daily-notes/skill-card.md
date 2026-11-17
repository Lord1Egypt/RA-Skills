## Description:

Daily Notes helps an agent capture everyday thoughts, ideas, memos, discoveries, and image attachments as local notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kazuya-ecnu](https://clawhub.ai/user/kazuya-ecnu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and personal productivity agents use this skill to record, list, search, update, and delete daily notes with optional image associations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may automatically save casual messages as notes, including personal thoughts or sensitive context.

Mitigation: Use it only for intentional journaling, avoid entering private or regulated information, and prefer workflows that ask for confirmation before saving.

Risk: Notes and image references are retained as raw local files.

Mitigation: Review local retention expectations before installation and periodically inspect or remove stored notes and attachments.

Risk: Delete operations can remove notes and associated images.

Mitigation: Require explicit user confirmation before deleting records or image attachments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kazuya-ecnu/skills/daily-notes)

## Skill Output:

**Output Type(s):** [Text, JSON, Files]

**Output Format:** [Markdown responses and local JSON note records with image path references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores notes locally under ~/.openclaw/workspace/notes-data/ with optional image attachments.]

## Skill Version(s):

1.2.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
