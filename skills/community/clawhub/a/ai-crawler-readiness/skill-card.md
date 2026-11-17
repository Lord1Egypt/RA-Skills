## Description:

Benchmark stored llms.txt and robots.txt signals from Crawlora's top-1M AI-readiness dataset. Use for cohort adoption or indexed-domain snapshots; domains outside the dataset remain unknown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to compare llms.txt adoption and crawler-policy signals across Crawlora's stored top-1M dataset, or review a single indexed domain's stored snapshot. It returns source-attributed counts or site findings while keeping unknown probe states separate from established presence or absence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queried domains and filters are sent to Crawlora when using its API.

Mitigation: Avoid sending sensitive domain queries and review filters before running a search.

Risk: Searches consume API credits, including a minimum charge for empty results.

Mitigation: Keep search pages bounded and check the documented per-record billing before broad queries.

Risk: Stored probe results can be mistaken for current live-site behavior.

Mitigation: Label findings as snapshots and include run and probe dates; treat domains outside the dataset or with unknown states as unknown.

## Reference(s):

- [Crawlora endpoint reference](reference/endpoints.md)
- [Google common crawlers documentation](https://developers.google.com/crawling/docs/crawlers-fetchers/google-common-crawlers)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown prose and tables with source-attributed site rows or cohort counts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes filters, snapshot and probe dates, denominators, and unknown-state counts when reporting results.]

## Skill Version(s):

1.0.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
