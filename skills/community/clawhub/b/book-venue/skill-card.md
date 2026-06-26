## Description: <br>
Book Venue helps agents search for venues, check availability, and create bookings through Lokuli's MCP server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edwardrodriguez703-design](https://clawhub.ai/user/edwardrodriguez703-design) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to find venue services, check availability, and submit a booking through Lokuli when the user asks to book or find a venue. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create real venue bookings and send customer contact details to Lokuli. <br>
Mitigation: Confirm the venue, time, contact details, price, cancellation terms, and personal data sharing before calling create_booking. <br>
Risk: The artifact does not define clear confirmation safeguards before booking. <br>
Mitigation: Require explicit user approval for the final booking details before submitting any create_booking request. <br>


## Reference(s): <br>
- [Lokuli MCP endpoint](https://lokuli.com/mcp/sse) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls] <br>
**Output Format:** [Markdown guidance with JSON-RPC MCP call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Booking actions may include venue details, time slots, and customer contact information.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
