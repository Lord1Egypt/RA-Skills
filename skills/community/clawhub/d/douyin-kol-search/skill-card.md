## Description:

用于搜索和分析抖音对标账号，不仅仅是流量，而是账号的商业价值，降低试错成本。当用户提到“对标账号”“抖音对标账号”“找对标账号”“对标账号分析”“竞品账号”“同行账号”或“同赛道账号”时使用。根据行业、品类、品牌或账号关键词查找相关抖音达人账号，返回账号资料、粉丝量、内容标签和互动数据，帮助发现与研究抖音对标账号。

This skill is ready for commercial/non-commercial use.

## Publisher:

[allinherog-star](https://clawhub.ai/user/allinherog-star)

### License/Terms of Use:

MIT-0

## Use Case:

内容运营人员、创作者和品牌方可按行业关键词、内容分类和粉丝范围发现抖音创作者，并参考账号信息与互动指标筛选对标或合作候选。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are sent to ai-skills.ai and API use may incur charges.

Mitigation: Use a dedicated API key, protect it as a secret, and review expected usage and billing before running searches.

Risk: The skill links to external installation instructions, and provider-side data handling was not verified.

Mitigation: Review installation commands before executing them and consult ai-skills.ai for its current data-handling terms.

Risk: The upstream service may relax requested filters when a filter combination is rejected.

Mitigation: Check searchStrategy.droppedFilters and do not treat results as meeting filters that were relaxed.

## Reference(s):

- [参数结构（form-schema.json）](references/form-schema.json)
- [技能目录信息（skill.json）](references/skill.json)
- [AI Skills 技能说明](https://ai-skills.ai/zh/skills/douyin-kol-search)
- [快速开始](https://github.com/allinherog-star/ai-skills/tree/main#%E5%BF%AB%E9%80%9F%E5%BC%80%E5%A7%8B)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Guidance]

**Output Format:** [JSON account candidate data with explanatory text and filtering guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Paginated candidate results include account details, follower counts, content tags, and interaction or commercial indicators when provided by the data source.]

## Skill Version(s):

1.0.6 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
