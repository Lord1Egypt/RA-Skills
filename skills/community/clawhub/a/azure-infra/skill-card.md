## Description: <br>
Azure Infra provides chat-based Azure infrastructure assistance using Azure CLI and portal context for querying, auditing, monitoring resources, and proposing safe changes with explicit confirmation before write or destructive actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bmdhodl](https://clawhub.ai/user/bmdhodl) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and cloud operators use this skill to inspect Azure subscriptions, audit resources, review health, security, costs, and prepare Azure CLI commands for changes that require explicit confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The assistant can inspect Azure resources visible to the current Azure CLI login. <br>
Mitigation: Use a least-privilege Azure account and confirm the tenant and subscription before running queries. <br>
Risk: Start, stop, scale, IAM, billing, or delete commands can change production infrastructure. <br>
Mitigation: Review the exact proposed command, prefer dry-run or plan output when available, and approve write or destructive actions only after explicit confirmation. <br>


## Reference(s): <br>
- [Azure CLI Query Patterns](references/azure-cli-queries.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline Azure CLI commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only Azure CLI queries by default; write or destructive commands require explicit user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
