## Description:

AI News Collector gathers AI news across product launches, research, industry activity, funding, open source projects, policy, and community trends, then ranks items by heat and returns Chinese summaries with source links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alvisdunlop](https://clawhub.ai/user/alvisdunlop)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, analysts, and other AI watchers use this skill to request current Chinese-language AI news roundups. It guides an agent through multi-dimensional public web search, source cross-checking, deduplication, and heat-based ranking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: News search results may include outdated, duplicated, paywalled, or weakly sourced claims.

Mitigation: Cross-check notable items against multiple sources, merge duplicate coverage, keep source links, and label inaccessible paid sources as subscription-only.

Risk: The workflow performs broad public web browsing across media, newsletters, forums, and community sites.

Mitigation: Use public sources only and review linked evidence before relying on the roundup for business or policy decisions.

## Reference(s):

- [AI News Source Recommendations](artifact/references/sources.md)
- [ClawHub Skill Page](https://clawhub.ai/alvisdunlop/skills/alv-ai-news-collector)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Chinese Markdown news roundup with source links and heat-ranked sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Typically 15-25 deduplicated AI news items, grouped by heat level with search count, covered dimensions, and update time.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
