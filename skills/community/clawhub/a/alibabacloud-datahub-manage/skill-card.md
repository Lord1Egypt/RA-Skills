## Description: <br>
Alibaba Cloud DataHub full-lifecycle resource management skill for creating, querying, updating, and deleting DataHub Projects, Topics, and Subscriptions via Aliyun CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to manage Alibaba Cloud DataHub projects, topics, and subscriptions through guided Aliyun CLI workflows. It helps confirm parameters, apply required RAM permissions, run lifecycle commands in dependency order, and verify results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cloud credentials may be exposed if users paste secrets into chat, shell history, logs, or command arguments. <br>
Mitigation: Prefer OAuth, short-lived STS credentials, RAM roles, or a secrets manager; check credential status without printing secret values. <br>
Risk: Create, update, and delete commands can change or remove Alibaba Cloud DataHub resources. <br>
Mitigation: Review generated commands before execution, confirm all resource parameters, and require explicit approval before destructive operations. <br>
Risk: Insufficient RAM permissions can cause failed or partially completed workflows. <br>
Mitigation: Use the documented DataHub RAM permissions and pause remediation until the user confirms required access has been granted. <br>


## Reference(s): <br>
- [RAM Permissions Required](references/ram-policies.md) <br>
- [Related CLI Commands](references/related-commands.md) <br>
- [Success Verification Method](references/verification-method.md) <br>
- [Acceptance Criteria](references/acceptance-criteria.md) <br>
- [Aliyun CLI Installation and Configuration Guide](references/cli-installation-guide.md) <br>
- [DataHub Product Docs](https://www.aliyun.com/product/datahub) <br>
- [DataHub Help Center](https://help.aliyun.com/zh/datahub/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands require explicit user confirmation for user-customizable parameters and destructive operations.] <br>

## Skill Version(s): <br>
0.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
