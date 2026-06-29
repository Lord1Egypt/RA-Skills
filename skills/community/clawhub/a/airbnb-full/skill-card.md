## Description: <br>
Complete Airbnb stay data toolkit via StayingAPI.com for id, URL, and address lookup, sub-resource retrieval, listing search, async batch jobs, job polling, webhook management, account usage, and hosted MCP tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nikhonit](https://clawhub.ai/user/nikhonit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill when a user explicitly requests Airbnb listing data, listing search, reviews, availability, pricing, host details, account usage, or bulk stay-data workflows through StayingAPI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Calls may consume StayingAPI credits. <br>
Mitigation: Use the skill only for explicit Airbnb stay-data requests, confirm ambiguous intent before calling tools, and set search or batch limits that match the user's need. <br>
Risk: Listing URLs, addresses, search criteria, and account requests are sent to StayingAPI. <br>
Mitigation: Review the requested data before use and avoid sending information the user has not asked to look up. <br>
Risk: Webhook subscriptions can cause future job or cache events to be delivered to a provided URL. <br>
Mitigation: Create webhooks only for trusted destination URLs and review webhook events before enabling them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nikhonit/skills/airbnb-full) <br>
- [StayingAPI homepage](https://stayingapi.com) <br>
- [StayingAPI OpenAPI spec](https://stayingapi.com/openapi.json) <br>
- [StayingAPI MCP server](https://api.stayingapi.com/mcp) <br>
- [StayingAPI MCP server card](https://stayingapi.com/.well-known/mcp/server-card.json) <br>
- [StayingAPI quickstart](https://stayingapi.com/quickstart/) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Text, Configuration, Guidance] <br>
**Output Format:** [Python dict API responses, including JSON-style data or error dictionaries; job results may be requested as JSON, CSV, or NDJSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires STAYINGAPI_KEY and may make outbound requests to StayingAPI.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
