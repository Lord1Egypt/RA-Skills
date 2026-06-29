## Description: <br>
Provides an MCP-based 12306 ticket search service that lets an agent query train ticket availability, station codes, transfer options, route stops, and Shanghai-time dates through the XiaoBenYang API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alinklab](https://clawhub.ai/user/alinklab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users can use this skill to let an agent search China Railway 12306 ticket availability and station information through a third-party API. It supports date resolution, station-code lookup, direct ticket search, transfer ticket search, and train route stop lookup when the required API key is configured. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The required third-party API key is stored in a local .env file. <br>
Mitigation: Treat the key like a password, avoid shared or synced folders, and delete or rotate the key when it is no longer needed. <br>
Risk: Ticket search results depend on a third-party API service and may fail or become stale if the service is unavailable or returns errors. <br>
Mitigation: Review the returned status and message before acting on results, and verify important ticket information against official booking channels before purchase. <br>


## Reference(s): <br>
- [XiaoBenYang API key site](https://xiaobenyang.com) <br>
- [XiaoBenYang MCP API endpoint](https://mcp.xiaobenyang.com) <br>
- [ClawHub skill page](https://clawhub.ai/alinklab/12306-ticket-purchase-search) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Text, JSON, Configuration guidance] <br>
**Output Format:** [Markdown summaries of API responses, with raw JSON available from tool results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an XBY_APIKEY value, which the skill can save to a local .env file.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
