## Description:

Chartmaker records, searches, summarizes, and exports chart-related text entries from a local command-line data store.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain1](https://clawhub.ai/user/bytesagain1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data practitioners can use this skill to log chart-related notes, track transformations, search previous entries, and export accumulated local records. It should be treated as a local activity log rather than a chart rendering tool.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is advertised as terminal chart visualization but primarily stores and searches user text locally, which may retain sensitive data unexpectedly.

Mitigation: Review before installing, use it only when a local activity log is intended, and avoid passing secrets, personal data, credentials, proprietary datasets, or other sensitive content.

Risk: Free-form command input is written to persistent files in the user's home directory.

Mitigation: Periodically inspect or delete ~/.local/share/chartmaker and limit logged content to non-sensitive chart or workflow notes.

## Reference(s):

- [Chartmaker ClawHub Skill](https://clawhub.ai/bytesagain1/skills/chartmaker)
- [BytesAgain](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, shell commands, files]

**Output Format:** [Terminal text with local log and export files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local activity logs and exports under ~/.local/share/chartmaker.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
