## Description: <br>
Manage Coolify deployments, applications, databases, and services via the Coolify API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[visiongeist](https://clawhub.ai/user/visiongeist) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to manage Coolify-hosted applications, databases, services, deployments, servers, projects, teams, backups, environment variables, SSH keys, and GitHub App integrations through API-backed commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate high-impact Coolify infrastructure resources, including deployments, databases, services, servers, projects, teams, backups, environment variables, SSH keys, and GitHub App integrations. <br>
Mitigation: Use a least-privilege Coolify token and require explicit human confirmation before delete, stop, restart, deploy, backup, key, or environment-variable changes are executed. <br>
Risk: The evidence security summary warns that the artifact encourages unsafe handling of private keys and secrets. <br>
Mitigation: Avoid pasting secrets or private keys into commands; do not allow the agent to read private key files unless the user explicitly requests that exact operation. <br>


## Reference(s): <br>
- [Coolify skill page](https://clawhub.ai/visiongeist/coolify) <br>
- [Coolify website](https://coolify.io) <br>
- [Coolify documentation](https://coolify.io/docs/) <br>
- [Coolify GitHub repository](https://github.com/coollabsio/coolify) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and structured JSON command responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands operate against Coolify API resources and require COOLIFY_TOKEN.] <br>

## Skill Version(s): <br>
2.1.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
