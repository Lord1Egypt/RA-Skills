## Description:

Agent Father helps OpenClaw operators create, onboard, manage, and remove AI employee agents, including Feishu group setup, workspace files, and employee records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[meichuanyi](https://clawhub.ai/user/meichuanyi)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw workspace operators use this skill to create AI employee agents, configure their workspaces, create Feishu chat groups, run onboarding setup, batch-import employee records, and remove agents during offboarding.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scripts can modify external Feishu resources and local OpenClaw workspaces.

Mitigation: Review the skill before installation, test in a non-production OpenClaw workspace, and run it only with service accounts and Feishu permissions scoped for the intended workspace.

Risk: Employee records, contact details, workspace paths, and agent configuration files may be created or updated locally.

Mitigation: Restrict permissions on generated employee records and agent directories, and avoid using sensitive personal data unless the workspace is approved for it.

Risk: Deletion flows can remove agent and workspace directories, especially when forced.

Mitigation: Back up OpenClaw workspaces first and avoid force deletion unless the target agent and workspace paths have been independently verified.

Risk: Scanner guidance reports unsafe deletion and node command-injection paths.

Mitigation: Use only trusted operator input and trusted CSV files until those issues are fixed, and do not run the scripts with shared service accounts or elevated permissions.

Risk: Troubleshooting output may expose Feishu configuration details.

Mitigation: Redact logs before sharing them and rotate Feishu secrets if any troubleshooting output exposes credentials or sensitive app configuration.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/meichuanyi/skills/agent-father)
- [Feishu Open APIs](https://open.feishu.cn/open-apis)
- [Templates Reference](references/templates.md)
- [Create Examples](references/examples/create-examples.md)
- [Employee CSV Sample](references/examples/employees-sample.csv)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and generated JSON/Markdown file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or modifies local OpenClaw agent, workspace, group, onboarding, and employee-record files when its shell scripts are run.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
