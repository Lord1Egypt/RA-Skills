## Description: <br>
Azure Cloud Architect helps agents use the local Azure CLI to inspect Azure resources, audit RBAC and security posture, analyze costs, and manage multiple subscriptions while requiring confirmation for write or destructive operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, cloud operators, and security teams use this skill to run Azure CLI-based inventory, health checks, RBAC reviews, security audits, cost analysis, and multi-subscription reporting. It is intended for Azure environments where the agent can use a local Azure CLI session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to run Azure CLI commands with broad local and cloud authority. <br>
Mitigation: Use least-privilege Azure accounts, verify the tenant and subscription before each operation, and require explicit confirmation before any write or destructive command. <br>
Risk: Generic API, callback, and file-write instructions are poorly scoped relative to the Azure CLI use case. <br>
Mitigation: Treat API callbacks and file writes as out of scope unless the publisher documents a precise need and the user explicitly approves the destination and data. <br>
Risk: Azure CLI output can expose subscription details, credentials, tokens, secrets, or other sensitive operational data. <br>
Mitigation: Redact sensitive values before sharing results in chat or logs, protect Azure CLI session credentials, and rotate any secret that may have been exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/azure-cloud-architect) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Azure CLI command examples, tables, checklists, and operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include read-only Azure CLI queries, dry-run or what-if plans, risk findings, and verification steps.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
