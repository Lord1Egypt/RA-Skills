## Description:

泛微 e-office 协同办公系统 OpenAPI - 用户管理、部门管理、审批流程、考勤等企业级 API

This skill is ready for commercial/non-commercial use.

## Publisher:

[quanruxiaohong](https://clawhub.ai/user/quanruxiaohong)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and enterprise administrators use this skill to let an agent query and operate a configured e-office OA system, including users, departments, workflows, attendance records, notifications, modeling data, and attachments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create, edit, and delete users, departments, modeling data, and attachments in a live OA system.

Mitigation: Use scoped application credentials, prefer test environments for validation, and require explicit confirmation before create, edit, delete, upload, or download actions.

Risk: Access tokens and application secrets are required, and the token helper prints tokens to stdout.

Mitigation: Avoid logging token output, keep credentials out of shared transcripts and source files, and rotate credentials if exposed.

Risk: Connecting to non-HTTPS or overbroad OA endpoints can expose sensitive enterprise data.

Mitigation: Configure HTTPS-only OA endpoints and restrict the e-office application account to the minimum permissions needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/quanruxiaohong/skills/eoffice-api)
- [e-office OpenAPI reference](references/api.md)
- [OA Open Platform application management](https://service.e-office.cn/knowledge/detail/49/ke7d0a3)
- [ClawDIS homepage](https://github.com/yourname/eoffice-skill)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate authenticated API requests against a configured e-office OA endpoint.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
