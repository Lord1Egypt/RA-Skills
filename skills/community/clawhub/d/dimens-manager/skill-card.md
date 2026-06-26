## Description: <br>
用于维表智联项目内业务资源创建、配置、维护和排查，适合处理 Key、团队、项目、表格、权限、工作流、报表、画布等落地问题。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[flyowl](https://clawhub.ai/user/flyowl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to manage Dimens project resources, including authentication, teams, projects, tables, permissions, workflows, reports, and canvases. It helps route tasks to the right reference material and produce operational guidance, CLI commands, API examples, and configuration payloads. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive credentials, OAuth tokens, or API secrets could be exposed through chat logs, shell history, or local profile storage. <br>
Mitigation: Avoid pasting real secrets into chats or command lines, store returned secrets in a secrets manager, and review local profile token storage before use. <br>
Risk: Write, delete, reset, or public-share actions could change business resources or access boundaries unintentionally. <br>
Mitigation: Require explicit confirmation before those actions and review the target operation, affected resource, and expected outcome. <br>
Risk: Commands run against the wrong Dimens team, project, or resource scope could modify unrelated business data. <br>
Mitigation: Check teamId, projectId, resource ownership, and permission scope before running permission, public-view, or resource-changing commands. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/flyowl/dimens-manager) <br>
- [维表智联官网](https://dimens.bintelai.com/) <br>
- [README](artifact/README.md) <br>
- [Skill Definition](artifact/SKILL.md) <br>
- [Key Authentication Overview](artifact/references/key-auth/overview.md) <br>
- [Team Context Overview](artifact/references/team/overview.md) <br>
- [Project Overview](artifact/references/project/overview.md) <br>
- [Table Overview](artifact/references/table/overview.md) <br>
- [Permission Overview](artifact/references/permission/overview.md) <br>
- [Workflow Overview](artifact/references/workflow/overview.md) <br>
- [Approval Workflow Generation](artifact/references/workflow/references/approval-generation.md) <br>
- [Report Overview](artifact/references/report/overview.md) <br>
- [Canvas Overview](artifact/references/canvas/overview.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, code] <br>
**Output Format:** [Markdown with CLI commands, API examples, and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May involve OAuth tokens, API keys, resource identifiers, and write operations that require user confirmation.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
