## Description:

Quota-aware multi-provider web search for OpenClaw. Supports 12 search providers with automatic failover, task-level deep search (@dual/@deep), real quota checks, and managed result storage under memory/.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vulcanusalex](https://clawhub.ai/user/vulcanusalex)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to run provider-diverse web searches, aggregate task-level research queries, monitor quota and provider health, and persist search results in managed memory storage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries and returned results are saved locally under memory/.

Mitigation: Avoid sensitive search queries and clean stored reports or cache when retained results are no longer needed.

Risk: Optional providers use API keys for external search services.

Mitigation: Use dedicated, restricted API keys and rotate or remove them according to the provider's operational policy.

Risk: The optional SearXNG setup path can use a Docker image.

Mitigation: Pin or review the SearXNG Docker image before using that optional setup path.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/vulcanusalex/skills/free-search-aggregator)
- [Mojeek Search API](https://www.mojeek.com/services/search/api/)
- [Exa](https://exa.ai/)
- [Google Custom Search JSON API](https://developers.google.com/custom-search/v1/introduction)
- [Programmable Search Engine](https://programmablesearchengine.google.com/)
- [Baidu Cloud](https://cloud.baidu.com/)
- [SearXNG documentation](https://searxng.github.io/searxng/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [JSON search and quota payloads, Markdown reports, and CLI text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results, indexes, reports, provider health, and discovery records may be persisted under memory/.]

## Skill Version(s):

1.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
