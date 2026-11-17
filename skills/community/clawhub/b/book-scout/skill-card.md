## Description:

Expert book recommendation engine that uses web search to find high-quality books (Douban ≥7.5 or Goodreads ≥3.8) by topic, with deduplication and comprehensive scoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kedoupi](https://clawhub.ai/user/kedoupi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to find a high-quality book for a topic, avoid previously used titles, and receive the top scored recommendation with rating, review count, summary, and reasoning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Book topics and candidate titles may be sent to third-party search and book-rating services during recommendation lookup.

Mitigation: Avoid entering sensitive or confidential topics, and review whether third-party search exposure is acceptable before using the skill.

Risk: The workflow is strongly oriented toward Chinese-language sources and Douban, with Goodreads as a fallback, so results may be less balanced for some topics or regions.

Mitigation: Review the returned recommendation and broaden or rephrase the topic when coverage appears narrow.

Risk: When exact ratings are unavailable, the workflow may use conservative estimated ratings based on search context.

Mitigation: Treat estimated ratings as lower-confidence and verify important recommendations against primary book-rating pages.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kedoupi/skills/book-scout)
- [README](README.md)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [JSON object or JSON error object with concise explanatory text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns the highest-scoring book after web search, deduplication, rating lookup, and deterministic local scoring.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
