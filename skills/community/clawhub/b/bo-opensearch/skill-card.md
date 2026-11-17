## Description:

BO-OpenSearch helps agents run broad web searches, fetch real pages, rank results by relevance, depth, and timeliness, and return useful source-linked findings while filtering ads and noise.

This skill is ready for commercial/non-commercial use.

## Publisher:

[exochief0125](https://clawhub.ai/user/exochief0125)

### License/Terms of Use:

MIT-0

## Use Case:

External users, students, researchers, and developers use this skill to ask an agent for web search results that are fetched, ranked, filtered, and summarized with source URLs. It is designed for knowledge lookup, current events, technical troubleshooting, product comparison, and how-to research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad automatic web-search activation may send unintended or sensitive user queries to search and fetch tools.

Mitigation: Use explicit invocation such as /bo-opensearch or configure the runtime to require confirmation before searches for sensitive, legal, medical, financial, personal, or proprietary topics.

Risk: Raw search queries and visited-result URLs may be recorded without clear retention or opt-out controls.

Mitigation: Deploy only in environments with acceptable logging controls, retention policies, and user notice for search activity.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/exochief0125/skills/bo-opensearch)
- [README](artifact/README.md)
- [Skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown search-results list with source URLs, relevance ratings, page summaries, and fetch status.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes the original query, ranked results, conflict notes, promotional or paywall labels when identified, and crawl-status counts.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
