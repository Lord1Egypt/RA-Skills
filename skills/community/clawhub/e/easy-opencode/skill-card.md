## Description:

opencode can do all the things related to code

This skill is ready for commercial/non-commercial use.

## Publisher:

[deciding](https://clawhub.ai/user/deciding)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to route repository coding tasks through Opencode, review its plan, and delegate implementation after the plan is approved.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill delegates broad repository coding tasks to an external coding tool with wide repository authority.

Mitigation: Use it only on trusted repositories and review Opencode plans and changes before applying them.

Risk: The artifact shows shell command templates that may be unsafe when copied with raw paths or user text.

Mitigation: Prefer safe process invocation and carefully quote or validate paths and instructions before execution.

Risk: The security evidence recommends avoiding sensitive or production-impacting tasks without explicit review.

Mitigation: Require human approval for sensitive files, credentials, deployment changes, and production-impacting modifications.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/deciding/skills/easy-opencode)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and coding guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Delegates planning and build work to the opencode CLI when available.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
