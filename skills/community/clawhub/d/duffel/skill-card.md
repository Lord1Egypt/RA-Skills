## Description: <br>
Search, book, and manage flights via the Duffel Flights API across 300+ airlines, with support for offer comparison, fare details, booking, order status, cancellation, seat maps, and airport or city lookup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fabiolr](https://clawhub.ai/user/fabiolr) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and travel operations users use this skill to search, compare, book, inspect, and cancel flights through Duffel from an agent-assisted CLI workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live Duffel tokens can spend account balance, issue real tickets, send passenger details to Duffel and travel providers, or cancel existing orders. <br>
Mitigation: Use sandbox Duffel tokens first and require explicit user approval before booking or confirmed cancellation commands with live tokens. <br>
Risk: Temporary search and cancellation files may be stored under /tmp on the local machine. <br>
Mitigation: Avoid shared machines for sensitive travel work or clear temporary Duffel files after use. <br>


## Reference(s): <br>
- [Duffel Flights on ClawHub](https://clawhub.ai/fabiolr/duffel) <br>
- [Duffel dashboard](https://app.duffel.com) <br>
- [Duffel API](https://api.duffel.com) <br>
- [Duffel API Guide](references/api-guide.md) <br>
- [Booking Flow](references/booking-flow.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and optional JSON API output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses DUFFEL_TOKEN for authentication and may save temporary search or cancellation state under /tmp.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
