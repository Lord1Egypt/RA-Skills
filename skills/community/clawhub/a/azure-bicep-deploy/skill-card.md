## Description: <br>
Deploy and validate Azure Bicep and ARM templates to manage resources and multi-environment setups, including Azure Container Apps configurations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[junior-juarez-MSFT](https://clawhub.ai/user/junior-juarez-MSFT) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud engineers use this skill to plan, validate, and run Azure CLI and Bicep workflows for Bicep or ARM template deployments across dev, staging, and production environments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Suggested deployment commands can create or change live Azure resources and incur cost. <br>
Mitigation: Confirm the active Azure tenant, subscription, resource group, template, parameter file, and expected cost, then run validation or what-if before deployment. <br>
Risk: Example Container Apps guidance includes public ingress and placeholder registry secrets. <br>
Mitigation: Enable public ingress only when required and replace placeholders with managed secret handling rather than hardcoded credentials. <br>


## Reference(s): <br>
- [Azure Bicep Deploy on ClawHub](https://clawhub.ai/junior-juarez-MSFT/azure-bicep-deploy) <br>
- [Bicep Build Script](references/bicep-build.md) <br>
- [Azure Container Apps Reference](references/container-apps.md) <br>
- [Deploy Script](references/deploy.md) <br>
- [Validate Script](references/validate.md) <br>
- [Azure CLI Install Documentation](https://docs.microsoft.com/cli/azure/install-azure-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline Azure CLI, PowerShell, Bicep, and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Azure deployment commands and example parameter files that require review before execution.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
