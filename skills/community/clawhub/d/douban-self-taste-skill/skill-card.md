## Description:

Collect, refresh, normalize, and analyze the user's own Douban history for taste analysis and recommendation reasoning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xeric7](https://clawhub.ai/user/xeric7)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to work with a user's own Douban shelves, ratings, tags, comments, and reviews. It helps decide whether local cache is fresh enough, refresh data from authenticated pages when appropriate, and produce category-aware taste analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a Douban session cookie to refresh logged-in personal account data.

Mitigation: Use a dedicated Douban-only cookie export, keep the cookie file private, and delete it when refresh is complete or no longer needed.

Risk: The skill stores ratings, comments, shelves, and analysis files locally.

Mitigation: Keep .local/douban-self-taste private, do not commit or sync it, and remove cached personal history when it is no longer needed.

Risk: Cached data can become stale or authentication can fail.

Mitigation: Respect the 7-day freshness check, verify crawl success, and ask for fresh cookies instead of analyzing failed login redirects.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xeric7/skills/douban-self-taste-skill)
- [Analysis rubric for self taste](artifact/references/analysis-rubric.md)
- [Data sources and refresh policy](artifact/references/data-sources.md)
- [Output schema](artifact/references/output-schema.md)
- [Storage layout](artifact/references/storage-layout.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON, guidance]

**Output Format:** [Markdown guidance, shell commands, and JSON cache or profile files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local .local/douban-self-taste paths; cache freshness is based on fetched_at and a 7-day staleness rule.]

## Skill Version(s):

0.1.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
