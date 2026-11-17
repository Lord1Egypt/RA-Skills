## Description:

端到端应用开发。当用户需要创建Web应用、管理系统或进行Vibe Coding时使用，从需求到部署全流程独立完成。

This skill is ready for commercial/non-commercial use.

## Publisher:

[kuafuai](https://clawhub.ai/user/kuafuai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and builders use this skill to create web applications, admin systems, and vibe-coding projects backed by AiPexBase BaaS. It guides the agent from requirements documentation and schema design through frontend integration, configuration, and deployment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Administrator tokens may be written to local config files and copied into project directories.

Mitigation: Use a scoped or disposable token where possible, keep config files out of version control, and rotate the token if it may have been exposed.

Risk: Setup guidance includes shell-based dependency installation and global package installation.

Mitigation: Review setup commands before execution and install prerequisites through trusted, pinned package sources.

Risk: Deployment packaging can accidentally include secret-bearing config files.

Mitigation: Inspect deployment archives and exclude config files containing tokens or API keys before upload.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kuafuai/skills/baas)
- [AiPexBase JS API Reference](artifact/references/aipexbase-js-api.md)
- [Deployment Guide](artifact/references/deploy.md)
- [HTML Template](artifact/references/html-template.html)
- [PRD Template](artifact/references/prd-template.md)
- [Style Guide](artifact/references/style-guide.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON, HTML/JavaScript, and bash snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce prd.md, app-schema.json, baas-config.json, frontend app files, and deployment package instructions.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
