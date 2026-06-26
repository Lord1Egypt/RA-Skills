## Description: <br>
Creates, queries, and lists Alibaba Cloud Platform for AI (PAI) workspaces. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to manage Alibaba Cloud PAI workspace lifecycle tasks from an agent, including creating workspaces, querying details, and listing workspace inventory while confirming region, permissions, and parameters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can affect Alibaba Cloud account resources by creating and managing PAI workspaces. <br>
Mitigation: Use a least-privilege RAM user or role limited to the documented PAI workspace actions, and require explicit user confirmation for region and workspace parameters before running commands. <br>
Risk: Credential exposure could occur if access keys or raw API responses are printed, logged, saved, or pasted into chat. <br>
Mitigation: Do not request or display access keys; verify credential status only with safe CLI checks, and keep workspace query output masked in a single command pipeline. <br>
Risk: CLI installation, plugin updates, and irreversible deletion guidance can create account or environment changes beyond ordinary documentation lookup. <br>
Mitigation: Review CLI and plugin installation steps before execution, and avoid deletion-related guidance unless the user explicitly requests irreversible removal. <br>


## Reference(s): <br>
- [Acceptance Criteria](references/acceptance-criteria.md) <br>
- [Aliyun CLI Installation and Configuration Guide](references/cli-installation-guide.md) <br>
- [RAM Policies](references/ram-policies.md) <br>
- [Related Commands](references/related-commands.md) <br>
- [Verification Method](references/verification-method.md) <br>
- [Alibaba Cloud CreateWorkspace API](https://help.aliyun.com/zh/pai/developer-reference/api-aiworkspace-2021-02-04-createworkspace) <br>
- [Alibaba Cloud GetWorkspace API](https://help.aliyun.com/zh/pai/developer-reference/api-aiworkspace-2021-02-04-getworkspace) <br>
- [Alibaba Cloud ListWorkspaces API](https://help.aliyun.com/zh/pai/developer-reference/api-aiworkspace-2021-02-04-listworkspaces) <br>
- [Alibaba Cloud ListProducts API](https://help.aliyun.com/zh/pai/developer-reference/api-aiworkspace-2021-02-04-listproducts) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline bash commands, jq filters, and RAM policy JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Aliyun CLI 3.3.3+, Alibaba Cloud credentials, explicit user-confirmed regions and parameters, and masked handling of workspace query outputs.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
