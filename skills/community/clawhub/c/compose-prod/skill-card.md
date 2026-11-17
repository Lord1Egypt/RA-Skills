## Description:

Generates production-grade Docker Compose configurations for Dockerized applications, including health checks, segmented networks, resource limits, log rotation, restart policies, secrets handling, and backup volumes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[llcsamih](https://clawhub.ai/user/llcsamih)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect Dockerized application projects and generate or improve production Docker Compose setups. It is intended for projects that need Compose services, network segmentation, resource controls, environment examples, health checks, and validation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated Compose output may include under-scoped secret handling or unsafe production defaults.

Mitigation: Review and harden the generated Compose file before use, prefer .env.example or source-derived variable names over reading live .env files, and require explicit secrets instead of default passwords.

Risk: Health-check commands can expose passwords or otherwise mishandle credentials.

Mitigation: Avoid passing passwords in health-check command arguments and confirm secret handling before deployment.

Risk: The skill may be used when Docker Compose is not the right deployment target.

Mitigation: Confirm the target is production Docker Compose rather than development Compose, Kubernetes, or a managed container platform before applying the generated configuration.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/llcsamih/skills/compose-prod)

## Skill Output:

**Output Type(s):** [Code, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with YAML, env, and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces docker-compose.yml content, .env.example content, validation commands, and operational notes for the generated Compose setup.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
