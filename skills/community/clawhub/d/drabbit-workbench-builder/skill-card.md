## Description:

个人工作台搭建器通过 5-7 个问题了解用户职业、工作需求和手机型号，生成个性化单页 PWA 工作台并提供部署与桌面安装指引。

This skill is ready for commercial/non-commercial use.

## Publisher:

[drabbit777](https://clawhub.ai/user/drabbit777)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to interview a user, customize a single-page PWA workbench with task, schedule, finance, project, profile, sync, import, and notification features, then deploy it and provide device-specific installation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional cloud sync can expose personal data if the sync authorization model or CloudBase access rules are weak.

Mitigation: Keep cloud sync disabled unless the authorization model and CloudBase rules have been reviewed and hardened.

Risk: Importing untrusted JSON backups can corrupt workbench data or introduce unsafe content.

Mitigation: Import only trusted backups and validate or escape imported content before using it in a generated workbench.

Risk: The generated app may store personal, schedule, project, or financial records.

Mitigation: Avoid storing sensitive financial or personal records until output escaping and cloud access controls are confirmed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/drabbit777/skills/drabbit-workbench-builder)
- [Template structure](references/template-structure.md)
- [Customization parameters](references/customization-params.md)
- [Bugs and fixes](references/bugs-and-fixes.md)
- [CloudBase console](https://console.cloud.tencent.com/tcb)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with code snippets and generated PWA files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces or modifies deployable PWA assets such as index.html, manifest.webmanifest, sw.js, apple-touch-icon.svg, and cloudbase-sdk.js.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
