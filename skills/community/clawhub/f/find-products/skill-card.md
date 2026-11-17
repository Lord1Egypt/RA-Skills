## Description:

Search and discover trending products from ProductHunt with structured analysis data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiazhefengzhi](https://clawhub.ai/user/xiazhefengzhi)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to find, compare, and summarize trending products, apps, and alternatives from ProductHunt-related search results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User product-search text may become unsafe if substituted directly into the documented curl command.

Mitigation: URL-encode query parameters or use a structured HTTP client before executing requests.

Risk: Product-search queries are sent to trend-hunt.com.

Mitigation: Avoid sending sensitive or private search terms unless the user accepts that external service interaction.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiazhefengzhi/skills/find-products)
- [Trend Hunt search API](https://trend-hunt.com/api/search?q=QUERY&locale=LOCALE&limit=LIMIT&category=CATEGORY)
- [ProductHunt post URL format](https://www.producthunt.com/posts/product-slug)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and product summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include product names, categories, upvote counts, hype and utility scores, review summaries, ProductHunt links, and website links.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
