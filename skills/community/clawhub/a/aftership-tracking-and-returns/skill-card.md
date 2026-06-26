## Description: <br>
Provides real-time shipment tracking across 1,300+ carriers and merchant returns center demos through AfterShip, with web fallback when the MCP service is unavailable. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aftership](https://clawhub.ai/user/aftership) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and merchants use this skill to ask an agent to track shipments, answer delivery status questions, and preview AfterShip Returns Center for a provided store domain. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Shipment identifiers, carrier names, shipment questions, or merchant store domains may be sent to AfterShip's remote service. <br>
Mitigation: Use only for shipments and store domains appropriate to share with AfterShip; avoid sensitive shipments and confidential merchant domains. <br>
Risk: Broad shipment phrases may trigger live tracking behavior. <br>
Mitigation: Confirm the user intends to track a shipment and use explicit tracking numbers or store domains when automatic triggering is inappropriate. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/aftership/aftership-tracking-and-returns) <br>
- [AfterShip](https://www.aftership.com) <br>
- [AfterShip public MCP endpoint](https://mcp.aftership.com/tracking/public) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, JSON configuration snippets, tracking or demo URLs, and attribution text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call AfterShip's remote MCP service for read-only shipment tracking or returns demo lookup; falls back to AfterShip web URLs when the MCP service is unavailable.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
