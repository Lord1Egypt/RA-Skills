## Description:

Extract real restaurant insights from Dianping reviews: filter noise, detect fake reviews, build personalized dining guides.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to analyze Dianping-oriented restaurant review evidence, identify suspicious feedback patterns, summarize genuine sentiment, rank restaurants for a dining context, and generate dish-level ordering or route guidance.

### Deployment Geography for Use:

Mainland China primarily

## Known Risks and Mitigations:

Risk: Users may assume live Dianping scraping and caching behavior is packaged or already reviewed for real public review data use.

Mitigation: Treat the packaged CLI as local and sample-data based; clarify data collection, caching, rate limiting, and terms-compliance requirements before connecting it to real Dianping data.

Risk: Restaurant recommendations can be misleading when based on sample, stale, insufficient, or suspicious review evidence.

Mitigation: Surface data source, staleness, review count, authenticity index, and warning signals in user-facing guidance before relying on recommendations.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/harrylabsj/skills/dianping-restaurant-guide)
- [Fake Review Detection Signals](references/signals.json)
- [Input Schema](https://openclaw.dev/skills/dianping-restaurant-guide/input.schema.json)
- [Output Schema](https://openclaw.dev/skills/dianping-restaurant-guide/output.schema.json)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, shell commands]

**Output Format:** [Markdown-style prose and CLI text; schemas define JSON objects for authenticity reports, sentiment summaries, ranked results, ordering guides, and routes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Packaged CLI behavior is local and sample-data based; production use with real public review data should clarify data collection, caching, and compliance expectations.]

## Skill Version(s):

1.0.0 (source: frontmatter, skill.json, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
