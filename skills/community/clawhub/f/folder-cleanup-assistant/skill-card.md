## Description:

Folder Cleanup Assistant helps users safely organize local folders by analyzing contents, requiring a compressed backup, and moving selected files instead of deleting them.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tianheihei002](https://clawhub.ai/user/tianheihei002)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill in a desktop agent to inspect a chosen local folder, choose cleanup options, back up contents, move selected files, and receive a recovery-oriented cleanup report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unintended file movement or loss of access during cleanup.

Mitigation: Review the proposed file list, create a compressed backup first, move files instead of deleting them, and keep the backup until recovery is no longer needed.

Risk: Running cleanup against the wrong folder.

Mitigation: Confirm the target directory before scanning or moving files, and limit the skill to a specific user-selected folder.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tianheihei002/skills/folder-cleanup-assistant)
- [Publisher profile](https://clawhub.ai/user/tianheihei002)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with shell command examples and cleanup reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-selected target folder, desktop filesystem access, backup confirmation, and review of proposed file moves before execution.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
