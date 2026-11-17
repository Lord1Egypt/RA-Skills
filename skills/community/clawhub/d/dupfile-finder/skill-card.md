## Description:

Identify and list duplicate files in a specified directory to help manage and free up storage space efficiently.

This skill is ready for commercial/non-commercial use.

## Publisher:

[albionaiinc-del](https://clawhub.ai/user/albionaiinc-del)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and users run this skill to find duplicate files in a chosen local directory so they can review storage usage and decide what to clean up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local duplicate-file finder reads file contents under the directories selected for scanning.

Mitigation: Run it only on directories whose file contents you are comfortable allowing a local script to hash.

Risk: The tool prints duplicate file paths and hashes to the terminal.

Mitigation: Review terminal output before sharing logs or screenshots that may expose local path names.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/albionaiinc-del/skills/dupfile-finder)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and plain-text duplicate file listings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports duplicate file hashes and paths; it does not delete files or send data elsewhere according to the security evidence.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
