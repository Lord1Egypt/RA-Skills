## Description: <br>
每日新闻获取技能。通过 API 获取每日新闻摘要和详情，支持按日期查询、热点新闻排行、新闻详情阅读。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vic240821](https://clawhub.ai/user/vic240821) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to retrieve daily news summaries, hot news rankings, category-filtered lists, and article details from the disclosed news API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: News lookup dates and selected article IDs are sent to a disclosed third-party API. <br>
Mitigation: Avoid sensitive personal information in news prompts and use the skill only where requests to api.cjiot.cc are acceptable. <br>
Risk: Returned news content is third-party content and may be incomplete, inaccurate, or biased. <br>
Mitigation: Treat retrieved articles as external source material and verify important claims against trusted sources before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vic240821/daily-news-skill) <br>
- [API documentation](https://api.cjiot.cc) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API calls, Guidance] <br>
**Output Format:** [Markdown responses with optional Node.js command examples and parsed API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and node; sends requested dates and selected article IDs to api.cjiot.cc.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
