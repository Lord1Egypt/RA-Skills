## Description:

Codeup provides command-line tools that let an agent work with Alibaba Cloud Yunxiao Codeup repositories, branches, files, merge requests, organizations, departments, members, and roles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yu-xiao-sheng](https://clawhub.ai/user/yu-xiao-sheng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to inspect and operate Alibaba Cloud Yunxiao Codeup repositories and organization data through JSON-returning CLI commands. Typical tasks include branch management, file changes, repository comparison, merge request workflows, and organization member queries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a user-provided YUNXIAO_ACCESS_TOKEN to access Alibaba Cloud Codeup repositories and organization data.

Mitigation: Use a least-privilege token scoped to the intended organization and repository operations, and prefer read-only scopes when write access is not needed.

Risk: The skill exposes commands that can change or remove repository state, including delete_branch, delete_file, merge_change_request, and comment deletion.

Mitigation: Review command arguments and target repository, branch, file, merge request, or comment before executing destructive or write operations.

## Reference(s):

- [Code Management API Reference](references/code-management.md)
- [Organization Management API Reference](references/organization-management.md)
- [Codeup Skill on ClawHub](https://clawhub.ai/yu-xiao-sheng/skills/codeup)
- [Alibaba Cloud DevOps OpenAPI Endpoint](https://openapi-rdc.aliyuncs.com)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Code, JSON, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands require YUNXIAO_ACCESS_TOKEN and return JSON responses from Alibaba Cloud DevOps APIs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
