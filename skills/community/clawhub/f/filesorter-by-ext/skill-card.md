## Description:

Automatically sorts files in a chosen directory into folders named by file extension.

This skill is ready for commercial/non-commercial use.

## Publisher:

[albionaiinc-del](https://clawhub.ai/user/albionaiinc-del)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and end users use this skill to organize local directories by grouping files into extension-named folders from the command line.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can move files unexpectedly while reorganizing a directory.

Mitigation: Run it first on a test folder and keep backups of important files.

Risk: The security summary reports a flaw that can move files outside the chosen folder.

Mitigation: Avoid shared or untrusted directories and check for existing extension-named symlinks such as pdf or jpg before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/albionaiinc-del/skills/filesorter-by-ext)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown usage guidance and command-line status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Moves files in place within the selected directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
