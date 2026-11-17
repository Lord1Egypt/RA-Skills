## Description:

Aggregates and deduplicates RSS and Atom feeds, ranks and clusters articles by importance, and generates concise daily digests with source attribution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[calvinxhk](https://clawhub.ai/user/calvinxhk)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to manage RSS subscriptions, discover and parse feeds, reduce duplicate coverage, prioritize important articles, and produce structured digests or feed health reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can direct broad outbound fetching of third-party feed and article URLs.

Mitigation: Restrict accepted URLs to http and https, block localhost, private network, and metadata-service addresses, validate redirects and discovered feed URLs, and limit response size, redirects, and request duration.

Risk: Feed redirects can cause stored feed URLs to change silently.

Mitigation: Require user confirmation before permanently changing stored feed URLs, and log moved, gone, or unhealthy feeds in the feed health report.

Risk: Deduplication, clustering, and importance scoring can misclassify articles or over-prioritize weak sources.

Mitigation: Keep source attribution visible, explain scoring and clustering signals for important items, and allow user review or correction of source authority and topic preferences.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/calvinxhk/skills/botlearn-rss-manager)
- [README](artifact/README.md)
- [Skill definition](artifact/skill.md)
- [RSS Manager Strategy](artifact/strategies/main.md)
- [Feed Formats, Parsing, and Content Extraction](artifact/knowledge/domain.md)
- [RSS Manager Best Practices](artifact/knowledge/best-practices.md)
- [RSS Manager Anti-Patterns](artifact/knowledge/anti-patterns.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Configuration]

**Output Format:** [Markdown or structured text digests and feed-management reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes source attribution, importance scores, topic clusters, trend indicators, and feed health details when available.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
