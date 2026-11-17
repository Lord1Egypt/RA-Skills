## Description:

DataNexus 数据采集 SDK 接入助手，帮助开发者完成 SDK 选型、接入开发、事件埋点、联调对账、质量评估、问题排查、自动化接入和已接入项目体检。

This skill is ready for commercial/non-commercial use.

## Publisher:

[tencent-adm](https://clawhub.ai/user/tencent-adm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and integration engineers use this skill to select and integrate the appropriate DataNexus SDK for mini-program, mini-game, iOS, Android, and HarmonyOS projects, then validate instrumentation, reconciliation, quality, compliance, and troubleshooting outcomes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automation and diagnostic scripts may read project files and propose edits that affect SDK startup, event reporting, or compliance behavior.

Mitigation: Run the automation only after explicit consent, review every proposed diff, and validate the integration before release.

Risk: DataNexus IDs, access tokens, or secret_key values may be exposed through command-line arguments, generated plan files, shell history, process metadata, logs, backups, or commits.

Mitigation: Avoid production secrets during automation, remove plaintext secrets from generated artifacts where possible, and rotate any real secret already processed by the scripts.

Risk: SDK initialization before privacy consent can create compliance exposure.

Mitigation: Gate SDK startup behind required privacy consent and use the included compliance guidance and quality checks before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tencent-adm/skills/datanexus-sdk-skills)
- [腾讯开源 Publisher Profile](https://clawhub.ai/user/tencent-adm)
- [DataNexus External Reference](https://docs.qq.com/doc/DU29kS3Jsd05yWUxO)
- [SDK 选型决策树](references/通用/选型/SDK选型决策树.md)
- [行为类型枚举表](references/通用/埋点/行为类型枚举表.md)
- [上报参数说明](references/通用/埋点/上报参数说明.md)
- [转化联调指南](references/通用/联调/转化联调指南.md)
- [数据对账](references/通用/联调/数据对账.md)
- [接入质量检查清单](references/通用/质量/接入质量检查清单.md)
- [数据合规指引](references/通用/合规/数据合规指引.md)
- [错误码速查表](references/通用/排障/错误码速查表.md)
- [能力7 自动化接入协议](references/通用/自动化/能力7自动化接入协议.md)
- [自动化接入脚本说明](scripts/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code examples, shell commands, JSON diagnostics, and structured patch proposals]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read local project files and propose or apply edits only after explicit user consent.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
