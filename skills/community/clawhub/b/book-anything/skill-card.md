## Description: <br>
Searches for businesses such as restaurants, salons, clinics, and hotels, then helps book, cancel, reschedule, or ask merchant questions through AI phone calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[danielzhangreal](https://clawhub.ai/user/danielzhangreal) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and their agents use this skill to search for local businesses, retrieve details, and complete bookings or merchant inquiries through the LifeClaw API. It is also used to cancel or reschedule existing reservations when the user has confirmed the intended action. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place paid outbound AI phone calls. <br>
Mitigation: Require explicit user confirmation before each phone call and monitor token balance or revoke LIFECLAW_API_TOKEN if needed. <br>
Risk: The skill can cancel, reschedule, or update real booking records. <br>
Mitigation: Require explicit confirmation before cancellation, rescheduling, booking-record updates, or sharing contact details. <br>
Risk: Booking details and contact information are sent to LifeClaw and may be disclosed to merchants to complete reservations. <br>
Mitigation: Use the skill only when the user agrees to share the relevant booking details and contact information for the requested transaction. <br>


## Reference(s): <br>
- [Book Anything ClawHub Listing](https://clawhub.ai/danielzhangreal/book-anything) <br>
- [LifeClaw Homepage](https://lifeclaw.agentese.ai) <br>
- [LifeClaw Skill API Reference](artifact/references/api.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls, text] <br>
**Output Format:** [Markdown guidance with REST API examples and JSON request or response bodies] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LIFECLAW_API_TOKEN and may initiate paid outbound phone calls through the LifeClaw API.] <br>

## Skill Version(s): <br>
1.4.2 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
