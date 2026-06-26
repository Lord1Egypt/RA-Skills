## Description: <br>
Finds eSIM plans for travel by searching plans by country, filtering by data and duration, ranking by value, checking device compatibility, and surfacing deals through a remote HTTP MCP endpoint. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vladkomudrich](https://clawhub.ai/user/vladkomudrich) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travelers and travel-support agents use this skill to compare eSIM data plans by destination, trip length, data need, device compatibility, price, and active deals. Developers can also use it to configure a remote HTTP MCP connection for eSIM search tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Trip details, data needs, country searches, and device model queries may be sent to the remote eSIM Agent service. <br>
Mitigation: Tell users what query details are being sent and avoid adding unrelated personal information to requests. <br>
Risk: Default purchase links are tracked affiliate redirects. <br>
Mitigation: Disclose the redirect behavior and provide the raw partner affiliate URL when the user asks for a direct partner link or wants to avoid the redirect. <br>
Risk: Plan, price, deal, and compatibility results depend on the remote service and partner data. <br>
Mitigation: Present results as current service data, preserve provider names and prices, and direct users to verify terms before purchase. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vladkomudrich/esimagent) <br>
- [eSIM Agent homepage](https://esimagent.vdigital.app/mcp) <br>
- [Remote HTTP MCP endpoint](https://esimagent.vdigital.app/api/mcp/mcp) <br>
- [MCP auto-discovery metadata](https://esimagent.vdigital.app/.well-known/mcp.json) <br>
- [Device compatibility checker](https://esimagent.vdigital.app/checker) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown guidance with optional JSON configuration snippets and purchase links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include remote API requests, ranked plan summaries, deal details, compatibility guidance, and tracked affiliate buy links.] <br>

## Skill Version(s): <br>
1.8.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
