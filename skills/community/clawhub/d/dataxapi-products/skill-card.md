## Description:

Searches TikTok or Xiaohongshu for a page of products by keyword, then fetches reviews for up to ten products into a CSV.

This skill is ready for commercial/non-commercial use.

## Publisher:

[data-x-api](https://clawhub.ai/user/data-x-api)

### License/Terms of Use:

MIT-0

## Use Case:

External product researchers can compare product listings and buyer feedback on TikTok or Xiaohongshu. The skill searches one page of products, fetches reviews for up to ten products, and writes the results to CSV.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Product searches and review fetches incur separate charges.

Mitigation: Review the free plan and maximum spend before running, and use a budget-limited API key.

Risk: The exported CSV contains third-party review text and reviewer identifiers.

Mitigation: Treat review text as untrusted data and protect the resulting CSV.

Risk: The external DataXAPI CLI implementation is outside the skill-instructions security review.

Mitigation: Use a reviewed, pinned CLI version.

## Reference(s):

- [DataXAPI Skills](https://dataxapi.com/skills/)
- [DataXAPI Products on ClawHub](https://clawhub.ai/data-x-api/skills/dataxapi-products)

## Skill Output:

**Output Type(s):** [CSV files, Text summaries]

**Output Format:** [CSV product and review rows, with a text cost plan and summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One product-search page and up to ten review pages; each successful call is charged separately, within the announced spending cap.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
