## Description: <br>
Complete self-hosting and homelab operating system for deploying, securing, monitoring, and maintaining home servers, Docker infrastructure, reverse proxies, backups, and self-hosted alternatives to SaaS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1kalin](https://clawhub.ai/user/1kalin) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, homelab operators, and infrastructure teams use this skill to plan, deploy, secure, monitor, troubleshoot, and maintain self-hosted services and Docker-based homelab infrastructure. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Administrative examples can install software, edit system configuration, change firewall exposure, prune Docker data, mount the Docker socket, delete backups, update packages, or reboot a server. <br>
Mitigation: Require explicit approval before running privileged commands, confirm the target host, inspect remote installer scripts, and back up configuration and data before changes. <br>
Risk: Self-hosted services can expose sensitive data or public network endpoints if configuration is copied without review. <br>
Mitigation: Review generated compose files, secrets, reverse proxy labels, firewall rules, and authentication settings before deployment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/1kalin/afrexai-self-hosting-mastery) <br>
- [Immich Docker Compose Release](https://github.com/immich-app/immich/releases/latest/download/docker-compose.yml) <br>
- [Docker Install Script](https://get.docker.com) <br>
- [Proxmox VE Package Repository](http://download.proxmox.com/debian/pve) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with YAML, Docker Compose, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include host-specific administrative commands and configuration snippets that require review before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
