## Description: <br>
Book brake-service appointments through Lokuli MCP by searching providers, checking availability, and creating bookings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edwardrodriguez703-design](https://clawhub.ai/user/edwardrodriguez703-design) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to find brake-service providers through Lokuli, review available appointment times, and create a booking with customer contact details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Booking requests can send customer contact details and appointment selections to Lokuli. <br>
Mitigation: Before confirming an appointment, review the provider, time slot, and contact details, and only provide personal information when the user intends to proceed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/edwardrodriguez703-design/book-brake-service) <br>
- [Lokuli MCP Endpoint](https://lokuli.com/mcp/sse) <br>
- [Publisher Profile](https://clawhub.ai/user/edwardrodriguez703-design) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Guidance] <br>
**Output Format:** [JSON-RPC 2.0 MCP tool calls with concise booking guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses search, check_availability, and create_booking tool calls; booking creation may include customer name, email, and phone number.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
