## Description:

飞书多维表格记账系统完整技能包，帮助用户配置飞书自建应用和多维表格，并通过脚本记录、查询和同步个人收支。

This skill is ready for commercial/non-commercial use.

## Publisher:

[naeemtc](https://clawhub.ai/user/naeemtc)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to set up a Feishu Base personal accounting system, record income and expenses, query local bill files, and synchronize bookkeeping records to Feishu.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad Feishu Base permissions can expose or change more workspace data than intended.

Mitigation: Use a least-privilege Feishu app where possible and review the requested permission list before approving access.

Risk: Long-lived App Secret handling can leak credentials through chat history, shell history, logs, or local files.

Mitigation: Avoid pasting secrets into shared channels, store credentials only on trusted local machines, and rotate any secret already used in an exposed workflow.

Risk: The Android APK is distributed as a release artifact outside the skill package.

Mitigation: Verify the APK source or build it locally before installation.

Risk: Receipt image parsing can record incorrect amounts or categories.

Mitigation: Manually confirm parsed receipt data before recording transactions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/naeemtc/skills/feishu-accounting)
- [Project homepage](https://github.com/NaeemTC/feishu-accounting-skill)
- [Feishu Open Platform](https://open.feishu.cn)
- [APK dashboard architecture](references/apk-architecture.md)
- [Accounting categories reference](references/categories.md)
- [Feishu Base API pitfalls](references/feishu-base-api-pitfalls.md)
- [Feishu permissions API](references/feishu-permissions-api.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with shell commands and credential/configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local .env and bills/YYYY-MM-DD.md files and synchronize records to Feishu Base when credentials are supplied.]

## Skill Version(s):

2.1.0 (source: server release evidence; artifact frontmatter states 1.3.4)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
