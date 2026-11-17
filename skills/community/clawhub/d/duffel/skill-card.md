## Description:

Search, book, and manage flights via the Duffel Flights API, including flight search, offer comparison, booking, order status, cancellation, seat maps, and airport or city lookup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fabiolr](https://clawhub.ai/user/fabiolr)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to search, compare, book, inspect, and cancel flights through Duffel-backed airline inventory. It is useful when an agent needs to produce CLI commands, booking workflow guidance, or JSON API output for a Duffel flight workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Production use can create real bookings, spend Duffel account balance, and send traveler details to Duffel and travel providers.

Mitigation: Prefer a Duffel test token first, verify fare details and passenger data, and require explicit user confirmation before booking.

Risk: Cancellation commands can affect real orders when confirmed.

Mitigation: Review the cancellation quote and refund amount before using --confirm, and require explicit user confirmation before cancellation.

Risk: Numbered offer and cancellation references rely on shared temporary cache files under /tmp, which can be stale or ambiguous.

Mitigation: Use explicit Duffel offer, order, and cancellation IDs for real purchases, and clear /tmp Duffel cache files after use.

## Reference(s):

- [Duffel API Guide](artifact/references/api-guide.md)
- [Booking Flow](artifact/references/booking-flow.md)
- [Duffel API](https://api.duffel.com)
- [Duffel Dashboard](https://app.duffel.com)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, JSON, text]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON API output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a DUFFEL_TOKEN environment variable and may call the Duffel API.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
