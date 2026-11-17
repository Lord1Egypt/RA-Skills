## Description:

FastGithub provides guidance and shell commands for running a local proxy that can accelerate GitHub clone, push, release download, and browsing workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yantianlong-01](https://clawhub.ai/user/yantianlong-01)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to install, start, stop, restart, and troubleshoot a local FastGithub proxy for slow GitHub access, Git operations, and release downloads.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run a FastGithub binary from an installation archive whose origin and integrity are not established in the provided evidence.

Mitigation: Use the skill only when the binary and certificate source are trusted and independently verified before installation.

Risk: The skill configures a local proxy and recommends CA certificate installation, which can affect HTTPS behavior beyond the immediate GitHub workflow.

Mitigation: Keep proxy and certificate changes scoped and reversible, and remove them after use when they are no longer needed.

Risk: The documentation suggests disabling Git TLS verification as a temporary workaround.

Mitigation: Avoid disabling TLS verification globally; if it is unavoidable for diagnosis, limit the scope and restore verification immediately afterward.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yantianlong-01/skills/fastgithub)

## Skill Output:

**Output Type(s):** [Markdown guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline bash code blocks and command tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes proxy environment variables, service-management commands, certificate guidance, and troubleshooting checks.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
