## Description:

AI News Collector guides an agent to collect, cross-check, rank, and summarize current AI news in Chinese with source links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[desmond56](https://clawhub.ai/user/desmond56)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to ask an agent for current AI-sector news. It directs multilingual searches, source cross-checking, deduplication, heat ranking, and Chinese digest output with links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Current-news collection can surface incorrect, duplicated, promotional, or paywalled reporting.

Mitigation: Cross-check high-heat items across multiple sources, merge duplicates, prefer authoritative sources, and label inaccessible subscription material.

Risk: The workflow asks the agent to open public news, community, newsletter, and social-source pages.

Mitigation: Review source links before relying on them and avoid entering credentials or private information into third-party pages.

## Reference(s):

- [Recommended AI news sources](artifact/references/sources.md)
- [ClawHub skill page](https://clawhub.ai/desmond56/skills/ai-news-collector)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown Chinese news digest with ranked items and source links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Ranks 15-25 deduplicated news items by heat and reports search coverage.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
