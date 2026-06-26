## Description: <br>
Provides broad web search for agent conversations by searching and fetching web pages, ranking results by relevance, depth, and freshness, filtering noise, and returning useful sourced summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[exochief0125](https://clawhub.ai/user/exochief0125) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, students, researchers, developers, and general agent users use this skill to gather current web sources for academic, news, technical, product-comparison, and how-to questions. It is intended to return ranked Markdown search results with source URLs, short summaries, and fetch status details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can auto-trigger on broad information requests and may send sensitive queries or fetched URLs to external search and fetch tools. <br>
Mitigation: Use it only for queries appropriate for external web search, avoid credential, personal, legal, medical, or confidential business searches, and review search terms before allowing the skill to run. <br>
Risk: The artifact describes logging original queries, fetched URLs, result scores, decisions, and timestamps. <br>
Mitigation: Limit use to contexts where query and URL logging is acceptable, and avoid including sensitive details in searches. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/exochief0125/bo-opensearch) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [README.md](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown search results with source URLs, ranked summaries, and fetch status counts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include relevance ratings, notes for login or paywall pages, promotion labels, and conflict notes across sources.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
