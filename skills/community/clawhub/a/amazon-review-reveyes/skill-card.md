## Description:

Fetches Amazon product reviews through the Reveyes API across 20 marketplaces and returns review data, star distributions, and critical review summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhuojiuya](https://clawhub.ai/user/zhuojiuya)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to fetch Amazon reviews for a supplied ASIN, compare review sentiment across marketplaces, inspect critical reviews, and export review data for product or competitor analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends ASINs, marketplace choices, and review-fetch requests to the third-party Reveyes service.

Mitigation: Use the skill only where sending those requests to Reveyes is acceptable for the user's workflow and data handling requirements.

Risk: The skill requires a Reveyes API key and consumes Reveyes API credits.

Mitigation: Store REVEYES_API_KEY in a protected secret store or tightly permissioned configuration and monitor page counts and credit usage.

Risk: The skill depends on the external Reveyes Python SDK and service availability.

Mitigation: Pin the Reveyes SDK version in controlled environments and review timeout or error responses before relying on fetched results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhuojiuya/skills/amazon-review-reveyes)
- [Reveyes official site](https://www.reveyes.cn)
- [Reveyes Python SDK on PyPI](https://pypi.org/project/reveyes/)
- [Repository listed by artifact metadata](https://github.com/zhuojiuya/Amazon-Review)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [Markdown-style review summary with structured JSON from the helper script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes ASIN, marketplace, total review count, average rating, rating distribution, top critical reviews, task ID, and credits used.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, clawhub.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
