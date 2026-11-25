## Description:

研究抖音搜索结果、作品结构、达人数据和用户反馈，筛选值得继续验证的机会。当用户询问抖音选题、抖音增长或用户痛点时使用。支持关键词搜索视频与图文、实时热榜查询、作品详情、博主作品抓取和视频评论分析。

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT-0

## Use Case:

短视频运营、品牌与增长团队可用它检索抖音公开视频、达人作品、评论和热榜数据，并整理选题、竞品、舆情或用户需求线索。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and supplied Douyin links or IDs are sent to guaikei.com for processing.

Mitigation: Obtain the user's agreement before querying and avoid confidential or personally sensitive inputs.

Risk: Keyword-based account discovery is not clearly disclosed in the scan summary, and some package components were only partially analyzed.

Mitigation: Review the account-search behavior before enabling it and limit use to public-data research.

## Reference(s):

- [参数与筛选选项](references/options.md)
- [评论需求挖掘指南](references/demand-mining.md)
- [评论区获客指南](references/customer-acquisition.md)
- [服务与令牌信息](https://www.guaikei.com)
- [ClawHub 技能发布页](https://clawhub.ai/why20261/skills/douyin-opportunity-research)

## Skill Output:

**Output Type(s):** [JSON, Text, Guidance]

**Output Format:** [Structured JSON data with concise research summaries and tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returned fields vary by query; results can be saved for downstream analysis.]

## Skill Version(s):

1.5.0 (source: release metadata, frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
