## Description: <br>
DataWorks Workspace Lifecycle Management Skill for creating workspaces, querying workspace information, and adding workspace members with role authorization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to manage allowed Alibaba Cloud DataWorks workspace lifecycle tasks, including workspace creation, workspace and member lookup, member addition, and role grants. It is intended to keep destructive workspace and membership changes out of the agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setup guidance can lead to broader Alibaba Cloud permissions than the skill needs. <br>
Mitigation: Use a dedicated least-privilege RAM user or role, remove dataworks:UpdateProject from copied policies, and avoid AliyunDataWorksFullAccess unless it is truly necessary. <br>
Risk: Mutating workspace or membership commands can affect the wrong region, workspace, user, or role if parameters are not checked. <br>
Mitigation: Explicitly verify the region, workspace, target user, and role codes before running any mutating command. <br>
Risk: Unsupported destructive actions could update or delete workspaces, remove members, or revoke roles. <br>
Mitigation: Do not perform or generate commands for UpdateProject, DeleteProject, DeleteProjectMember, or RevokeMemberProjectRoles; direct users to the DataWorks Console for those actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sdk-team/alibabacloud-dataworks-workspace-manage) <br>
- [DataWorks Workspace Management](https://help.aliyun.com/zh/dataworks/user-guide/workspace-management/) <br>
- [Add Workspace Members](https://help.aliyun.com/zh/dataworks/user-guide/add-workspace-members-and-assign-roles-to-them) <br>
- [DataWorks OpenAPI Reference](https://help.aliyun.com/zh/dataworks/developer-reference/api-dataworks-public-2024-05-18-overview) <br>
- [DataWorks Workspace Management - API and CLI Command Reference](references/related-apis.md) <br>
- [DataWorks Workspace Management - RAM Permission Policies](references/ram-policies.md) <br>
- [DataWorks Service Endpoints](references/endpoint-regions.md) <br>
- [DataWorks Workspace Management - Operation Verification Methods](references/verification-method.md) <br>
- [Aliyun CLI Installation & Configuration Guide](references/cli-installation-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash command examples and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands should include explicit region, endpoint, user-agent, and timeout parameters where applicable.] <br>

## Skill Version(s): <br>
0.0.2 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
