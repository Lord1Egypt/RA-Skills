## Description:

基于飞书知识库多维表格和文档能力的任务管理技能。提供创建任务、创建任务关联文档、修改任务状态等功能，可与外部工具灵活集成。

This skill is ready for commercial/non-commercial use.

## Publisher:

[kwokkwok](https://clawhub.ai/user/kwokkwok)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill to configure an agent for Feishu Bitable-based task management, create task records, create linked wiki documents, update task status, and view task statistics through scripted commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup stores Feishu app credentials in local configuration files.

Mitigation: Treat config/credentials.json and any alternate credential files as secrets, restrict filesystem permissions, and do not commit them.

Risk: Validation and task commands can create persistent Feishu Bitable records and wiki documents.

Mitigation: Run validation only against a dedicated test Bitable/wiki area, or confirm that any created records and documents can be cleaned up manually.

Risk: A broadly privileged Feishu app could affect resources beyond the intended task workspace.

Mitigation: Use a Feishu app limited to a dedicated Bitable/wiki area and grant only the permissions needed for the documented task workflow.

Risk: Installing from a mutable package reference may pull a revision that has not been reviewed.

Mitigation: Prefer a pinned and reviewed release or revision before deploying the skill in shared or production workflows.

## Reference(s):

- [Feishu Open Platform](https://open.feishu.cn/)
- [ClawHub skill page](https://clawhub.ai/kwokkwok/skills/feishu-bitable-tasker)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local credential configuration files and Feishu Bitable/wiki resources when the user runs the documented commands.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
