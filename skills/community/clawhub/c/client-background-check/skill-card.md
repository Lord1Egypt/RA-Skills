## Description:

基于公开招投标记录生成客户或竞对的采购、合作关系、中标表现与公开风险调查报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[dragonzu](https://clawhub.ai/user/dragonzu)

### License/Terms of Use:

MIT-0

## Use Case:

销售和商务拓展人员在拜访或合作前，利用招投标记录了解客户的采购习惯、供应商格局及预算量级；也可比较两家企业。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic trial registration sends a MAC-derived device hash for account deduplication.

Mitigation: Obtain explicit consent before registration, or preconfigure ZLBX_API_KEY to bypass it.

Risk: The API key persists in a local configuration file.

Mitigation: Protect ~/.zlbx/config.json and avoid exposing the key in reports or conversations.

Risk: Report links can contain signed access tokens and remain accessible when shared.

Mitigation: Review report recipients and signed links before sharing or publishing reports.

Risk: Research calls consume account credits and conclusions may be misleading when coverage is incomplete.

Mitigation: Disclose expected credit use, cite supporting records, and label missing data and coverage limits.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/dragonzu/skills/client-background-check)
- [API quick reference](references/api-quick.md)
- [Investigation workflow](references/workflow.md)
- [Report templates](references/report-template.md)
- [Account registration and privacy](references/auto-register.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, HTML report]

**Output Format:** [Markdown investigation report and shareable HTML file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Single-company analysis or two-company comparison, with citations and data gaps.]

## Skill Version(s):

1.0.6 (source: release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
