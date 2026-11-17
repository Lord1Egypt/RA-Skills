## Description:

Book a professional apartment cleaning in San Francisco via the claw.cleaning REST API, including availability checks, customer detail collection, explicit booking confirmation, and appointment status lookup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cnnrobrn](https://clawhub.ai/user/cnnrobrn)

### License/Terms of Use:

MIT-0

## Use Case:

External customers use this skill through an agent to check availability and book professional apartment cleaning appointments for San Francisco addresses. The agent collects scheduling details, address, name, and email, confirms the total and payment terms, and then initiates the booking through the claw.cleaning API.

### Deployment Geography for Use:

San Francisco, California, United States

## Known Risks and Mitigations:

Risk: The status lookup can reveal a customer's home address and appointment schedule when queried with only an email address.

Mitigation: Use the status lookup only when the requester is clearly the customer, and treat customer contact details, home addresses, and schedules as sensitive.

Risk: The booking endpoint immediately reserves a slot and sends a calendar invite.

Mitigation: Check availability first, show a full booking preview with total cost and payment terms, and obtain explicit customer confirmation before initiating the booking.

## Reference(s):

- [Full Example Booking Flow](references/booking-flow.md)
- [claw.cleaning API](https://claw.cleaning)
- [Apartment Cleaning on ClawHub](https://clawhub.ai/cnnrobrn/skills/claw-cleaning)

## Skill Output:

**Output Type(s):** [guidance, API calls, shell commands, markdown]

**Output Format:** [Markdown guidance with HTTPS request examples and JSON request or response bodies]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit customer confirmation before creating a booking; status lookup should be used only when the requester is clearly the customer.]

## Skill Version(s):

1.0.7 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
