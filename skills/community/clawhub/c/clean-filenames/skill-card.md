## Description:

Clean Filenames sanitizes local filenames by replacing invalid characters, normalizing whitespace, and trimming problematic leading or trailing spaces and dots.

This skill is ready for commercial/non-commercial use.

## Publisher:

[albionaiinc-del](https://clawhub.ai/user/albionaiinc-del)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, content managers, and other users use this skill to clean filenames for cross-platform compatibility in a single file, one directory, or a recursive directory tree.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill renames existing local files, and recursive mode can affect many filenames at once.

Mitigation: Run it first on a small test folder, use recursive mode only when intended, and keep backups for directories where renamed files could break links, scripts, media libraries, or workflows.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/albionaiinc-del/skills/clean-filenames)

## Skill Output:

**Output Type(s):** [Shell commands, Text, Files]

**Output Format:** [Plain text CLI status messages and file rename side effects]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Skips rename conflicts to avoid overwriting existing files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
