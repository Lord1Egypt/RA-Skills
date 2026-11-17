## Description:

从真实 AI 回答和原生引用复测品牌提及、链接引用及同题前后变化。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xxjrq](https://clawhub.ai/user/xxjrq)

### License/Terms of Use:

MIT-0

## Use Case:

品牌与内容团队可用此技能整理导出的 AI 回答和原生引用，按平台与相同问题比较品牌提及及链接引用变化。它输出可追溯的样本报告和未采集清单，帮助规划后续复测。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reports retain original records and may include sensitive content.

Mitigation: Keep exports and reports private. Review sensitive content before optional online sampling or publication.

Risk: Optional online sampling sends questions to selected services through logged-in accounts.

Mitigation: Review questions for sensitive content before sending them, and publish only approved content.

Risk: The helper depends on the idna package for domain handling.

Mitigation: Use idna 3.15 or newer within the declared dependency range.

## Reference(s):

- [Input format and measurement rules](references/input-format.md)
- [aimeGeo](https://github.com/aiispower/aimegeo)
- [GEO Optimization monitoring design reference](https://clawhub.ai/capt-marbles/geo-optimization)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSON, Guidance]

**Output Format:** [Markdown reports and JSON evidence records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a comparison report, per-platform results, and a collection-gap list; conclusions are limited to supplied evidence.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata, manifest.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
