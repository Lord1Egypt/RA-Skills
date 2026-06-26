## Description: <br>
Constructs precise, multi-query Google searches using advanced operators, result filtering, source credibility checks, and relevance ranking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[calvinxhk](https://clawhub.ai/user/calvinxhk) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to turn web-search requests into targeted Google queries, rank credible sources, deduplicate results, and present source-aware findings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad web-search trigger phrases may activate the skill more often than intended. <br>
Mitigation: Review and narrow activation phrases if tighter control is needed in the target agent environment. <br>
Risk: Search requests may expose passwords, private tokens, confidential business details, or highly sensitive personal information to web-search tooling. <br>
Mitigation: Avoid including secrets, credentials, confidential business data, or highly sensitive personal information in search queries. <br>
Risk: Search results can be outdated, duplicated, low quality, or misleading if source quality and date context are not checked. <br>
Mitigation: Apply the skill's source credibility, freshness, deduplication, and primary-source preference checks before presenting results. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/calvinxhk/botlearn-google-search) <br>
- [Publisher profile](https://clawhub.ai/user/calvinxhk) <br>
- [README](README.md) <br>
- [Skill definition](skill.md) <br>
- [Google Search Strategy](strategies/main.md) <br>
- [Google Search Best Practices](knowledge/best-practices.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown with ranked results, source credibility annotations, summaries, relevance notes, and synthesis when multiple sub-queries are used] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include optimized Google query strings, deduplicated result lists, publication-date context, and source-quality notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill.md frontmatter; package metadata lists 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
