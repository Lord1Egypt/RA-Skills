## Description:

Compare book niches and title positioning using Goodreads catalogs, editions and reviews alongside Apple Books and Audible listings, while preserving coverage and sales limitations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Authors, publishers, and researchers use the skill to compare titles, editions, and sampled reader reception when developing book-positioning hypotheses. It reports gaps in catalog coverage and does not equate ratings or rankings with sales.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Book-research queries and the Crawlora API key are sent to Crawlora; sensitive unpublished material in searches may be disclosed to the service.

Mitigation: Use a service-scoped key and omit private or sensitive unpublished material from search terms unless sharing it with Crawlora is intended.

Risk: Catalog requests can consume credits, especially across many pages or titles.

Mitigation: Set call and page limits that match the requested scope and credit budget.

Risk: Incomplete catalogs and selected reviews can mislead positioning decisions or imply unsupported sales conclusions.

Mitigation: Preserve sample sizes, source dates, and missing coverage; distinguish work-level and edition-level ratings and do not treat ratings or chart ranks as sales.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/crawlora-org/skills/book-market-positioning)
- [Crawlora endpoint reference](reference/endpoints.md)

## Skill Output:

**Output Type(s):** [Analysis, Guidance]

**Output Format:** [Markdown comparable-title matrix, edition ledger, reception evidence, and positioning hypotheses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes source identifiers, observation dates, sample sizes, and coverage limitations.]

## Skill Version(s):

1.0.3 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
