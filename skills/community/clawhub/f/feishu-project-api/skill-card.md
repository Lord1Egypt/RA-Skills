## Description:

飞书项目Open API技能用于查询、创建、更新和删除工作项，管理流程模板、节点配置、自定义字段、视图和角色权限，并批量分析商机进度与风险。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jimislg](https://clawhub.ai/user/jimislg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and project operations teams use this skill to call Feishu Project Open API endpoints for work item lifecycle management, workflow/template/field/view administration, and opportunity progress risk reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide broad Feishu project administration actions, including deletes and workflow, template, field, view, relation, task, comment, and work-hour mutations.

Mitigation: Use least-privilege Feishu credentials, prefer read-only analysis where possible, and require explicit human confirmation with an affected-object preview before any write or destructive operation.

Risk: Progress and risk analysis may be misleading if work item data is incomplete, stale, or filtered incorrectly.

Mitigation: Review source filters, pagination, and sampled records before acting on generated reports or recommendations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jimislg/skills/feishu-project-api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with API request examples and structured analysis reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include proposed Feishu project mutations; review affected objects before writes.]

## Skill Version(s):

1.0.0 (source: release metadata and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
