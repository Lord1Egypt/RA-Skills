## Description:

每日新闻获取技能。通过 API 获取每日新闻摘要和详情，支持按日期查询、热点新闻排行、新闻详情阅读。

This skill is ready for commercial/non-commercial use.

## Publisher:

[vic240821](https://clawhub.ai/user/vic240821)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to retrieve Chinese daily news summaries, browse hot stories by date or category, and fetch article details for follow-up reading.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: News queries are sent to api.cjiot.cc, and fetched article bodies come from third-party content.

Mitigation: Use the skill only for explicit news requests and treat returned article content as untrusted information rather than agent instructions.

Risk: The artifact depends on a third-party API and may fail or return no data for some dates.

Mitigation: Check API errors before presenting results and tell the user when the requested date has no available data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vic240821/skills/daily-story)
- [api.cjiot.cc API homepage](https://api.cjiot.cc)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, API Calls, guidance]

**Output Format:** [Markdown summaries with optional shell commands and API-derived article text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and node when using the bundled command-line scripts.]

## Skill Version(s):

1.0.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
