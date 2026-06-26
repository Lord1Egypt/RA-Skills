## Description: <br>
Facilitates installation and management of VPS tools such as Traefik, Portainer, Chatwoot, N8N, and other open-source applications on Linux VPSs using the Setup Automatik engine. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alltomatos](https://clawhub.ai/user/alltomatos) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and VPS administrators use this skill to install, configure, and verify open-source infrastructure, automation, AI, communication, and business application stacks on Linux VPS hosts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks an agent to administer a VPS with powerful server access. <br>
Mitigation: Use a fresh or snapshotted server and temporary SSH keys rather than passwords or long-lived private keys. <br>
Risk: The bundled installer under-discloses telemetry and credential-handling behavior. <br>
Mitigation: Review or restrict the installer before execution, block or remove Orion telemetry if unacceptable, and rotate SSH, Portainer, SMTP, and application credentials after use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alltomatos/aetup-automatik) <br>
- [tools.md](references/tools.md) <br>
- [SetupOrion.sh](assets/SetupOrion.sh) <br>
- [Mundo Automatik](https://mundoautomatik.com/) <br>
- [Orion Design setup](https://oriondesign.art.br/setup) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and configuration values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require VPS access, domain names, service credentials, SMTP details, and post-installation verification steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
