## Description:

Organizes files into folders based on their extensions to help clean up a directory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[albionaiinc-del](https://clawhub.ai/user/albionaiinc-del)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and general users can use this skill to organize a selected local directory by moving files into extension-named folders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The tool rearranges files in the directory where it is run and may disrupt existing organization.

Mitigation: Test it on a non-critical folder first and keep backups for files that cannot be lost.

Risk: Running it in directories with important existing extension folders may create confusing or unwanted file moves.

Mitigation: Avoid running it in important directories until the expected folder layout has been reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/albionaiinc-del/skills/file-organizer-by-ext)

## Skill Output:

**Output Type(s):** [text, shell commands, code]

**Output Format:** [Markdown guidance with shell command examples and local Python behavior]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local command-line guidance; the bundled tool moves files in place.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
