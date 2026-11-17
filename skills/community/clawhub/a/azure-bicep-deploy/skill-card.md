## Description:

Deploy and validate Azure Bicep and ARM templates to manage resources and multi-environment setups, including Azure Container Apps configurations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[junior-juarez-msft](https://clawhub.ai/user/junior-juarez-msft)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to plan, validate, and run Azure Bicep or ARM deployments across dev, staging, and production environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PowerShell helper examples use command-string execution patterns that can run unintended commands if arguments are not trusted.

Mitigation: Review helper scripts before use and pass arguments directly to Azure CLI commands instead of evaluating assembled command strings.

Risk: Deployment examples can create or change live Azure resources.

Mitigation: Run what-if first, confirm the active tenant and subscription, and use a least-privileged identity in a non-production subscription until reviewed.

Risk: Container Apps examples include public ingress and placeholder registry credentials.

Mitigation: Treat external ingress as internet exposure and avoid hardcoding real registry passwords in templates or parameter files.

## Reference(s):

- [Deploy Script](references/deploy.md)
- [Validate Script](references/validate.md)
- [Bicep Build Script](references/bicep-build.md)
- [Azure Container Apps Reference](references/container-apps.md)
- [Install Azure CLI](https://docs.microsoft.com/cli/azure/install-azure-cli)
- [Azure deployment parameters schema](https://schema.management.azure.com/schemas/2019-04-01/deploymentParameters.json#)
- [ClawHub skill page](https://clawhub.ai/junior-juarez-msft/skills/azure-bicep-deploy)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline Azure CLI, PowerShell, Bicep, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include copy-paste deployment, validation, and build commands that should be reviewed before execution.]

## Skill Version(s):

2.1.0 (source: server evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
