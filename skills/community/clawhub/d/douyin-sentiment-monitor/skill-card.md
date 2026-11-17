## Description:

抖音舆情监测助手。针对任意关键词获取抖音作品数据、详情、互动数据、评论数据，基于抖音实时数据，综合分析舆情健康、情感占比、负面信息、事件时间、热度排行、竞品口碑对比与风险建议等，进行分析并输出舆情报告。支持四大能力：(1) 关键词搜索视频/图文，可按点赞数、发布时间、视频时长、内容类型筛选排序；(2) 实时热榜查询，获取抖音热搜词条与热度数据；(3) 博主作品抓取，按主页链接或 sec_uid 获取公开作品列表；(4) 视频评论分析，按视频链接或 aweme_id 获取评论内容与互动数据。

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

内容运营、品牌与投放团队、舆情与客服人员，以及数据分析人员可用此技能查询抖音公开作品、作者、互动、评论和热榜数据，再整理为选题研究、竞品观察或舆情报告。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries send user-provided keywords or links to the third-party Guaikei API.

Mitigation: Use only when sharing those query terms or links with that service is acceptable; avoid including sensitive information.

Risk: ClawScan reports a benign verdict with medium confidence, but inspection was partial and the tool-misuse analyzer was degraded.

Mitigation: Review the skill's stated data handling and third-party API use before installing, and weigh whether that use fits your needs.

## Reference(s):

- [Demand mining guide](references/demand-mining.md)
- [Command options](references/options.md)
- [Changelog](references/changelog.md)
- [Guaikei API and token service](https://www.guaikei.com)
- [ClawHub skill page](https://clawhub.ai/why20261/skills/douyin-sentiment-monitor)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Markdown]

**Output Format:** [Structured JSON query results with concise analysis or reports in Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Available data depends on the selected query and API plan; shared and playback links may expire.]

## Skill Version(s):

1.4.2 (source: SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
