## Description: <br>
Provides free web, image, news search, and autocomplete suggestions through the Claw Search API without requiring an API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuanchao193](https://clawhub.ai/user/yuanchao193) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to add web, image, news, and autocomplete search to OpenClaw agents without managing a search API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms are sent to an external service and may be routed through its DuckDuckGo fallback. <br>
Mitigation: Do not use the skill for secrets, credentials, personal data, confidential project names, regulated information, or queries whose disclosure would be unacceptable. <br>
Risk: The external search service may enforce rate limits or become unavailable. <br>
Mitigation: Handle failed requests and rate-limit responses in the calling agent before relying on search results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yuanchao193/claw-search-free) <br>
- [Claw Search API search endpoint](https://www.claw-search.com/api/search) <br>
- [Claw Search API image endpoint](https://www.claw-search.com/api/images) <br>
- [Claw Search API news endpoint](https://www.claw-search.com/api/news) <br>
- [Claw Search API suggestions endpoint](https://www.claw-search.com/api/suggest) <br>


## Skill Output: <br>
**Output Type(s):** [code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JavaScript examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Queries are sent to the Claw Search service and may use its DuckDuckGo fallback.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
