## Description:

Sets up native macOS notifications for Claude Code in local and devpod/remote environments using terminal-notifier, notification hooks, and SSH reverse tunnels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ajitsingh25](https://clawhub.ai/user/ajitsingh25)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure Claude Code notifications on macOS, including local alerts and devpod notifications routed through SSH reverse tunnels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow persistently changes Claude hook settings, SSH config, remote devpod files, and macOS startup settings.

Mitigation: Review the setup script before running it and verify the affected Claude, SSH, devpod, and LaunchAgent configuration after installation.

Risk: Devpod setup depends on user-supplied SSH hostnames.

Mitigation: Use only trusted devpod hostnames and confirm the resolved SSH target before allowing the skill to configure remote files or SSH forwarding.

Risk: The local listener and fixed notification port may need stronger listener authentication and port-conflict handling.

Mitigation: Assess listener authentication and port 19876 availability before deployment, and harden those controls where required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ajitsingh25/skills/claude-notifications)
- [Publisher profile](https://clawhub.ai/user/ajitsingh25)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command examples and setup instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide macOS and SSH setup actions that write local and remote configuration files.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
