## Description:

Deploy a project from a git repository onto AgentsPodium: frontend and backend on one pod, behind one domain, with a persistent disk.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samorodkin](https://clawhub.ai/user/samorodkin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to deploy or rebuild frontend, backend, or full-stack web projects on AgentsPodium from HTTPS git repositories, including private repositories when scoped credentials are supplied.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private repository tokens are stored for rebuilds and exposed inside the running pod environment.

Mitigation: Use a short-lived, read-only token scoped to one repository; rotate it after deployment when possible; deploy only trusted code and dependencies while the token is available.

Risk: Deployment configuration is sent to AgentsPodium and may include sensitive repository or environment settings.

Mitigation: Review configuration before submission and limit secrets to the minimum values required for the deployed app.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/samorodkin/skills/deploy-app)
- [AgentsPodium API](https://agentspodium.com/api)
- [AgentsPodium account API keys](https://agentspodium.com/account)
- [AgentsPodium webhook documentation](https://hosting.defispace.com/docs/webhooks.md)
- [AgentsPodium quickstart documentation](https://hosting.defispace.com/docs/quickstart.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes deployment API payloads, rebuild commands, troubleshooting notes, and credential-handling guidance.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
