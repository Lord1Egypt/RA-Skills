## Description: <br>
Create, view, and manage Alibaba Cloud DTS data migration/synchronization tasks interactively. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to create, inspect, start, suspend, and release Alibaba Cloud DTS migration or synchronization tasks through guided CLI workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create, start, suspend, and delete Alibaba Cloud DTS data-migration jobs, which may affect production data flows or incur charges. <br>
Mitigation: Use a least-privilege RAM role and review every region, source, destination, and job summary before approving creation, start, suspend, or delete actions. <br>
Risk: Task release is irreversible, and forced deletion of active migration or synchronization jobs can interrupt data movement. <br>
Mitigation: Query task status before deletion, warn when a task is active, and require explicit double confirmation before release. <br>
Risk: DTS setup may involve database passwords, access keys, certificates, or private keys. <br>
Mitigation: Mask secrets in all user-facing output, avoid writing secrets to local files, and provide production credentials only when required for the migration. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sdk-team/alibabacloud-dts-task-manager) <br>
- [Environment Setup](references/setup.md) <br>
- [Create Data Migration/Synchronization Task](references/create-task.md) <br>
- [View Task List](references/list-tasks.md) <br>
- [View Task Status](references/task-status.md) <br>
- [Start/Resume Task](references/start-task.md) <br>
- [Suspend (Stop) Task](references/suspend-task.md) <br>
- [Release (Delete) Task](references/delete-task.md) <br>
- [RAM Permission Configuration](references/ram-policies.md) <br>
- [Aliyun CLI Releases](https://github.com/aliyun/aliyun-cli/releases) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown] <br>
**Output Format:** [Markdown with inline bash commands and tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Masks sensitive values in summaries and displayed commands.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
