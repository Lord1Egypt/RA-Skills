## Description:

BondSeat helps diners monitor Resy cancellations or reservation releases and automatically books tables matching their authorized preferences.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bondseat](https://clawhub.ai/user/bondseat)

### License/Terms of Use:

MIT-0

## Use Case:

Diners use this skill to request hard-to-get Resy reservations, monitor cancellations or known release times, and check or stop existing requests. An agent confirms dining details and the success fee before enabling automatic booking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The external connector stores a private per-diner connection file and needs ongoing access to monitor availability.

Mitigation: Use isolated, persistent storage for each diner and do not reveal the connection file or credentials in chat.

Risk: A matching table may be booked automatically and incur a success fee.

Mitigation: Confirm the diner's reservation details and automatic-booking authorization, disclose the fee, and use the hosted page for payment consent.

Risk: Stopping a request does not cancel an existing reservation, and an in-flight booking may still complete.

Mitigation: Explain that stopping prevents future attempts and ask the diner to verify any uncertain outcome with the reservation provider.

## Reference(s):

- [BondSeat on ClawHub](https://clawhub.ai/bondseat/skills/bondseat)
- [BondSeat agent setup](https://bond-seat.com/agents)
- [BondSeat request management](https://bond-seat.com/agents/link)

## Skill Output:

**Output Type(s):** [Text, Guidance, Shell commands]

**Output Format:** [Markdown with setup links and JSON command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides request status and booked dining details; keeps credentials out of agent responses.]

## Skill Version(s):

0.1.3 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
