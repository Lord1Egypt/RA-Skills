## Description:

Docker容器专业版 helps operations teams manage Docker clusters, private registries, image scanning, container monitoring, alerts, scaling, and CI/CD workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, DevOps engineers, and enterprise operations teams use this skill to plan and operate Docker infrastructure, including Swarm clusters, Harbor registries, vulnerability scanning, monitoring, alerting, scaling, and pipeline deployments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives agents high-impact Docker, registry, and CI/CD authority with weak scoping.

Mitigation: Require explicit host, registry, and environment selection before deploy, join, push, scale, or CI/CD actions, and review proposed commands before execution.

Risk: Credential handling guidance is inconsistent for registry, webhook, and CI/CD tokens.

Mitigation: Keep secrets in environment variables or a secret manager, avoid storing credentials in local configuration files, and redact tokens from generated output.

Risk: Container and pipeline operations can affect production availability.

Mitigation: Run the skill with least-privilege Docker and registry access, separate development, staging, and production targets, and require human approval for production changes.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash and YAML code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include structured task responses with status, results, logs, Docker command examples, and configuration snippets.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
