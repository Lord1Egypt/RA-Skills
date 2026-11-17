## Description:

Compare two files and display their differences in a human-readable markdown format.

This skill is ready for commercial/non-commercial use.

## Publisher:

[super9du](https://clawhub.ai/user/super9du)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other agent users use this skill to compare two provided file paths and receive a concise Markdown summary of additions, deletions, modifications, and unchanged context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Diffing sensitive files can expose secrets, credentials, private keys, or private content in the agent response.

Mitigation: Only compare file paths the user explicitly provides, and avoid diffing sensitive files unless the user intends their contents to appear in output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/super9du/skills/file-diff)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with diff-style code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes the compared file paths and reports when no differences are found.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
