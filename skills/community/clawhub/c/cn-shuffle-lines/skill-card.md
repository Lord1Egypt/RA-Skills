## Description:

Randomly shuffles the order of lines in provided text or a local UTF-8 file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freedompixels](https://clawhub.ai/user/freedompixels)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to randomize the order of text lines supplied inline or read from a local file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using file input can print shuffled contents from the provided path, which may expose sensitive data if terminal output is logged.

Mitigation: Avoid passing sensitive files and review terminal logging practices before using file input.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/freedompixels/skills/cn-shuffle-lines)

## Skill Output:

**Output Type(s):** [text, shell commands]

**Output Format:** [Plain text CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Line order is randomized; file input reads from a user-provided path and prints shuffled content to standard output.]

## Skill Version(s):

1.0.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
