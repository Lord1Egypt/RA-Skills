## Description: <br>
Helps agents gather event staffing requirements, check TempGuru market coverage, rate ranges, availability guidance, and state compliance, and prepare or submit a structured quote request for W-2 event staff in the United States and Canada. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kissmyabs32](https://clawhub.ai/user/kissmyabs32) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to plan event staffing needs, estimate W-2 staffing costs, surface location-specific compliance notes, and submit a human-reviewed TempGuru quote request. <br>

### Deployment Geography for Use: <br>
United States and Canada <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence reports a suspicious verdict and flags account-impacting maintainer actions in the bundle. <br>
Mitigation: Install only when the publisher is trusted, review sensitive helper behavior before use, avoid broad-access defaults, and run privileged actions only with explicit intent and appropriate credentials. <br>
Risk: The quote-request flow can submit contact, company, event, role, and headcount details to TempGuru for human review. <br>
Mitigation: Confirm the staffing plan and user consent before invoking request_quote; otherwise provide the plan as a draft. <br>
Risk: Rate ranges and availability guidance are planning estimates, not final pricing or a reservation. <br>
Mitigation: Label estimates clearly and state that final pricing and availability come from TempGuru after review. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/kissmyabs32/event-staffing-ordering) <br>
- [TempGuru MCP endpoint](https://mcp.tempguru.co/mcp) <br>
- [TempGuru machine-readable site overview](https://tempguru.co/llms.txt) <br>
- [TempGuru city staffing guide pattern](https://tempguru.co/insights/{city}-event-staffing) <br>
- [TempGuru role guide pattern](https://tempguru.co/insights/{role}-in-{city}) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, API calls, configuration] <br>
**Output Format:** [Markdown guidance with structured staffing request details and MCP tool calls when appropriate] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes planning estimates, compliance notes, lead-time guidance, and optional quote-request submission details.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
