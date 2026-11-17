## Description:

Constructs precise, multi-query Google searches with advanced operators, source filtering, relevance ranking, and credibility annotations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[calvinxhk](https://clawhub.ai/user/calvinxhk)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use this skill to turn broad information-retrieval requests into targeted Google searches, then rank and summarize credible, current sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad activation phrases such as "look up" may route routine information requests through this search workflow more often than intended.

Mitigation: Review activation behavior during deployment and ask a clarifying question when a request is ambiguous or does not require web search.

Risk: Search-result quality depends on source credibility, freshness, and deduplication checks being applied consistently.

Mitigation: Keep the credibility, date-context, and multi-query verification steps in the workflow active for time-sensitive or high-impact topics.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/calvinxhk/skills/botlearn-google-search)
- [Publisher profile](https://clawhub.ai/user/calvinxhk)
- [README](artifact/README.md)
- [Skill definition](artifact/skill.md)
- [Search strategy](artifact/strategies/main.md)
- [Google Search operator syntax](artifact/knowledge/domain.md)
- [Search best practices](artifact/knowledge/best-practices.md)
- [Search anti-patterns](artifact/knowledge/anti-patterns.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown with ranked source summaries, credibility annotations, date context, and optional synthesis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include advanced Google query strings, source-quality tiers, relevance notes, and deduplicated result lists.]

## Skill Version(s):

1.0.0 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
