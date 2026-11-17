## Description:

按照 OpenClaw 官方规范删除一个或多个 agent（代理），自动完成列表展示、确认、执行删除、移到回收站及历史记录。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangyangupday](https://clawhub.ai/user/yangyangupday)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and operators use this skill to list configured agents, confirm deletion targets, and remove selected agent workspaces and agent directories through a guarded five-step workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted agent IDs may be mishandled by the deletion script.

Mitigation: Validate agent IDs before execution and reject values outside the expected OpenClaw agent identifier format.

Risk: The deletion workflow can move or remove unintended local workspace or session data.

Mitigation: Constrain resolved paths to expected OpenClaw state directories, review the displayed deletion summary, and keep the trash folder until recovery is no longer needed.

Risk: Agent IDs are interpolated into Python code inside the shell script.

Mitigation: Pass IDs as data rather than embedded code and fail safely when lookup or validation fails.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yangyangupday/skills/agent-del)
- [Publisher Profile](https://clawhub.ai/user/yangyangupday)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline bash commands and command output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the openclaw CLI and user confirmation before deletion.]

## Skill Version(s):

1.10.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
