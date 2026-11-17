## Description:

Aggregates configured Danish RSS feeds into category-based unified RSS feeds with deduplication and source ranking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[broedkrummen](https://clawhub.ai/user/broedkrummen)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to configure and run a Danish RSS aggregation workflow that emits category feeds for readers, dashboards, or publishing pipelines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Network fetching may be unsafe because the shipped artifact includes TLS-bypass code and an HTTP feed.

Mitigation: Remove TLS-bypass behavior, restrict feeds.json to trusted HTTPS domains, and run the aggregator in a restricted environment.

Risk: Scheduled refresh can repeatedly fetch untrusted external content if the cron job is enabled before review.

Mitigation: Do not add the cron job until dependencies are pinned and the feed list, runtime behavior, and generated outputs have been reviewed.

Risk: Release claims may overstate what the shipped code does.

Mitigation: Validate the scripts and generated RSS outputs against expected category coverage before relying on the release claims.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/broedkrummen/skills/danish-news-aggregator)
- [Comprehensive Danish RSS Feeds](artifact/comprehensive_feeds.md)
- [Feed configuration](artifact/feeds.json)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with command snippets, JSON configuration, Python code, and RSS XML files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces category RSS XML feeds from configured external RSS sources; network access is required at runtime.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
