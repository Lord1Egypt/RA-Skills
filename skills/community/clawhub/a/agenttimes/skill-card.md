## Description: <br>
Live context layer for AI agents. One /ask endpoint for news, weather, crypto prices, and alerts. 228K+ articles, 3,576 feeds, 14 categories. Enriched with sentiment, entities, and credibility. Free to use, no API key needed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[angpenghian](https://clawhub.ai/user/angpenghian) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI agents use Agent Times to query current news, weather, crypto prices, trending stories, and topic alerts through copy-paste curl workflows and JSON API responses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Webhook subscriptions send query interests and matching article data to the provided webhook URL. <br>
Mitigation: Use only trusted HTTPS webhook endpoints, understand what data will be delivered, and save the returned unsubscribe secret. <br>
Risk: External API responses can vary by endpoint and source field. <br>
Mitigation: Parse the JSON response shape by checking the source field before acting on returned data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/angpenghian/agenttimes) <br>
- [Agent Times homepage](https://agenttimes.live) <br>
- [Agent Times documentation](https://agenttimes.live/info) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API calls, Guidance] <br>
**Output Format:** [Markdown with inline bash examples and JSON response descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Most documented endpoints require no API key; /search uses x402 micropayment and /subscribe sends matching article data to the user-provided webhook.] <br>

## Skill Version(s): <br>
8.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
