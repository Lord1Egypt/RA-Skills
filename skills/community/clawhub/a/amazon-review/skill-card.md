## Description:

Fetches Amazon product reviews through the Reveyes API across 20 marketplaces, returning review data, star distribution statistics, and critical review summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhuojiuya](https://clawhub.ai/user/zhuojiuya)

### License/Terms of Use:

MIT-0

## Use Case:

External users, sellers, and commerce analysts use this skill to fetch Amazon review data for an ASIN, compare marketplace sentiment, inspect star distributions, and summarize critical feedback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Amazon ASINs, marketplace selections, page counts, and star filters are sent to Reveyes for review retrieval.

Mitigation: Use the skill only when sharing those review-query parameters with Reveyes is acceptable.

Risk: The Reveyes API key can consume account credits when review pages are fetched.

Mitigation: Use a dedicated revocable key, monitor credit usage, and limit requested page counts to the analysis need.

Risk: The helper depends on the external reveyes Python package.

Mitigation: Pin or review the reveyes dependency in controlled environments before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhuojiuya/skills/amazon-review)
- [Reveyes official site](https://www.reveyes.cn)
- [Reveyes Python SDK on PyPI](https://pypi.org/project/reveyes/)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration guidance]

**Output Format:** [Markdown response with JSON helper output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires REVEYES_API_KEY and sends Amazon ASIN, marketplace, page count, and star-filter parameters to Reveyes.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
