## Description:

Search Douyin (抖音) content by natural language keyword, including video search, trending topics, and video detail extraction using web search and page scraping without an API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Content researchers, social media managers, and external users use this skill to discover Douyin videos, trending topics, and basic metadata from public Douyin URLs through natural language requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may use web search and fetch public Douyin pages when asked for Douyin discovery or video details.

Mitigation: Use it for public content discovery only and review outbound retrieval policies before deployment.

Risk: Broad Douyin search requests can activate the skill and return incomplete or stale indexed results.

Mitigation: Review the extracted keyword and verify important findings directly on Douyin when freshness or completeness matters.

Risk: Douyin CAPTCHA, authentication, or access controls may prevent detailed page metadata extraction.

Mitigation: Fallback to search result metadata and clearly label limited results instead of presenting them as comprehensive.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/terrycarter1985/skills/douyin-quick-search)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown search summaries with keywords, result counts, titles, descriptions, and links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may be partial when Douyin pages are blocked or search indexes lag live content.]

## Skill Version(s):

1.0.0 (source: frontmatter, skill manifest, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
