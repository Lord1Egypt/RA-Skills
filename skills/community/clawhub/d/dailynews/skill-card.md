## Description: <br>
每日新闻获取技能。通过 API 获取每日新闻摘要和详情，支持按日期查询、热点新闻排行、新闻详情阅读。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vic240821](https://clawhub.ai/user/vic240821) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to retrieve daily Chinese news summaries, ranked hot news, category-filtered news, and article details for a requested date. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts api.cjiot.cc to retrieve news lists and article details. <br>
Mitigation: Use it only when external news API access is acceptable for the environment. <br>
Risk: Broad news-related phrases may trigger the skill more often than expected. <br>
Mitigation: Confirm user intent before fetching news when the request is ambiguous. <br>
Risk: News queries may reveal user interests or requested dates to the external API. <br>
Mitigation: Avoid including personal information or sensitive context in news requests. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vic240821/dailynews) <br>
- [每日新闻 API](https://api.cjiot.cc) <br>
- [Publisher profile](https://clawhub.ai/user/vic240821) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown-formatted news summaries and article details, with optional shell commands for local script execution] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include dates, article IDs, heat scores, categories, summaries, and HTML-stripped article content.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
