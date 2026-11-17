## Description:

Helps users find hidden-city flight opportunities by comparing one-way direct fares with one-stop connecting itineraries that pass through the intended destination.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coder-0x7fffffff](https://clawhub.ai/user/coder-0x7fffffff)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-planning agents use this skill to search one-way hidden-city fare opportunities, compare savings against a direct-flight baseline, and present booking QR links with passenger risk warnings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on installing a global, unpinned npm CLI.

Mitigation: Use an isolated environment, pin and review the @fly-ai/flyai-cli version before use, and reinstall only from the expected npm package source.

Risk: Booking links can be shared with a third-party QR-code service when QR links are opened or previewed.

Mitigation: Avoid sensitive or signed booking URLs, and review generated QR links before sharing them with users.

Risk: Hidden-city itineraries can create baggage, airline-policy, missed-segment, return-ticket, and international-document risks.

Mitigation: Independently verify airline policy, baggage handling, visa and passport requirements, and ticketing consequences before purchase; prefer one-way trips and hand luggage.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/coder-0x7fffffff/skills/bargain-flights)
- [ClawHub publisher profile](https://clawhub.ai/user/coder-0x7fffffff)
- [bargain-flights reference](artifact/references/bargain-flights.md)
- [@fly-ai/flyai-cli npm package](https://www.npmjs.com/package/@fly-ai/flyai-cli)
- [Feizhu flight API endpoint](https://a.feizhu.com)
- [QR Server API endpoint](https://api.qrserver.com)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown tables and links, with JSON outputs from helper scripts and inline shell commands for flight lookup.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include explored route summaries, candidate hidden-city fare recommendations, QR-code booking links, and required baggage, itinerary, airline-policy, and visa/passport warnings.]

## Skill Version(s):

1.0.8 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
