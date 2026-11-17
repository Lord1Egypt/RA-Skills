## Description:

Travel With Family helps agents produce family-friendly travel plans that combine kid-aware itinerary guidance with bookable hotels, attractions, packages, and flights when a destination is provided.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zuckonit](https://clawhub.ai/user/zuckonit)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-planning agents use this skill to answer family travel requests with child-aware itineraries, booking references, and pre-trip checks. It is aimed at trips involving children, stroller or nap needs, solo-parent logistics, rainy-day backups, child-ticket reminders, refund reminders, and similar constraints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on an external travel CLI, so travel-search details may be shared with that provider.

Mitigation: Use the skill only when that data-sharing posture is acceptable and avoid submitting unnecessary sensitive personal, medical, or child information.

Risk: Installing the required CLI through npm introduces supply-chain risk.

Mitigation: Prefer a pinned, reviewed, isolated installation of @fly-ai/flyai-cli before enabling the skill in shared or production agent environments.

Risk: Booking links, prices, child-ticket rules, facilities, and refund terms can change or may be incomplete in search results.

Mitigation: Treat travel results as planning aids and verify purchase-critical details on the booking page, airline page, venue page, or with the provider before purchase.

Risk: Optional API-key configuration may create long-lived credential exposure.

Mitigation: Avoid storing long-lived API keys unless needed, and use normal secret-management practices if an API key is configured.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zuckonit/skills/family-trip-travel)
- [README](README.md)
- [flyai CLI capabilities and family travel mapping](references/cli-capabilities.md)
- [Professional family itinerary output guidance](references/output-professional.md)
- [Family query templates](references/family-queries.md)
- [Family flight-search notes](references/search-flight-family.md)
- [Family hotel-search notes](references/search-hotels-family.md)
- [Family point-of-interest search notes](references/search-poi-family.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown travel guidance with optional inline shell command examples and booking-reference presentation rules]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses should avoid user-visible internal tooling terms, show available images before booking links, and ask for missing trip constraints when needed.]

## Skill Version(s):

1.0.0 (source: server release metadata and release changelog; artifact metadata.version reports 1.4.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
