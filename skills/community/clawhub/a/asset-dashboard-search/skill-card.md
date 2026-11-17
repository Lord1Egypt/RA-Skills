## Description:

专利资产看板检索技能，封装多个智慧芽专利检索API能力，支持按申请人、关键词等维度检索专利，返回去重后的专利列表。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and patent-analysis users use this skill to retrieve patent asset-board data from Zhihuiya patent search APIs by applicant, keyword, patent type, industry category, receiving office, inventor ranking, and innovation word cloud.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Zhihuiya API token for patent searches.

Mitigation: Use the ZHIHUIYA_API_TOKEN environment variable rather than passing tokens on the command line.

Risk: Untrusted applicant names may produce unintended or misleading patent-search queries.

Mitigation: Validate or review applicant names before using them in API-backed searches.

Risk: P002 count results may be unreliable while the documented collapse_order_authority conflict remains unresolved.

Mitigation: Treat P002 counts cautiously and align requests with the documented guidance to avoid collapse_order_authority where it affects counts.

## Reference(s):

- [API 调用说明](references/api_notes.md)
- [Zhihuiya Open Platform](https://open.zhihuiya.com/)
- [ClawHub Skill Page](https://clawhub.ai/yuanzhian-patsnap/skills/asset-dashboard-search)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance]

**Output Format:** [Markdown guidance with JSON request and response examples plus Python command-line helper output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call Zhihuiya APIs when a valid API token and configured agent environment are available.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
