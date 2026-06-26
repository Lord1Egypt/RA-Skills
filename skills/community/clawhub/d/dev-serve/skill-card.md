## Description: <br>
Start and manage tmux-backed dev servers exposed through Caddy at wildcard subdomains. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BrennerSpear](https://clawhub.ai/user/BrennerSpear) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to start, list, restart, and stop local project dev servers in tmux while exposing them through Caddy on wildcard subdomains. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper can expose local dev servers on a wildcard domain with limited safeguards. <br>
Mitigation: Use it only with trusted repositories, keep repo names and DEV_SERVE_DOMAIN DNS-safe, firewall raw dev ports, and remove routes with dev-serve down when finished. <br>
Risk: The helper can modify the Caddyfile and reload Caddy through the local admin API. <br>
Mitigation: Back up the Caddyfile before use and review generated route changes before relying on the exposed service. <br>
Risk: The helper can patch Vite configuration and run project dev commands in tmux. <br>
Mitigation: Inspect the project's package.json dev script or DEV_CMD override before starting a server, especially for unfamiliar repositories. <br>


## Reference(s): <br>
- [Dev Serve on ClawHub](https://clawhub.ai/BrennerSpear/dev-serve) <br>
- [Caddy companion skill](https://clawhub.com/skills/caddy) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell command blocks and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide changes to tmux sessions, Vite allowedHosts, Caddyfile routes, Caddy reloads, and local state files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
