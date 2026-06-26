## Description: <br>
Set up native macOS notifications for Claude Code on local and devpod/remote environments, including terminal-notifier, SSH reverse tunnels, a launchd listener, tmux passthrough, and Claude Code notification hooks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ajitsingh25](https://clawhub.ai/user/ajitsingh25) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to configure Claude Code notifications on a local Mac and optionally route notifications from trusted devpod or remote SSH hosts back to macOS Notification Center. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup creates a persistent local notification listener and SSH reverse-forwarding configuration. <br>
Mitigation: Install only when this behavior is desired, use trusted devpod SSH hostnames, and review the listener and SSH configuration before enabling it. <br>
Risk: The setup changes local Claude Code settings and may also change remote ~/.claude and ~/.tmux.conf files. <br>
Mitigation: Review or back up ~/.claude/settings.json, ~/.ssh/config, and relevant remote configuration files before running setup. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ajitsingh25/claude-notifications) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires macOS for setup and may configure local Claude Code settings, launchd, SSH config, and remote devpod files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
