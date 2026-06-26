## Description: <br>
Book professional apartment cleaning appointments in San Francisco through the claw.cleaning REST API, including availability checks, customer detail collection, explicit confirmation, booking, and status lookup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cnnrobrn](https://clawhub.ai/user/cnnrobrn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External customers and their agents use this skill to find available apartment-cleaning slots, prepare a booking summary, and reserve a San Francisco cleaning appointment after explicit confirmation. <br>

### Deployment Geography for Use: <br>
San Francisco, California, United States <br>

## Known Risks and Mitigations: <br>
Risk: Booking details include personal information such as name, email, and home address sent to claw.cleaning. <br>
Mitigation: Use only when the customer is comfortable sharing those details and review the full booking preview before confirmation. <br>
Risk: The booking endpoint reserves an appointment immediately after confirmation, even though payment is made later. <br>
Mitigation: Confirm date, time, address, email, hours, and total cost with the customer before initiating the booking. <br>
Risk: Availability can change before booking is posted. <br>
Mitigation: Check current availability before initiating a booking and offer alternatives if the slot is no longer available. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cnnrobrn/claw-cleaning) <br>
- [Publisher profile](https://clawhub.ai/user/cnnrobrn) <br>
- [claw.cleaning API base URL](https://claw.cleaning) <br>
- [Full example booking flow](references/booking-flow.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API calls, Shell commands, Guidance] <br>
**Output Format:** [Markdown responses with JSON request bodies and optional curl commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an agent with HTTPS request capability; booking is reserved only after explicit customer confirmation.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
