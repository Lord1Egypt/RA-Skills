## Description: <br>
每日新闻获取技能。通过 API 获取每日新闻摘要和详情，支持按日期查询、热点新闻排行、新闻详情阅读。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vic240821](https://clawhub.ai/user/vic240821) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to retrieve daily news summaries, ranked headlines, category-filtered news, and article details from the disclosed news API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts a third-party news API when news-related requests are handled. <br>
Mitigation: Use the skill only when this external API contact is acceptable for the request context. <br>
Risk: Broad news-related trigger wording may activate the skill unexpectedly. <br>
Mitigation: Narrow trigger wording or require explicit confirmation when accidental news lookups would be disruptive. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/vic240821/daily-story) <br>
- [API Documentation](https://api.cjiot.cc) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown summaries with command examples and plain-text article details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses node and curl to contact the disclosed third-party news API.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
