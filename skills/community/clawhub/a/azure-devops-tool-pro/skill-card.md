## Description:

Azure DevOps 专业版 helps agents support enterprise Azure DevOps workflows including work item operations, pipeline monitoring, pull request creation, multi-project coordination, and permission audits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and DevOps teams use this skill to inspect Azure DevOps projects and repositories, create pull requests, manage work items, monitor CI/CD status, run batch operations, and prepare permissions or compliance reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad read, write, and command authority for Azure DevOps workflows.

Mitigation: Use narrowly scoped Azure DevOps personal access tokens and avoid organization-wide permissions unless they are required for the specific task.

Risk: Batch operations, pull request creation, work item changes, and webhook notifications can affect many repositories or users.

Mitigation: Require the agent to show the target organization, project, repository list, and a dry-run summary before making changes or sending notifications.

Risk: Credential exposure could occur when configuring Azure DevOps PATs or inspecting environment variables.

Mitigation: Store credentials in environment variables or a secret manager, redact token values in output, and avoid hardcoding secrets in commands or configuration.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/thcjp/skills/azure-devops-tool-pro)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, code, guidance]

**Output Format:** [Markdown guidance with shell, JSON, and Python examples plus structured status and log output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Azure DevOps REST API calls, environment variable configuration, batch operation summaries, audit notes, and error-handling guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
