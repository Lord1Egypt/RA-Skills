## Description:

AigoHotel MCP helps agents search, compare, price, book, and review hotel reservations through the RollingGo hotel service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dreamtzlong](https://clawhub.ai/user/dreamtzlong)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-support agents use this skill to find hotels by destination, budget, rating, amenities, or brand, compare options, retrieve real-time room prices, create hotel bookings, and check booking history. The workflow handles real purchases, so users should confirm selected rooms, guest details, total price, cancellation policy, and payment link before completing payment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create real hotel orders and expose booking history, names, email addresses, prices, order identifiers, and payment links.

Mitigation: Require explicit user confirmation before price lock, booking, or payment handoff, and show only the booking details needed for the user to verify the purchase.

Risk: Installation and updates depend on mutable external npm packages and GitHub release assets.

Mitigation: Install only from trusted RollingGo channels, avoid administrator privileges where possible, and review updates before applying them.

Risk: Prices and room availability can change after search results are shown.

Mitigation: Label search prices as reference prices and confirm the current total price and cancellation policy before booking.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dreamtzlong/skills/aigohotel-mcp)
- [CLI command reference](references/cli-params.md)
- [RollingGo Hotel CLI releases](https://github.com/RollingGo-AI/oauth-hotel-cli/releases/latest)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries with hotel options, room prices, booking details, payment links, and concise operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include hotel images, prices, cancellation policies, order identifiers, and payment links while suppressing internal command and JSON details from end users.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
