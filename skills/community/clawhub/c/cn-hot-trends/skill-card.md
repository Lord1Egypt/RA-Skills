## Description: <br>
聚合中国主流平台热点榜单，帮助代理获取实时热搜、热议、科技、财经、影视、音乐等多维度热点内容。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SunGang-pine](https://clawhub.ai/user/SunGang-pine) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to gather and summarize public Chinese trending-topic lists across platforms such as Weibo, Baidu, Zhihu, Douyin, Bilibili, 36Kr, and Huxiu. It supports general daily trend briefs as well as platform- or category-specific trend lookups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Some platform requests may require cookies or user-agent headers, and cookies can act like account access. <br>
Mitigation: Use public trend lookups by default and provide cookies only when necessary for the specific query and after understanding the account-access implications. <br>
Risk: Broad activation phrases may cause the skill to be used for general public trend lookups across several sites. <br>
Mitigation: Keep use to public trending-topic retrieval and limit each aggregation to a small set of relevant platforms. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/SunGang-pine/cn-hot-trends) <br>
- [Weibo Hot Search API](https://weibo.com/ajax/side/hotSearch) <br>
- [Baidu Realtime Hot Search](https://top.baidu.com/board?tab=realtime) <br>
- [Zhihu Billboard](https://www.zhihu.com/billboard) <br>
- [Bilibili Popular Ranking](https://www.bilibili.com/v/popular/rank/all) <br>
- [36Kr Hot List](https://36kr.com/hot-list/catalog) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown trend brief with optional inline PowerShell examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include platform sections, ranked topic lists, heat indicators, keyword summaries, and graceful skips when a platform cannot be fetched.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
