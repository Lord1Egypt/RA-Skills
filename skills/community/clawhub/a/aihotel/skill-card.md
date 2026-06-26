## Description: <br>
A Skill for searching hotels and querying prices via AIGoHotel MCP (searchHotels / getHotelDetail / getHotelSearchTags). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qiao101660](https://clawhub.ai/user/qiao101660) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and travel-assistant agents use this skill to search hotels by destination, dates, budget, ratings, guests, and tags, then summarize live room-rate details and cancellation-policy information returned by the AIGoHotel MCP service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The packaged MCP configuration includes a bearer token for the remote AIGoHotel service, and the security evidence says it should be treated as an exposed shared credential. <br>
Mitigation: Replace the packaged token with a scoped, revocable authentication mechanism before deployment and avoid treating the bundled token as private or account-specific. <br>
Risk: Hotel prices, availability, booking links, and cancellation policies are real-time travel data that can change after the tool call. <br>
Mitigation: Present returned prices and policies as current at response time, do not fabricate missing values, and direct users to verify final terms before booking. <br>


## Reference(s): <br>
- [AI Go Hotel ClawHub listing](https://clawhub.ai/qiao101660/aihotel) <br>
- [README_EN.md](artifact/README_EN.md) <br>
- [AIGoHotel API key application](https://mcp.agentichotel.cn/apply) <br>
- [Model Context Protocol](https://modelcontextprotocol.io/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, configuration, guidance] <br>
**Output Format:** [Markdown summaries with structured MCP request and response data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Hotel prices, availability, booking links, and cancellation policies are live service results and may change.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
