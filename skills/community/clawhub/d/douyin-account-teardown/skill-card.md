## Description:

获取抖音真实一手数据，逆向拆解抖音平台账号，根据账号互动数据及账号作品数据，产出可复刻的运营手册。当用户提出「拆解某账号」「分析对标号」「看看XX号为什么火」「复刻这个账号的风格」「抓取抖音账号数据」「竞品账号分析」「对标账号数据」「账号诊断」等需求时使用。产出结构化数据 + 互动指标 + 形态拆解 + 差距定位。支持五大能力：(1) 关键词搜索视频/图文，可按点赞数、发布时间、视频时长、内容类型筛选排序；(2) 实时热榜查询，获取抖音热搜词条与热度数据；(3) 单条作品详情，按视频链接或 aweme_id 获取文案、互动与作者；(4) 博主作品抓取，按主页链接或 sec_uid 获取公开作品列表；(5) 视频评论分析，按视频链接或 aweme_id 获取评论内容与互动数据。

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT-0

## Use Case:

内容运营、营销和数据分析人员可用此技能检索抖音公开视频、账号、作品详情、评论和热榜数据，并据此整理对标分析、选题思路和舆情洞察。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and Douyin links or IDs are sent to the Guaikei API for processing.

Mitigation: Use public content only, avoid submitting sensitive information, and review the service's terms before providing inputs.

Risk: Comment analysis can be used to identify potential customer leads, extending beyond account and content analysis.

Mitigation: Keep analysis limited to legitimate, platform-compliant research; do not infer private contact details or automate unsolicited outreach.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/why20261/skills/douyin-account-teardown)
- [Publisher profile](https://clawhub.ai/user/why20261)
- [Guaikei API and support](https://www.guaikei.com)
- [Routing guide](references/routing.md)
- [Demand mining guide](references/demand-mining.md)
- [Customer acquisition guide](references/customer-acquisition.md)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Guidance]

**Output Format:** [Structured JSON data with concise text or Markdown analysis and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses public Douyin data; the skill does not log in, publish, like, or comment.]

## Skill Version(s):

1.5.0 (source: SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
