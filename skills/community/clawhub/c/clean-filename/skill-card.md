## Description:

Removes invalid or unsafe characters from filenames and normalizes them for safe cross-platform use in files and directories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[albionaiinc-del](https://clawhub.ai/user/albionaiinc-del)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to clean unsafe filenames for individual files, directories, or recursive directory trees before sharing or moving them across platforms. It is useful for previewing and applying filename normalization to messy exports, downloads, or collaborative project folders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Directory or recursive use can rename many files in place, which may break links or references that depend on old filenames.

Mitigation: Run with --dry-run first and review the proposed changes before applying renames.

## Reference(s):

- [Clean Filename ClawHub page](https://clawhub.ai/albionaiinc-del/skills/clean-filename)

## Skill Output:

**Output Type(s):** [shell commands, guidance, text]

**Output Format:** [Markdown with inline bash code blocks and concise instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes dry-run guidance for previewing file renames before applying changes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
