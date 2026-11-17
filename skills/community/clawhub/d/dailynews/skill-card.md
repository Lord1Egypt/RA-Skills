## Description:

每日新闻获取技能，通过 API 获取每日新闻摘要和详情，支持按日期查询、热点新闻排行和新闻详情阅读。

This skill is ready for commercial/non-commercial use.

## Publisher:

[vic240821](https://clawhub.ai/user/vic240821)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to request Chinese daily news summaries, ranked headlines, category-filtered news, and article details for a current or specified date.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-requested dates and article IDs are sent to api.cjiot.cc when retrieving news lists or article details.

Mitigation: Install and use the skill only where outbound requests to this news API are acceptable, and avoid placing sensitive personal context in news queries.

Risk: The broad Chinese news trigger terms may activate the skill for ambiguous requests.

Mitigation: Confirm the user's news intent before calling the API when a request containing news-related keywords is ambiguous.

Risk: The skill depends on availability and responses from an external API.

Mitigation: Handle API errors, missing dates, and non-200 responses by telling the user that news data is unavailable rather than fabricating results.

## Reference(s):

- [Daily News API](https://api.cjiot.cc)
- [ClawHub Skill Page](https://clawhub.ai/vic240821/skills/dailynews)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown-style Chinese news summaries and article details, with optional Node shell commands for direct API retrieval.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include article IDs, heat scores, publication timestamps, summaries, and HTML-stripped article content returned by the remote API.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
