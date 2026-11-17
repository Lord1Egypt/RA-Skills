## Description:

Helps agents create, query, and list Alibaba Cloud MaxCompute (ODPS) projects using Aliyun CLI workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to manage Alibaba Cloud MaxCompute projects through Aliyun CLI commands. It supports listing projects, retrieving project details, creating projects after quota checks, and reporting unsupported deletion requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installer guidance includes a remote shell script and plugin-update steps that can make persistent local changes.

Mitigation: Review installation steps before use, prefer a trusted package manager or verified download, and avoid piping remote scripts directly into bash.

Risk: MaxCompute project creation can create billable cloud resources.

Mitigation: Require explicit user confirmation for create operations and use least-privilege RAM credentials with only the actions needed for the workflow.

Risk: The requested RAM permissions use broad resource scopes for project and quota operations.

Mitigation: Review RAM policy scope before installation and restrict permissions to specific projects or environments where feasible.

Risk: Enabling automatic plugin installation can change future CLI behavior without per-plugin review.

Mitigation: Do not enable global automatic plugin installation unless the operator accepts that persistent configuration change.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sdk-team/skills/alibabacloud-odps-project-manage)
- [CLI Installation Guide](artifact/references/cli-installation-guide.md)
- [Acceptance Criteria](artifact/references/acceptance-criteria.md)
- [Related APIs](artifact/references/related-apis.md)
- [Verification Method](artifact/references/verification-method.md)
- [RAM Policies](artifact/references/ram-policies.md)
- [MaxCompute Product Page](https://api.aliyun.com/product/MaxCompute)
- [CreateProject API](https://api.aliyun.com/api/MaxCompute/2022-01-04/create-project)
- [GetProject API](https://api.aliyun.com/api/MaxCompute/2022-01-04/get-project)
- [ListProjects API](https://api.aliyun.com/api/MaxCompute/2022-01-04/list-projects)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided region and project parameters before executing cloud operations.]

## Skill Version(s):

0.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
