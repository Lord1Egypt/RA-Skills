## Description:

Researches books, authors, and audiobooks via the Crawlora API — Goodreads (books, authors, reviews, lists, quotes), Apple Books (books, audiobooks, series, reviews, charts), and Audible (audiobook catalog search, product detail, narrators/series, reviews, charts, editorial lists) — returning clean JSON. Use when the user wants a book's ratings/reviews, an author's bibliography, curated reading lists, or audiobook details and charts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Readers and research agents use this skill to find book and author details, reviews, curated reading lists, and audiobook information across Goodreads, Apple Books, and Audible.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crawlora receives research queries and the API key, and requests consume service credits. The helper briefly stores the key in a restricted temporary file; server-side data handling was not verified.

Mitigation: Keep confidential information out of searches, protect the API key, and review Crawlora's data handling before sending sensitive queries.

## Reference(s):

- [Endpoint reference](reference/endpoints.md)
- [Crawlora](https://crawlora.net)

## Skill Output:

**Output Type(s):** [JSON]

**Output Format:** [Normalized JSON catalog results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Public catalog data; review and list results may be paginated.]

## Skill Version(s):

1.0.21 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
