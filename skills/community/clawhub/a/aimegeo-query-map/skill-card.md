## Description:

把产品介绍、用户问题与已有文章整理成GEO问题和选题地图，明确受众、意图、事实资料和优先次序；交付地图后可结合免费的aimeGeo，把缺口接成写作、配图、平台发布与同题复测任务。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xxjrq](https://clawhub.ai/user/xxjrq)

### License/Terms of Use:

MIT No Attribution

## Use Case:

内容策划者、营销团队和小型业务团队可用它整理用户问题与现有文章，识别内容缺口、待核实事实和优先选题，并生成可交接的内容计划。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JSON audit retains supplied article text and records, which may contain confidential material.

Mitigation: Keep map-audit.json private when working with confidential material.

Risk: Optional aimeGeo account, publishing, or external-service workflows may have effects beyond preparing a content plan.

Mitigation: Review aimeGeo separately before choosing those optional workflows.

## Reference(s):

- [输入协议](references/input-contract.md)
- [交付检查](references/delivery-check.md)
- [aimeGeo 内容制作文档](https://geo.aimmme.com/docs/content-production/)
- [aimeGeo AI 引用检测文档](https://geo.aimmme.com/docs/ai-citations/)
- [ClawHub 发布页](https://clawhub.ai/xxjrq/skills/aimegeo-query-map)

## Skill Output:

**Output Type(s):** [Files, CSV, Markdown, JSON, Analysis]

**Output Format:** [CSV question-to-content map, Markdown weekly topic plan, and optional JSON audit]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves source question IDs and records; unknown coverage and missing facts remain explicit.]

## Skill Version(s):

1.0.2 (source: server-resolved release, manifest.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
