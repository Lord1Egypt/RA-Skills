## Description:

Reads and displays the contents of a user-specified local text, configuration, or code file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jwu26](https://clawhub.ai/user/jwu26)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers and other agent users use this skill when they need an agent to inspect a known local file path and return its contents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill displays whatever local file path is passed to it, which can expose secrets or sensitive configuration if used on those files.

Mitigation: Use it only on files the user intends to inspect, and avoid passing secret or sensitive paths unless disclosure is intentional.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Shell commands]

**Output Format:** [Plain text file contents]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads the file path supplied by the user.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
