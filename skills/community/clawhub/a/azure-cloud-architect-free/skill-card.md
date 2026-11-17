## Description: <br>
This skill helps agents use Azure CLI for basic Azure subscription navigation, resource inventory queries, and virtual machine health checks in a read-only posture. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, cloud engineers, and operations staff use this skill to inspect accessible Azure subscriptions, switch the active subscription, list resources, and check virtual machine status through Azure CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests broad local command authority and includes write authority even though its documented Azure behavior is mostly read-only. <br>
Mitigation: Review the skill before installation, restrict granted tools where the agent platform allows it, and run Azure CLI commands with a least-privilege Azure identity. <br>
Risk: Azure login and subscription context guidance can affect which tenant or subscription subsequent commands use. <br>
Mitigation: Manually approve az login and az account set actions, then verify the active identity and subscription with az account show before interpreting results. <br>
Risk: The security and compliance claims are unreliable unless the publisher tightens the scope and removes unnecessary authority. <br>
Mitigation: Treat the skill as an inventory helper only and independently validate security, RBAC, compliance, and cost findings with approved processes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/azure-cloud-architect-free) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline Azure CLI command blocks and tabular or JSON query outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs depend on the local Azure CLI session, permissions, selected subscription, and user-approved command execution.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
