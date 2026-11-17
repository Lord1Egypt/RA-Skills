## Description:

A Chinese-language desktop and folder organization skill that helps agents scan local files, propose safe classifications, and move files into type- or pattern-based folders after user confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[realorange1994](https://clawhub.ai/user/realorange1994)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to have an agent organize desktop or folder contents by scanning files, proposing categories, and producing local move operations only after review. It is intended for file organization workflows that need no deletion, no overwriting, logging, and rollback guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent to move local files, which may disrupt workflows if the source directory, destination directory, or classification plan is wrong.

Mitigation: Require a scan-and-review phase before move commands run, and approve only plans with clear source paths, destination folders, skipped-file handling, and rollback log locations.

Risk: Name collisions or sensitive-file moves could cause confusion or data handling issues.

Mitigation: Use collision-safe moves or auto-renaming, skip system and occupied files, and avoid running on irreplaceable or sensitive folders without a backup.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/realorange1994/skills/dandan-file-organizer)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands, tables, and file organization summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include scan summaries, proposed destination folders, operation logs, skipped-file reasons, and rollback command guidance.]

## Skill Version(s):

1.0.1 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
