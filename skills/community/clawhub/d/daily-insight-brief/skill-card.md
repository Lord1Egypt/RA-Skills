## Description:

Daily morning brief（8:30 Beijing time）自动收集、交叉验证并提炼来自广域来源的商业、科技、金融等领域信息，产出10-15条要点性简报。每条包含：标题/要点、来源（名称+链接）、关键数据点、分析评论（1-2句）、核心观点、验证状态（已验证 / 待核实）。

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexweng123](https://clawhub.ai/user/alexweng123)

### License/Terms of Use:


## Use Case:

Employees, external users, and developers can use this skill to generate a Chinese-language daily morning brief covering business, technology, finance, markets, and research from broad public sources. It is intended to produce concise brief items with source links, key data points, short analysis, core takeaways, and verification status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled or external delivery could send reports to unintended destinations if channels, credentials, or opt-in controls are not confirmed.

Mitigation: Confirm destinations, credentials, schedule settings, and opt-in controls before enabling any real scheduler, Feishu delivery, email delivery, or channel delivery.

Risk: Brief items may include public-source claims that are not fully verified at generation time.

Mitigation: Preserve the per-item verification status and evidence notes, and treat items marked pending verification as leads that need follow-up before decision-making.

## Reference(s):

- [Daily Insight Brief source list](references/source_list.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Structured Markdown brief in Chinese with source links, data points, analysis, takeaways, verification status, and notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Typically 10-15 brief items per output; each item includes verification status and evidence notes.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
