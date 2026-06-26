## Description: <br>
Configure Caddy as a reverse proxy with automatic HTTPS and simple Caddyfile syntax. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill for Caddy reverse proxy configuration guidance, including automatic HTTPS, Caddyfile syntax, Docker networking, reload validation, certificate storage, debugging, security headers, and performance notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Incorrect Caddyfile guidance could affect live HTTPS availability or reverse proxy routing. <br>
Mitigation: Review generated configuration and run caddy validate before applying changes. <br>
Risk: Reloads, port binding, DNS changes, or certificate storage changes can disrupt HTTPS service. <br>
Mitigation: Plan operational changes, verify DNS and ports 80 and 443, preserve certificate storage, and prefer caddy reload after validation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/caddy) <br>
- [Publisher profile](https://clawhub.ai/user/ivangdavila) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline Caddyfile and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the caddy binary when applying or validating generated configuration guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
