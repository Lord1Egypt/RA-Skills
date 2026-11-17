## Description:

Organizes Desktop files into type-based folders for images, documents, and archives, with a preview mode intended to show planned moves before changes are applied.

This skill is ready for commercial/non-commercial use.

## Publisher:

[578499893](https://clawhub.ai/user/578499893)

### License/Terms of Use:

MIT-0

## Use Case:

Users and agents use this skill to clean a cluttered Desktop by previewing and optionally moving common file types into Images, Documents, and Archives folders. It is suited for simple personal file organization where the user can review the planned source and destination paths before applying changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can move Desktop files and create destination folders.

Mitigation: Require a dry-run preview listing exact source and destination paths before any move, block overwrites, and ask for explicit confirmation before applying changes.

Risk: Bulk organization may place files in folders the user did not intend.

Mitigation: Limit actions to the documented file extensions, skip hidden files and shortcuts, and provide a clear post-action report for review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/578499893/skills/clean-desktop)
- [Source skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown report with planned or completed file moves and inline shell commands when execution is needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preview mode is the default; applying moves should require explicit user confirmation.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
