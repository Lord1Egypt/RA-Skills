## Description:

Batch rename files with customizable patterns, including prefixes, suffixes, sequential numbering, and dry-run previews.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freedompixels](https://clawhub.ai/user/freedompixels)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators can use this skill to generate shell-command guidance for previewing and applying local batch file renames with predictable numbering and preserved file extensions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Pattern handling can move or rename files outside the intended scope.

Mitigation: Use dry-run first, run only on disposable or backed-up directories, and avoid prefixes or suffixes containing slashes, backslashes, absolute paths, or '..' until names are validated and output is confined to the selected directory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/freedompixels/skills/cn-batch-file-renamer)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include dry-run-first guidance and warnings for local file renaming.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
