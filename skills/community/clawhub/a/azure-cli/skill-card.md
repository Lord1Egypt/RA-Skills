## Description: <br>
Comprehensive Azure Cloud Platform management via command-line interface. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ddevaal](https://clawhub.ai/user/ddevaal) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, cloud engineers, and DevOps practitioners use this skill to operate Azure resources with Azure CLI commands, automation patterns, and helper scripts for status checks, deployment, storage analysis, subscription reporting, and cleanup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Azure CLI examples and helper scripts can create, update, deploy, or delete live cloud infrastructure. <br>
Mitigation: Confirm the active subscription and resource group, use non-production resources for examples, and review every create, update, delete, deploy, or run-command action before execution. <br>
Risk: Azure credentials, access tokens, connection strings, or service-principal secrets could be exposed if pasted into chat or logs. <br>
Mitigation: Use least-privilege Azure identities and avoid sharing secrets in agent conversations, command output, or logs. <br>


## Reference(s): <br>
- [Azure CLI Complete Command Reference](references/REFERENCE.md) <br>
- [Azure CLI official documentation](https://learn.microsoft.com/en-us/cli/azure/) <br>
- [Azure CLI command reference](https://learn.microsoft.com/en-us/cli/azure/reference-index) <br>
- [Azure Storage pricing](https://azure.microsoft.com/en-us/pricing/details/storage/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline bash and PowerShell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Azure CLI examples and helper shell script usage that should be reviewed before execution against live Azure subscriptions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
