# DomiDocs profile

## Company
DomiDocs

## Sitemap
- `https://domidocs.com/sitemap_index.xml`

## Primary business topics for v1
These are valid starting topics for this skill:
- homeowner enablement platform
- documenting for disaster
- homelock
- truevalue index
- proprtax

## Dense cluster guardrails

Treat `homelock` as a dense protected topic cluster.

For `homelock`:
- default to reviewing existing URL coverage before any keyword expansion
- treat adjacent phrasing as likely architecture overlap, not automatic new opportunities
- prefer `expand-existing` when a current page can absorb the query
- prefer `no-go` when the distinction is weak or mostly rephrased
- choose `new-url` only when there is one clearly separate unanswered question with materially different intent

## How to use this file
For DomiDocs runs, start from one of the topics above or a close business-topic variant.
For future reuse with another company, replace or supplement this file with that company's:
- brand / company name
- sitemap url
- allowed business topics / product lines / service areas
- any topical guardrails

Keep the rest of the skill unchanged whenever possible.
