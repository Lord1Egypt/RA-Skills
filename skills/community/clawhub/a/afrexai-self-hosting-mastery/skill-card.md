## Description:

Guides agents through planning, deploying, securing, monitoring, backing up, and maintaining self-hosted homelab services.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1kalin](https://clawhub.ai/user/1kalin)

### License/Terms of Use:


## Use Case:

Developers, engineers, and technically capable operators use this skill to plan homelab infrastructure, generate Docker and reverse proxy configurations, design backup and monitoring practices, and audit self-hosted service operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated infrastructure commands can change host packages, firewall rules, containers, backups, or service exposure.

Mitigation: Review commands manually before execution, preview package upgrades, and test changes in a non-critical environment when possible.

Risk: Installer and update patterns such as curl-to-shell scripts, automatic container updates, and Docker socket access can expand operational risk.

Mitigation: Avoid curl-to-shell installers where possible, prefer HTTPS and signed repositories, pin container image versions, and restrict Docker socket access.

Risk: Incorrect self-hosting guidance can expose services or weaken backup and recovery posture.

Mitigation: Validate generated network, authentication, backup, and monitoring plans against the target environment before deployment.

## Reference(s):

- [Self-Hosting Mastery on ClawHub](https://clawhub.ai/1kalin/skills/afrexai-self-hosting-mastery)
- [Immich Docker Compose Release Asset](https://github.com/immich-app/immich/releases/latest/download/docker-compose.yml)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline YAML, bash, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose high-impact infrastructure commands and configuration changes that require manual review before execution.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
