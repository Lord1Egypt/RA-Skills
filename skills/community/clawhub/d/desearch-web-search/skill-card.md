## Description: <br>
Search the web and get real-time SERP-style results with titles, URLs, and snippets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[okradze](https://clawhub.ai/user/okradze) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to run current web searches through Desearch and retrieve SERP-style titles, links, and snippets for general research workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and API credentials are handled by a third-party Desearch service. <br>
Mitigation: Provide the API key through DESEARCH_API_KEY and avoid using sensitive private information in search queries. <br>
Risk: Search results may reflect external web content that is inaccurate, stale, or unsafe to act on directly. <br>
Mitigation: Review returned links and snippets before relying on them in downstream decisions or generated work. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/okradze/desearch-web-search) <br>
- [Desearch Homepage](https://desearch.ai) <br>
- [Desearch Web Search API Reference](https://desearch.ai/docs/api-reference/get-web) <br>
- [Desearch Console](https://console.desearch.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration] <br>
**Output Format:** [JSON search results and plain-text error messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DESEARCH_API_KEY; sends search queries and pagination offsets to Desearch; returns up to 10 results per page.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
