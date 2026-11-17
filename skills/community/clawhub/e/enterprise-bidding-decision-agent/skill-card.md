## Description:

基于知了标讯的历史招中标数据，分析具体项目的投标价值、竞争格局、报价参考和废标风险，并生成决策报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhiliaobiaoxun](https://clawhub.ai/user/zhiliaobiaoxun)

### License/Terms of Use:

MIT-0

## Use Case:

企业投标团队根据具体招标公告、项目名称或招标文件，评估是否参与投标，并参考历史采购、潜在竞争者和成交价格制定策略。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Project and company queries are sent to a third-party bidding service.

Mitigation: Avoid submitting confidential details; review the service's data handling before use.

Risk: API credentials may be stored in a local configuration file.

Mitigation: Protect the local key, limit access to the configuration file, and rotate it if exposed.

Risk: Optional registration sends a hashed device MAC address.

Mitigation: Require informed consent before registration; use a preconfigured key to skip device registration.

Risk: Shareable reports may retain signed access links to source records.

Mitigation: Remove signed links before sharing reports unless recipients are intended to use them.

Risk: Request and update behavior is specified partly in source comments.

Mitigation: Review those instructions before deployment and verify update notices before acting on them.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/zhiliaobiaoxun/skills/enterprise-bidding-decision-agent)
- [API quick reference](artifact/references/api-quick.md)
- [Decision workflow](artifact/references/workflow.md)
- [Report template](artifact/references/report-template.md)
- [Automatic registration](artifact/references/auto-register.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, HTML files, Guidance]

**Output Format:** [Markdown decision report; shareable HTML report in full mode]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a recommendation, supporting data and caveats; analysis uses metered API credits.]

## Skill Version(s):

1.0.6 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
