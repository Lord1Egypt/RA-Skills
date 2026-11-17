## Description:

Change file permissions using symbolic or numeric modes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to guide local file permission changes with chmod-style symbolic or numeric modes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Permission changes can unintentionally remove access, executability, or privacy controls when applied to the wrong path or mode.

Mitigation: Review target paths and modes before execution; test on a single noncritical file before broad or recursive changes.

Risk: The artifact helper script accepts an octal mode for one file, while the skill text also describes symbolic and recursive usage.

Mitigation: Confirm generated commands against the available tool behavior and use the system chmod command when symbolic or recursive changes are required.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should be reviewed before execution because permission changes affect local files.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
