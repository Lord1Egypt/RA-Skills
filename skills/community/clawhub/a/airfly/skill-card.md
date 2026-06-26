## Description: <br>
AI flight ticket assistant for domestic flight search, fare lookup, booking, order lookup, changes, cancellations, and refunds. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ryan-zry](https://clawhub.ai/user/ryan-zry) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-support agents use this skill to search domestic flights, compare cabin prices and fare rules, create booking orders, and manage order changes, cancellations, or refunds through the Fenbeitong flight service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles credentials and passenger identity data for booking workflows. <br>
Mitigation: Use it only with a trusted publisher and service; restore TLS certificate verification, store the apiKey in a user-private secure location, and mask passenger PII in outputs. <br>
Risk: Booking, change, cancellation, and refund workflows can affect paid travel orders. <br>
Mitigation: Require explicit, scoped user confirmation for paid bookings, changes, cancellations, and refunds after showing the flight, order, and fee details. <br>
Risk: Order-detail and booking outputs may expose phone numbers, passenger names, identity numbers, order IDs, and payment links. <br>
Mitigation: Redact sensitive values in chat, logs, screenshots, and support transcripts unless the user explicitly needs the value for the active transaction. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ryan-zry/airfly) <br>
- [Fenbeitong flight service endpoint](https://app-gate.fenbeitong.com/air_biz/skill/execute) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown and plaintext tables with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include order IDs, payment links, booking status, fare details, and temporary local JSON files used between workflow steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
