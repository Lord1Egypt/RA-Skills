## Description:

Installs and configures headless Google Chrome for OpenClaw's browser tool on Linux hosts where root or sudo access is unavailable.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huangdawei](https://clawhub.ai/user/huangdawei)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to install no-root Chrome dependencies, configure OpenClaw for CDP attachment, and troubleshoot common browser automation failures in Linux containers, VPS hosts, or sandboxes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer downloads Chrome and package archives without independent integrity checks.

Mitigation: Review before installing, run only on machines where a user-level Chrome installer is acceptable, and prefer pinned package versions with hash or signature verification.

Risk: Custom chrome or library directory arguments can affect the persistent wrapper script that is generated.

Mitigation: Do not pass directory values from untrusted input, and inspect generated wrapper paths before reuse.

Risk: The documented OpenClaw setup uses no-sandbox browser execution for constrained Linux hosts.

Mitigation: Run the browser in an isolated container or user account with least privilege and limited access to sensitive local data.

## Reference(s):

- [Google Chrome stable Debian package](https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash, JSON, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes no-root Chrome installation steps, OpenClaw browser settings, and troubleshooting guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
