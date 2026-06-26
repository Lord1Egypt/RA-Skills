## Description: <br>
Guide for setting up Claude Code in Docker containers with ttyd web terminal, tmux session persistence, acpx multi-agent tooling, and API configuration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tonakic](https://clawhub.ai/user/tonakic) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to configure Claude Code inside Docker or OpenClaw-style environments with browser terminal access, tmux persistence, optional multi-agent workflows, and provider-specific API settings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Writable ttyd sessions can expose an interactive shell if the web terminal is reachable by untrusted users. <br>
Mitigation: Run the setup only in an isolated trusted container and protect any non-local ttyd endpoint with authentication, TLS, and firewall or VPN restrictions. <br>
Risk: Broad Claude Code permissions and sensitive host mounts can expand the impact of a compromised or mistaken agent session. <br>
Mitigation: Limit Claude permissions to the project directory, avoid mounting sensitive host paths, and review permissions before using the skill. <br>
Risk: Persisted API keys and configuration files can be exposed through mounted directories or version control. <br>
Mitigation: Use Docker secrets or tightly permissioned env files, keep local credential files out of version control, and protect persisted configuration directories. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tonakic/docker-claude-code-setup) <br>
- [Claude Code installation guide](references/claude-code-installation.md) <br>
- [ttyd and tmux setup guide](references/ttyd-tmux-setup.md) <br>
- [acpx setup guide](references/acpx-setup.md) <br>
- [API configuration guide](references/api-configuration.md) <br>
- [ttyd source repository](https://github.com/tsl0922/ttyd.git) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash, JSON, and env configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Bilingual English and Chinese setup guidance with helper shell scripts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
