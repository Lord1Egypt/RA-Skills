## Description:

Search Amazon KDP books, retrieve a single book's BSR history, and explore Amazon book categories through BeyondBSR's API for market and niche research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ramius88](https://clawhub.ai/user/ramius88)

### License/Terms of Use:

MIT-0

## Use Case:

Authors, publishers, and market researchers use this skill to search and compare Amazon KDP books, review a book's BSR history, and explore book categories for niche and competitor research.

### Deployment Geography for Use:

United States (Amazon.com marketplace data only)

## Known Risks and Mitigations:

Risk: Search terms, filters, and book identifiers are sent to BeyondBSR, whose data-retention practices have not been verified.

Mitigation: Avoid confidential queries and keep BOOKSEARCH_API_KEY in the configured environment variable; do not expose it in output.

## Reference(s):

- [BeyondBSR Book Search API](https://api.beyondbsr.com/api/v1/books/search)
- [BeyondBSR category taxonomy API](https://api.beyondbsr.com/api/v1/categories?domainId=1&depth=2)
- [ClawHub skill release](https://clawhub.ai/ramius88/skills/booksearch-api)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Markdown]

**Output Format:** [JSON API results and concise Markdown research summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BOOKSEARCH_API_KEY; book data is currently limited to the US marketplace.]

## Skill Version(s):

1.0.10 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
