## Description:

Search, compare, and score flights with jetlag optimization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kurosh87](https://clawhub.ai/user/kurosh87)

### License/Terms of Use:

MIT

## Use Case:

External users and travel-planning agents use this skill to search, compare, and score flight options with jetlag-aware recovery context. It can validate fare offers and supports booking-related actions only with explicit user approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Booking workflows can expose payment card details, CVVs, passport data, or passenger identity information through an agent-facing flow.

Mitigation: Use search, comparison, scoring, and fare validation unless a secure checkout or tokenized payment flow with clear data-handling guarantees is available.

Risk: The skill includes booking-related API actions that could place or alter a travel booking.

Mitigation: Require explicit user approval before any booking-related action and validate fare availability or price changes before proceeding.

## Reference(s):

- [Aerobase Homepage](https://aerobase.app)
- [Aerobase OpenClaw Travel Agent Setup](https://aerobase.app/openclaw-travel-agent)
- [ClawHub Skill Page](https://clawhub.ai/kurosh87/skills/aerobase-travel-flights)

## Skill Output:

**Output Type(s):** [API Calls, Guidance, Markdown]

**Output Format:** [Markdown summaries with structured flight options and API request guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AEROBASE_API_KEY; free tier is capped at 5 requests/day.]

## Skill Version(s):

3.3.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
