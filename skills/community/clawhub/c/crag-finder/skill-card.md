## Description:

当用户查找野攀岩场、攀岩区域、抱石场所或特定地区的攀岩目的地时，该技能使用 theCrag.com 和搜索结果帮助查找并整理岩场信息。

This skill is ready for commercial/non-commercial use.

## Publisher:

[lixin0217](https://clawhub.ai/user/lixin0217)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to find outdoor climbing and bouldering areas by country, region, city, or crag name. It returns concise Chinese-language summaries with route counts, difficulty range, climbing style, access notes, coordinates when available, and theCrag links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: theCrag pages or web search results may be incomplete, outdated, or blocked by anti-bot protections.

Mitigation: Provide direct theCrag links, summarize only available evidence, and tell users when data could not be fetched directly.

Risk: Climbing area data is community-maintained and may omit route conditions, access restrictions, seasonal limits, or local safety updates.

Mitigation: Present route and access details as informational guidance and encourage checking current local sources before climbing.

Risk: The skill is optimized for Chinese output, which may not match every user's preferred language.

Mitigation: Non-Chinese users can ask the agent to respond in their preferred language.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lixin0217/skills/crag-finder)
- [theCrag.com](https://www.thecrag.com/)
- [theCrag API documentation](https://www.thecrag.com/en/article/api)
- [theCrag URL patterns reference](references/url_patterns.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Structured Markdown in Chinese with links and concise field summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include direct theCrag URLs, fallback search summaries, and caveats about community-maintained climbing data.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
