## Description:

Perform chown-tool operations from the command line.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when they need an agent to provide command-line guidance for changing file ownership on local systems.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The utility can change ownership of arbitrary local paths and does not provide built-in path safeguards.

Mitigation: Use it only on trusted, intended paths and avoid sudo, privileged automation, or attacker-controlled path input unless additional validation is added.

Risk: Ownership-change failures are printed to stderr, but the script does not explicitly return a nonzero exit status.

Mitigation: Check stderr and command output after use, or wrap execution so automation fails closed when ownership changes are unsuccessful.

## Reference(s):


## Skill Output:

**Output Type(s):** [Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
