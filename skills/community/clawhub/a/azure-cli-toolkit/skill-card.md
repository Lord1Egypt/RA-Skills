## Description: <br>
Azure Cli Toolkit helps agents guide Azure CLI administration for service-principal authentication, batch resource operations, scripted deployments, multi-subscription management, cost analysis, and policy and security checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, DevOps engineers, and cloud operations teams use this skill to draft and review Azure CLI commands for resource administration, automation, multi-subscription inventory, cost review, and compliance checks. It is intended for agent-assisted operational guidance where commands are reviewed before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: High-impact Azure operations such as VM deletion or stopping can affect live resources when scope is unclear. <br>
Mitigation: Require the agent to show the exact subscription, resource group, resource IDs, and planned command before execution, and require explicit approval for delete or stop commands. <br>
Risk: Exported long-lived Azure credentials can be exposed through shell history, process environments, or logs. <br>
Mitigation: Prefer managed identity or Key Vault-backed secrets and avoid printing or storing credentials in generated commands or configuration. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/azure-cli-toolkit) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Azure CLI commands and configuration snippets that require operator review before execution.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter lists 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
