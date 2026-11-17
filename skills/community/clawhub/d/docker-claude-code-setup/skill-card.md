## Description:

Guide for setting up Claude Code in Docker containers with ttyd web terminal access, tmux session persistence, acpx multi-agent workflows, and API configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tonakic](https://clawhub.ai/user/tonakic)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to set up a Docker-based Claude Code environment with browser terminal access, persistent tmux sessions, optional acpx agent routing, and provider API configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A writable ttyd web terminal can expose shell access if the port is reachable from public or shared networks.

Mitigation: Bind ttyd to localhost or protect it with strong authentication, HTTPS, and network controls before use outside a local environment.

Risk: Broad persistent Claude Code permissions can allow unintended file edits or command execution.

Mitigation: Avoid wildcard permission examples for routine use and grant only the project-specific permissions required for the task.

Risk: Persistent workspace files and configuration examples may contain API keys or other secrets.

Mitigation: Keep secrets out of tracked files, prefer environment-specific secret handling, and rotate keys if exposure is suspected.

Risk: Installer commands that fetch and execute remote setup scripts can change behavior over time.

Mitigation: Review and pin or verify installation sources before running them in a production or shared container.

## Reference(s):

- [Claude Code Installation](references/claude-code-installation.md)
- [ttyd and tmux Setup](references/ttyd-tmux-setup.md)
- [acpx Setup](references/acpx-setup.md)
- [API Configuration](references/api-configuration.md)
- [ttyd source repository](https://github.com/tsl0922/ttyd.git)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, Code]

**Output Format:** [Markdown with bash, JSON, and environment variable examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Bilingual English and Chinese setup guidance]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
