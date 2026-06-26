## Description: <br>
Uses AigoHotel MCP tools to search hotels, apply structured filters, and confirm real-time room pricing and booking policy details. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dreamtzlong](https://clawhub.ai/user/dreamtzlong) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to turn hotel requirements such as location, dates, budget, star rating, and preferences into MCP hotel searches and room-detail checks. It is intended for hotel candidate comparison and price, availability, and policy confirmation based on returned tool data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release documentation publishes and encourages reuse of a shared API key or bearer token. <br>
Mitigation: Use a per-user AigoHotel credential stored in an environment variable or secret manager, and avoid committing or sharing real tokens in configs, screenshots, or repositories. <br>
Risk: Hotel availability, pricing, taxes, and cancellation policies can be misleading if inferred without tool confirmation. <br>
Mitigation: Quote only data returned by searchHotels or getHotelDetail, and call getHotelDetail before presenting room-level availability or policy conclusions. <br>


## Reference(s): <br>
- [AigoHotel MCP tool reference](references/tools.md) <br>
- [AigoHotel MCP configuration and run guide](references/mcp-config.md) <br>
- [ClawHub skill page](https://clawhub.ai/dreamtzlong/aigohotel-mcp) <br>
- [AigoHotel MCP API key application](https://mcp.agentichotel.cn/apply) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, shell commands] <br>
**Output Format:** [Markdown with structured hotel recommendations, assumptions, tool-result summaries, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results should state search assumptions and avoid claiming availability, prices, taxes, or cancellation terms unless returned by the MCP tools.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
