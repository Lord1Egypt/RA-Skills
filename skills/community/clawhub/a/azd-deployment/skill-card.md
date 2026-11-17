## Description:

Helps agents produce Azure Developer CLI, Bicep, shell-command, and troubleshooting guidance for deploying containerized applications to Azure Container Apps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thegovind](https://clawhub.ai/user/thegovind)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to set up azd projects, author azure.yaml and Bicep infrastructure, configure Azure Container Apps deployments, and troubleshoot azd up failures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated deployment guidance can change live Azure subscriptions, resource groups, role assignments, and Container Apps environments.

Mitigation: Review generated azure.yaml, Bicep, and shell commands before execution, and confirm the intended subscription, resource group, and azd environment.

Risk: Some Bicep examples include ACR admin credentials and listCredentials-based secrets for registry access.

Mitigation: Prefer managed identity with AcrPull for Container Apps and avoid ACR admin credentials or registry passwords in generated infrastructure.

Risk: Hook examples may use fixed /tmp files or suppress role-assignment errors.

Mitigation: Use private temporary paths for hook state and keep error suppression limited to known idempotent role-assignment cases.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thegovind/skills/azd-deployment)
- [Acceptance criteria](references/acceptance-criteria.md)
- [azure.yaml schema reference](references/azure-yaml-schema.md)
- [Bicep patterns for Azure Container Apps](references/bicep-patterns.md)
- [Azure Developer CLI troubleshooting guide](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with YAML, Bicep, JSON, shell, and troubleshooting snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include cloud-changing deployment commands and infrastructure-as-code examples for user review before execution.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
