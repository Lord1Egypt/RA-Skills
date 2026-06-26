## Description: <br>
Deploy containerized applications to Azure Container Apps using Azure Developer CLI (azd). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thegovind](https://clawhub.ai/user/thegovind) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to configure azd projects, Azure Container Apps services, Bicep infrastructure, remote ACR builds, environment variables, deployment hooks, and troubleshooting workflows for containerized applications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes Azure deployment templates and commands that can create, modify, delete, or bill cloud resources. <br>
Mitigation: Review the active Azure tenant, subscription, resource group, costs, and azd hooks before running azd commands. <br>
Risk: The security summary flags a risky ACR admin-password/listCredentials pattern. <br>
Mitigation: Prefer managed identity with least-privilege AcrPull and review any credential-based registry access before use. <br>
Risk: Environment reset commands can remove local azd environment state. <br>
Mitigation: Back up or verify the target environment before using reset or delete commands. <br>


## Reference(s): <br>
- [Azd Deployment for Azure on ClawHub](https://clawhub.ai/thegovind/azd-deployment) <br>
- [Azure Developer CLI Deployment Acceptance Criteria](references/acceptance-criteria.md) <br>
- [azure.yaml Complete Schema Reference](references/azure-yaml-schema.md) <br>
- [Bicep Patterns for Azure Container Apps](references/bicep-patterns.md) <br>
- [Azure Developer CLI Troubleshooting](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with YAML, JSON, Bicep, shell, Dockerfile, and nginx code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance may include Azure CLI and azd commands that change cloud resources and costs.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
