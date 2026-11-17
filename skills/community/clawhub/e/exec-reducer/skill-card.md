## Description:

Provides reusable tools to batch process files for reading, writing, listing, and searching, reducing repeated exec command usage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jaxint](https://clawhub.ai/user/jaxint)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to wrap simple local file operations in reusable commands when reading, writing, listing, or searching files during automation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read and overwrite arbitrary accessible files without clear scope limits or overwrite safeguards.

Mitigation: Review target paths and content before running commands, and avoid sensitive directories, credentials, configuration files, or important files unless the write is intentional.

## Reference(s):


## Skill Output:

**Output Type(s):** [Shell commands, Code, Text]

**Output Format:** [Markdown guidance with Python command examples and plain text command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands operate on local filesystem paths available to the agent.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
