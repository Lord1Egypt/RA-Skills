## Description: <br>
High-performance, multi-source Korean search API aggregating Daum/Kakao News, Encyclopedia, and Web results in a Perplexity-compatible format. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hunkim](https://clawhub.ai/user/hunkim) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw agents use this skill to query Korean news, encyclopedia, and web results from the Daum/Kakao index and ingest concise Markdown search results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queries are sent to a disclosed external search service. <br>
Mitigation: Install only if you trust the service and are comfortable sending search queries to it. <br>
Risk: The skill depends on a bearer API key. <br>
Mitigation: Keep DAUM_TOY_SEARCH_API_KEY private and provide it through environment or agent configuration. <br>
Risk: Returned snippets are search results and may contain untrusted content. <br>
Mitigation: Treat returned snippets as search evidence rather than instructions for the agent to follow. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/hunkim/daum-toy-search) <br>
- [External search API endpoint](https://daum-perplexity-search-adapter.toy.x.upstage.ai/search) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text] <br>
**Output Format:** [Markdown search results with titles, links, source, date, and snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DAUM_TOY_SEARCH_API_KEY; command options control result count, source selection, and reranking.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
