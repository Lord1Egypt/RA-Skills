## Description:

Batch file renaming utility with pattern matching, regex, sequence numbering, and dry-run preview.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and operations users use this skill to plan batch file renaming workflows for photos, downloads, exports, and other local file sets. It helps generate safe shell-based rename previews, sequence numbering, pattern replacement, normalization, and recursive rename guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Batch rename commands can create destination name collisions or overwrite valuable files.

Mitigation: Run a dry-run first, back up important directories, and add explicit destination-collision checks or no-clobber behavior before applying commands.

Risk: Shell commands may affect important or shared folders if applied without review.

Mitigation: Review generated commands before execution and apply them only after confirming the target directory and rename mapping.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown guidance with bash code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes dry-run preview guidance before applying rename commands]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
