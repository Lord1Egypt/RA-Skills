## Description:

Hotel search, booking, amendments, loyalty vouchers, and jetlag-friendly layover stays.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kurosh87](https://clawhub.ai/user/kurosh87)

### License/Terms of Use:

MIT

## Use Case:

External travel users and travel-support agents use this skill to search hotels, compare layover-friendly stays, check rates, and manage hotel bookings through Aerobase APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can initiate or change hotel bookings, including cancellations, rebooks, amendments, voucher redemptions, and payments.

Mitigation: Before any high-impact action, show the exact booking, policy, fees, and action being taken, then get explicit user confirmation.

Risk: The skill requires trust in Aerobase with hotel-search and booking-management authority.

Mitigation: Install only when the user trusts Aerobase for this authority, keep API keys redacted, and keep the interaction focused on public booking metadata and user constraints.

## Reference(s):

- [Aerobase homepage](https://aerobase.app)
- [Aerobase OpenClaw travel agent setup](https://aerobase.app/openclaw-travel-agent)
- [ClawHub skill page](https://clawhub.ai/kurosh87/skills/aerobase-travel-hotels)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown text with structured API request guidance and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AEROBASE_API_KEY. Booking, cancellation, amendment, rebooking, voucher redemption, and payment actions should be shown to the user and explicitly confirmed before execution.]

## Skill Version(s):

3.3.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
