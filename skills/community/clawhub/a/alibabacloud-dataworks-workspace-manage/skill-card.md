## Description:

DataWorks Workspace Lifecycle Management Skill for creating workspaces, querying workspace information, and adding workspace members with role authorization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to administer Alibaba Cloud DataWorks workspaces through Aliyun CLI workflows for workspace creation, workspace lookup, member addition, and role grants.

### Deployment Geography for Use:

Global, subject to Alibaba Cloud DataWorks regional availability.

## Known Risks and Mitigations:

Risk: Cloud account exposure from broad DataWorks permissions or unreviewed workspace administration.

Mitigation: Review requested RAM permissions before use, remove UpdateProject and FullAccess-style permissions unless approved outside the skill, and prefer narrowly scoped or short-lived credentials.

Risk: Credential leakage through command-line handling or local shell history.

Mitigation: Use the default credential chain, avoid entering cloud secrets on command lines, and confirm credential status without exposing access keys.

Risk: Supply-chain exposure from CLI installation and automatic plugin installation.

Mitigation: Use a verified and pinned Aliyun CLI installation and keep automatic plugin installation disabled unless separately reviewed.

Risk: Irreversible or unsupported workspace changes could affect production environments.

Mitigation: Do not perform prohibited update, delete, member-removal, or role-revocation operations through the skill; use the DataWorks Console for unsupported changes.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sdk-team/skills/alibabacloud-dataworks-workspace-manage)
- [Acceptance Criteria](references/acceptance-criteria.md)
- [Aliyun CLI Installation and Configuration Guide](references/cli-installation-guide.md)
- [DataWorks Service Endpoints](references/endpoint-regions.md)
- [DataWorks Workspace Management RAM Permission Policies](references/ram-policies.md)
- [DataWorks Workspace Management API and CLI Command Reference](references/related-apis.md)
- [DataWorks Workspace Management Operation Verification Methods](references/verification-method.md)
- [DataWorks Workspace Management](https://help.aliyun.com/zh/dataworks/user-guide/workspace-management/)
- [Add Workspace Members](https://help.aliyun.com/zh/dataworks/user-guide/add-workspace-members-and-assign-roles-to-them)
- [DataWorks OpenAPI Reference](https://help.aliyun.com/zh/dataworks/developer-reference/api-dataworks-public-2024-05-18-overview)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Aliyun CLI command patterns with confirmed user parameters, DataWorks endpoints, and role-code guidance.]

## Skill Version(s):

0.0.2 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
