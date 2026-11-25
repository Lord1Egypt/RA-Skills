## Description:

Connects an agent to a user's Google Drive and Sheets through OAuth for creating, reading, editing, formatting, and deleting files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thinhbuiii](https://clawhub.ai/user/thinhbuiii)

### License/Terms of Use:

MIT-0

## Use Case:

People using an OpenClaw agent use this skill to connect their own Google account and manage Drive and Sheets files, including creating folders, reading and writing spreadsheet data, and formatting sheets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment rates this release suspicious because a formatting command can bypass deletion safeguards and requested Drive access exceeds the stated connection-and-test purpose; the scan is partial.

Mitigation: Review the deletion safeguard, OAuth endpoint override, chat-based credential setup, and requested permissions before installation; the partial scan does not establish that all relevant details were covered.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/thinhbuiii/skills/gdrive-connect-pro)
- [User installation guide](artifact/CAI-DAT.md)

## Skill Output:

**Output Type(s):** [Files, API Calls, Guidance, Shell commands, Configuration instructions]

**Output Format:** [Google Drive and Sheets files, operation results, and setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the connected user's Google account; operations can create, modify, format, or delete Drive files.]

## Skill Version(s):

1.3.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
