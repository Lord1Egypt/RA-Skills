## Description: <br>
Azure Infra Free helps agents run read-only Azure CLI queries for basic Azure resource inventory and health checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to inspect Azure subscriptions with read-only Azure CLI list, show, and get queries. It is intended for basic inventory and health checks, not write changes, security audits, cost analysis, or broad operations automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary flags broader and conflicting capability claims. <br>
Mitigation: Review before installation and use only for read-only Azure resource lookup unless the publisher narrows and clarifies the documented scope. <br>
Risk: The skill can guide command execution against a logged-in Azure account. <br>
Mitigation: Limit execution to read-only Azure CLI commands such as list, show, and get; block write, delete, modify, start, and stop requests. <br>
Risk: Azure query outputs may expose sensitive operational details. <br>
Mitigation: Do not request, print, store, or log secrets, tokens, passwords, access keys, or client secrets; redact sensitive values from shared outputs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/azure-infra-free) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline Azure CLI commands and table-style query results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only Azure CLI usage; requires local Azure CLI installation, Azure login, network access to Azure, and an appropriate subscription context.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
