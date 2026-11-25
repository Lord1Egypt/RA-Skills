## Description:

Retrieves Xiaohongshu (RedNote) keyword search-index history and related keyword metrics from PGY for trend and keyword research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[data-x-api](https://clawhub.ai/user/data-x-api)

### License/Terms of Use:

MIT-0

## Use Case:

Marketers, creators, and analysts use this skill to review a keyword’s roughly three-month daily Xiaohongshu search-index history and find related terms for content planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI install is unpinned, so a later package change could affect the host.

Mitigation: Install a reviewed version of the dataxapi package, consider pinning its version, and assess trust in the DataXAPI service before use.

## Reference(s):

- [DataXAPI homepage](https://dataxapi.com)
- [Xiaohongshu PGY keyword history API](https://dataxapi.com/apis/xiaohongshu/pgy/keywords/history/)
- [Xiaohongshu PGY related keywords API](https://dataxapi.com/apis/xiaohongshu/pgy/keywords/related/)
- [DataXAPI agent setup](https://dataxapi.com/agents.md)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Guidance]

**Output Format:** [Structured keyword metrics with concise trend and related-term guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Daily history spans about three months; the platform sets the period. Search index values are platform indices, not raw search counts.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
