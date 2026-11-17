## Description:

Facilitate the installation and management of VPS solutions using the Setup Automatik engine (powered by Orion Design). Use when the user wants to install, configure, or manage tools like Traefik, Portainer, Chatwoot, N8N, and other open-source applications on a Linux VPS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alltomatos](https://clawhub.ai/user/alltomatos)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to prepare a Linux VPS and install or manage open-source infrastructure, automation, CRM, AI, and utility stacks through the Setup Automatik and SetupOrion workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for broad VPS access and can run an installer that changes server configuration.

Mitigation: Use short-lived, least-privilege access and run it only on a disposable or well-backed-up VPS after reviewing the planned commands.

Risk: SSH secrets and administrator credentials could be exposed or persist after setup.

Mitigation: Prefer OpenClaw pairing, do not paste SSH passwords or private keys into chat, and rotate Portainer or other administrator credentials created or stored during installation.

Risk: The installer may use telemetry, remote installers, container images, or scripts that require additional trust decisions.

Mitigation: Review the installer first, explicitly accept or disable telemetry, and verify remote installers and container images before deployment.

## Reference(s):

- [Setup Automatik on ClawHub](https://clawhub.ai/alltomatos/skills/aetup-automatik)
- [Orion Design VPS Solutions](references/tools.md)
- [SetupOrion.sh installer script](assets/SetupOrion.sh)
- [Mundo Automatik](https://mundoautomatik.com/)
- [Orion Design setup](https://oriondesign.art.br/setup)
- [OpenClaw node pairing installer](https://get.openclaw.ai)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and deployment steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include VPS access setup, domain and service configuration, credential handling guidance, and post-installation verification steps.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
