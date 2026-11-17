## Description:

使用 `baijimu` CLI 开发和部署 Hosted Service 后端，包括独立 Project/Git、Rust BuildJob、统一 Artifact 目录、数据库迁移 Artifact、Environment、Slot、Deployment、Endpoint、配置和服务鉴权。

This skill is ready for commercial/non-commercial use.

## Publisher:

[momoplan](https://clawhub.ai/user/momoplan)

### License/Terms of Use:

MIT-0

## Use Case:

开发者和工程师使用该技能通过 `baijimu` CLI 交付 Hosted Service 后端应用，覆盖构建、Artifact 管理、环境配置、数据库迁移、部署、Endpoint 验证和服务鉴权。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on an unpinned `@baijimu/cli` package and may execute deployment or migration workflows with sensitive workspace access.

Mitigation: Use a pinned or otherwise verified CLI version for production-sensitive environments, and confirm credentials are least-privileged before running deployment or migration commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/momoplan/skills/baijimu-hosted-service-development)
- [Baijimu Hosted Service backend development documentation](https://docs.baijimu.com/development/backend-development/)
- [Baijimu database migrations documentation](https://docs.baijimu.com/development/backend-development/database-migrations/)
- [Baijimu platform skill homepage](https://github.com/momoplan/baijimu-platform-skill)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the `baijimu` CLI and terminal access.]

## Skill Version(s):

1.6.1 (source: frontmatter and server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
