## Description:

Search academic papers and conduct literature reviews using OpenAlex API (free, no key needed).

This skill is ready for commercial/non-commercial use.

## Publisher:

[feiyang2007](https://clawhub.ai/user/feiyang2007)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to search scholarly works by topic, author, or DOI, inspect citation chains, and generate literature-review drafts with paper metadata and thematic summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated literature reviews may be used as academic or professional deliverables without enough human review.

Mitigation: Review search results, citations, abstracts, and synthesized claims against source papers before relying on the output.

Risk: The skill contacts OpenAlex and Unpaywall, sends a hard-coded contact email in API requests, caches data under /tmp/litreview_cache, and can write reports to a user-provided path.

Mitigation: Use it in environments where those outbound requests, cache behavior, attribution, and file writes are acceptable.

Risk: Markdown reports insert Topanga attribution by default.

Mitigation: Check generated reports for required attribution, disclosure, and branding treatment before distribution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/feiyang2007/skills/academic-research-conflict)
- [OpenAlex API](https://api.openalex.org)
- [Unpaywall API](https://api.unpaywall.org/v2)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, files]

**Output Format:** [Plain text search results, Markdown literature reviews, structured JSON metadata, and optional user-specified output files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can include titles, authors, abstracts, citation counts, DOIs, open access URLs, thematic clusters, and generated review summaries.]

## Skill Version(s):

1.0.0 (source: release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
