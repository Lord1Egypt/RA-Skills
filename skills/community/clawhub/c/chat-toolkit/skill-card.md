## Description:

面向团队与企业的沟通偏好管理工具，支持多用户共享、版本回滚、跨设备同步、偏好分析、场景切换及跨Agent迁移。

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Team leads, developers, product managers, and multi-agent users use this skill to manage communication preferences across teams, devices, scenarios, and agent platforms. It provides guidance and command examples for baselines, history rollback, sync, analytics, scene switching, and preference migration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Preference files may be synced to Git or object storage.

Mitigation: Review what is included before enabling sync, store credentials in secure locations, and avoid syncing private preferences unless intended.

Risk: Automatic scene switching may change agent communication style based on inferred context.

Mitigation: Enable automatic scene switching only when context-based style changes are acceptable and review scene rules before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/chat-toolkit)
- [Publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash, YAML, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated configuration examples, workflow steps, and safety guidance for sync and preference automation.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
