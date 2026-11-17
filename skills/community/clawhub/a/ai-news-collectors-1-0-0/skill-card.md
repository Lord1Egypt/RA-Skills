## Description:

Aggregates current AI news across newsletters, community forums, product launches, funding, research, and policy, then returns a Chinese heat-ranked digest with source links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kkblock](https://clawhub.ai/user/kkblock)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to monitor AI-industry developments and receive a concise Chinese digest of 15-25 current items ranked by observed heat. The skill is intended for news discovery across public sources, community discussions, product launches, funding events, research, and policy updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill performs multiple web searches and fetches public news sources, so results may include stale, incomplete, paywalled, or source-biased information.

Mitigation: Review the cited source links for important claims and rerun searches across the required dimensions when coverage appears thin.

Risk: The default output language is Chinese, which may not match every user's preference.

Mitigation: Ask explicitly for another output language when needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kkblock/skills/ai-news-collectors-1-0-0)
- [AI news source recommendations](references/sources.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown Chinese news digest with ranked sections and source links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Typically returns 15-25 deduplicated AI news items, grouped by heat level, with collection count, search count, covered dimensions, and update time.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
