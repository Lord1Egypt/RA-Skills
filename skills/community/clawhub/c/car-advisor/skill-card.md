## Description:

Car Advisor is a real-time vehicle research and comparison skill for questions about car buying, model specifications, pricing, owner feedback, and market data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deusyu](https://clawhub.ai/user/deusyu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to research China-market vehicles, compare models, check configurations and prices, summarize owner feedback, and produce buying guidance grounded in current web sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Vehicle prices, configurations, sales rankings, and owner feedback can change quickly or differ across sources.

Mitigation: Use live sources for dynamic facts, prefer official pages for pricing, cross-check important claims, and include collection timestamps in answers.

Risk: The skill focuses on Chinese sources and China-market vehicle models, which may bias coverage for users asking about other markets.

Mitigation: State market scope when relevant and verify local-market availability, pricing, and specifications before giving buying guidance.

Risk: The artifact references a plain HTTP APPKEY API example for a paid car data provider.

Mitigation: Use HTTPS where available and avoid exposing API keys or secrets in prompts, logs, URLs, or shared outputs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/deusyu/skills/car-advisor)
- [Data Sources Reference](references/data-sources.md)
- [Comparison Dimensions Matrix](references/compare-dimensions.md)
- [Dongchedi Parameters](https://www.dongchedi.com/auto/params-carIds-x-{series_id})
- [Autohome Configuration](https://www.autohome.com.cn/config/)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown with tables, source notes, timestamps, and concise recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should separate objective vehicle data from subjective owner feedback and cite collection time for dynamic prices or market data.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
