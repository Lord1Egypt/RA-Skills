## Description:

Human-in-the-loop security layer. Intercepts high-risk commands and requires push notification approval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lucky-2968](https://clawhub.ai/user/lucky-2968)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to route shell command execution through a human approval and audit workflow for high-risk commands in OpenClaw environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented shell safety layer may create false confidence because the package evidence does not include the tools it instructs users to rely on.

Mitigation: Do not rely on this as a shell safety layer unless the publisher supplies the missing implementation, tool registration, fail-closed behavior, and tests for blocked or approved commands.

Risk: Copying the documented TOOLS.md instructions could break shell use if the referenced tools are unavailable.

Mitigation: Review the installed package before deployment and verify that clawshell_bash, clawshell_status, and clawshell_logs are registered and executable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lucky-2968/skills/clawshell-0-1-0)
- [Pushover Application Setup](https://pushover.net/apps/build)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe tool calls, command results, approval state, and audit log entries.]

## Skill Version(s):

0.1.0 (source: frontmatter); release 1.0.0 (source: server evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
