## Description:

Hash passwords using bcrypt or verify a password against a bcrypt hash.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ohernandez-dev-blossom](https://clawhub.ai/user/ohernandez-dev-blossom)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to generate bcrypt hashes for password storage workflows or check whether a supplied password matches an existing bcrypt hash.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Inline shell commands can expose passwords through shell history, process listings, logs, or command interpolation.

Mitigation: Read passwords from standard input or another non-command-line channel, avoid shell interpolation, and do not place secrets in temporary files or command arguments.

Risk: Unvalidated rounds or hash inputs can cause slow execution, malformed verification attempts, or unsafe command construction.

Mitigation: Parse rounds as an integer, validate bcrypt hash format before verification, and review commands before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ohernandez-dev-blossom/skills/bcrypt-generate)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and plaintext bcrypt hash or match result]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and the Python bcrypt package.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
