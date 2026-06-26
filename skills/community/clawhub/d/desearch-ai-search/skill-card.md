## Description: <br>
AI-powered search that aggregates and summarizes results from multiple sources including web, X/Twitter, Reddit, Hacker News, YouTube, ArXiv, and Wikipedia. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[okradze](https://clawhub.ai/user/okradze) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, developers, and research workflows use this skill to query Desearch for synthesized answers or curated links across web, social, community, video, academic, and encyclopedia sources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and the API key are sent to the external Desearch service. <br>
Mitigation: Avoid placing passwords, tokens, private documents, confidential business information, or other sensitive content in queries, and use a scoped Desearch API key where possible. <br>
Risk: Use may consume paid quota or balance tied to the Desearch API key. <br>
Mitigation: Monitor account quota or balance and choose result counts and source filters appropriate for the task. <br>
Risk: Aggregated search summaries and curated links can be incomplete, stale, or misleading. <br>
Mitigation: Review cited links and source results before relying on the output for decisions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/okradze/desearch-ai-search) <br>
- [Desearch Homepage](https://desearch.ai) <br>
- [Desearch API Reference](https://desearch.ai/docs/api-reference/post-desearch-ai-search) <br>
- [Desearch Console](https://console.desearch.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, guidance] <br>
**Output Format:** [Plain text summaries, curated links, or pretty-printed JSON from the Desearch API] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DESEARCH_API_KEY and sends search prompts plus selected source filters to the Desearch API.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
