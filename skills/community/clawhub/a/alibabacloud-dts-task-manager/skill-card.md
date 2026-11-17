## Description:

Create, view, and manage Alibaba Cloud DTS data migration and synchronization tasks interactively.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to set up, create, inspect, start, suspend, and delete Alibaba Cloud DTS migration or synchronization tasks through guided CLI workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create postpaid DTS instances and start migration or synchronization jobs that may incur cloud charges.

Mitigation: Review task settings before execution, require user confirmation for billable actions, and release partially created instances if configuration or startup fails.

Risk: The skill can delete DTS jobs, including active jobs, which may interrupt migrations or synchronization.

Mitigation: Check task status before deletion, clearly warn on active states, and require explicit double confirmation before calling DeleteDtsJob.

Risk: The skill collects database passwords, AccessKey secrets, certificates, and private keys for local CLI and DTS API workflows.

Mitigation: Mask sensitive values in conversation output, avoid writing secrets to files or logs, and only provide high-value credentials when acceptable for the local CLI and DTS API path.

Risk: Broad Alibaba Cloud DTS permissions increase the blast radius of mistakes or misuse.

Mitigation: Use a narrowly scoped RAM user or role with only the required DTS and read-only instance-listing permissions for the intended operations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sdk-team/skills/alibabacloud-dts-task-manager)
- [Publisher profile](https://clawhub.ai/user/sdk-team)
- [Environment Setup](references/setup.md)
- [Create Data Migration/Synchronization Task](references/create-task.md)
- [View Task List](references/list-tasks.md)
- [View Task Status](references/task-status.md)
- [RAM Permission Configuration](references/ram-policies.md)
- [Release (Delete) Task](references/delete-task.md)
- [Alibaba Cloud CLI releases](https://github.com/aliyun/aliyun-cli/releases)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, markdown]

**Output Format:** [Markdown with inline bash commands and tabular task summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include masked credentials, DTS instance IDs, job IDs, task status, progress, delay, and Alibaba Cloud CLI commands.]

## Skill Version(s):

0.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
