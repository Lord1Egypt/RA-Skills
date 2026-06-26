## Description: <br>
Admapix Repo is an ad intelligence and app analytics assistant for searching ad creatives, analyzing apps, exploring rankings, tracking download and revenue estimates, and summarizing market insights via SkillBoss/AdMapix APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alvisdunlop](https://clawhub.ai/user/alvisdunlop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, marketers, app developers, and analysts use this skill to query ad creative, app ranking, download and revenue estimate, distribution, and market intelligence data in English or Chinese. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends ad-search keywords, app names, and analysis requests to the AdMapix/SkillBoss service using a configured API key. <br>
Mitigation: Use a dedicated provider API key, avoid confidential queries, and rotate or revoke the key if exposure is suspected. <br>
Risk: Generated H5 result links may expose analysis context or query results when shared. <br>
Mitigation: Share generated links only with intended recipients and avoid using sensitive query terms. <br>
Risk: Download and revenue figures are third-party estimates rather than official data. <br>
Mitigation: Label these figures as estimates and avoid treating them as audited business metrics. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/alvisdunlop/alvis-admapix) <br>
- [SkillBoss](https://www.skillboss.co) <br>
- [Creative Search API](references/api-creative.md) <br>
- [Product & Company API](references/api-product.md) <br>
- [Ranking API](references/api-ranking.md) <br>
- [Download & Revenue API](references/api-download-revenue.md) <br>
- [App Distribution API](references/api-distribution.md) <br>
- [Market Analysis API](references/api-market.md) <br>
- [Parameter Mapping Reference](references/param-mappings.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown reports, tables, summaries, H5 result links, and shell command snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Bilingual English/Chinese output; download and revenue figures are presented as third-party estimates.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
