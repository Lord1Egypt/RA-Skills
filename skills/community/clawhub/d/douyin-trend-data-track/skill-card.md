## Description:

检索抖音公开视频、账号作品、评论和实时热榜，并整理为结构化 JSON，支持短视频选题、竞品分析与舆情研究。

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT-0

## Use Case:

短视频运营、内容分析、品牌投放和数据分析人员可用它搜索抖音内容与账号、查看作品和评论、追踪热榜，并将公开数据整理为选题、竞品或舆情分析材料。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags account-search behavior beyond the stated capabilities and broad activation triggers; some referenced files were only partially analyzed.

Mitigation: Review the account-search command and referenced files before enabling the skill, and invoke account discovery only for an explicit user request.

Risk: Search terms and supplied Douyin links are sent to the external Guaikei service.

Mitigation: Tell the user before running a query and avoid sending sensitive terms or links.

## Reference(s):

- [Quick start and command reference](readme.md)
- [Output contract](references/contract.md)
- [Search options](references/options.md)
- [Demand mining guide](references/demand-mining.md)
- [Customer acquisition guide](references/customer-acquisition.md)
- [Release changelog](references/changelog.md)
- [Service and token information](https://www.guaikei.com)
- [Publisher profile](https://clawhub.ai/user/why20261)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Guidance, Shell commands]

**Output Format:** [Structured JSON results with concise analysis and command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May contain public creator and engagement data; results can be saved under the skill's logs directory.]

## Skill Version(s):

1.5.0 (source: release evidence, changelog, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
