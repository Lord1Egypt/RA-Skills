## Description:

This skill helps agents create, query, and list Alibaba Cloud Platform for AI (PAI) workspaces using Aliyun CLI workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, cloud engineers, and AI platform operators use this skill to manage Alibaba Cloud PAI workspaces, including workspace creation, lookup, listing, activation checks, and verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup steps can modify the local CLI environment through install, update, and plugin update behavior.

Mitigation: Review setup before execution, prefer a package manager or pinned verified Aliyun CLI release, and avoid curl-to-bash and global plugin auto-install or update behavior.

Risk: Workspace operations can change Alibaba Cloud account resources.

Mitigation: Use least-privilege RAM credentials and confirm every workspace-changing action before running commands.

Risk: Credential secrets may be exposed if entered directly or passed on command lines.

Mitigation: Use configured profiles, temporary credentials, or role-based authentication; do not ask for, print, or pass credential secrets in commands.

Risk: Workspace deletion is outside the normal create, query, and list workflow and is irreversible.

Mitigation: Treat deletion instructions as out of scope for normal use and require explicit user confirmation and appropriate console or API safeguards before deletion.

## Reference(s):

- [RAM Policies](references/ram-policies.md)
- [Related Commands](references/related-commands.md)
- [Verification Method](references/verification-method.md)
- [Acceptance Criteria](references/acceptance-criteria.md)
- [Aliyun CLI Installation Guide](references/cli-installation-guide.md)
- [ListWorkspaces API Documentation](https://help.aliyun.com/zh/pai/developer-reference/api-aiworkspace-2021-02-04-listworkspaces)
- [CreateWorkspace API Documentation](https://help.aliyun.com/zh/pai/developer-reference/api-aiworkspace-2021-02-04-createworkspace)
- [GetWorkspace API Documentation](https://help.aliyun.com/zh/pai/developer-reference/api-aiworkspace-2021-02-04-getworkspace)
- [ListProducts API Documentation](https://help.aliyun.com/zh/pai/developer-reference/api-aiworkspace-2021-02-04-listproducts)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and concise operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-confirmed parameters, Aliyun CLI 3.3.3 or later, configured Alibaba Cloud credentials, and masked output for workspace queries.]

## Skill Version(s):

0.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
