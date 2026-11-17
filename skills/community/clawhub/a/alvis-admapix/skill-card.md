## Description:

AdMapix is an ad intelligence and app analytics assistant for searching ad creatives, analyzing apps, viewing rankings, tracking download and revenue estimates, and generating market insights through the AdMapix/SkillBoss API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alvisdunlop](https://clawhub.ai/user/alvisdunlop)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, marketers, and app growth teams use this skill to query ad creative libraries, app metadata, rankings, download and revenue estimates, advertising distribution, and market-level competitive intelligence from natural-language prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Ad-analysis queries, app names, filters, and the configured API key are sent to the AdMapix/SkillBoss service.

Mitigation: Install only when this data sharing is acceptable, avoid personal identifiers or confidential campaign names in prompts, and keep the API key in the configured environment variable.

Risk: Download and revenue figures are third-party estimates and may be mistaken for official app performance data.

Mitigation: Clearly label download and revenue outputs as third-party estimates whenever presenting or using them.

Risk: Unpinned installation in controlled environments can make provenance and repeatability harder to verify.

Mitigation: Use a pinned or otherwise verified install command for controlled deployments.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/alvisdunlop/skills/alvis-admapix)
- [AdMapix website](https://www.admapix.com)
- [SkillBoss website](https://www.skillboss.co)
- [Creative Search API](artifact/references/api-creative.md)
- [Product & Company API](artifact/references/api-product.md)
- [Ranking API](artifact/references/api-ranking.md)
- [Download & Revenue API](artifact/references/api-download-revenue.md)
- [App Distribution API](artifact/references/api-distribution.md)
- [Market Analysis API](artifact/references/api-market.md)
- [Parameter Mapping Reference](artifact/references/param-mappings.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries, tables, structured reports, H5 result links, and inline shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses should match the user's language and label download or revenue figures as third-party estimates.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
