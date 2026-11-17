## Description:

Azure智能体框架工具-专业版 helps agents guide enterprise Azure AI Foundry orchestration, including batch agent management, tool integration, monitoring and alerting, multi-tenant isolation, and CI/CD deployment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to plan and execute Azure AI Foundry agent workflows, from creating multiple agents to configuring monitoring, tenant workspaces, and deployment pipelines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloud resource changes or deployment commands may affect Azure AI Foundry environments.

Mitigation: Review commands before execution, test in staging first, and use least-privilege Azure credentials.

Risk: Webhook URLs, credentials, or environment-specific settings could be exposed through committed configuration files.

Mitigation: Keep real webhook URLs and credentials out of committed files and use environment-specific secret management.

Risk: Monitoring, tenant isolation, or CI/CD guidance may be misconfigured for a production workspace.

Mitigation: Review workspace boundaries, alert settings, and health checks before production deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/azure-agent-framework-tool-pro)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code, shell command, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Azure setup steps, deployment commands, YAML configuration, operational checks, and security guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
