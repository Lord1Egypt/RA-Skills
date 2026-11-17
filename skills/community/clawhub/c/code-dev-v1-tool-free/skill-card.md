## Description:

A structured coding workflow guide for personal developers that organizes requests, planning, implementation, verification, testing, delivery, preference memory, and checkpoint tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and individual project maintainers use this skill to structure coding tasks into request, planning, execution, verification, and delivery checkpoints. It can also guide preference memory and checkpoint records for iterative development.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security evidence reports inconsistent claims about command execution, network/API use, credentials, and local persistence.

Mitigation: Review the skill before installation and enable it only where file writes, shell commands, API credentials, and network access remain under explicit user control.

Risk: The artifact describes local preference and checkpoint persistence and examples that may guide shell commands or tests.

Mitigation: Confirm paths and commands before execution, and avoid storing secrets or sensitive project data in memory or checkpoint files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/code-dev-v1-tool-free)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with JSON examples and inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local preference and checkpoint files under $HOME/code and may guide command execution through the host agent.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
