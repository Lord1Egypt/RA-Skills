## Description:

Complete AI travel concierge covering flights, hotels, lounges, awards, activities, deals, wallet, and recovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kurosh87](https://clawhub.ai/user/kurosh87)

### License/Terms of Use:

MIT

## Use Case:

External travelers and travel-planning agents use this skill to plan, compare, book, monitor, and optimize trips across flights, hotels, lounges, awards, activities, deals, wallet value, and jetlag recovery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use an Aerobase API key to book or cancel travel and change wallet or payment-related data without clearly requiring user confirmation.

Mitigation: Require explicit user approval before booking, cancellation, deletion, alert creation, or wallet/card/loyalty changes.

Risk: Aerobase API use may expose travel, booking, wallet, payment, and boarding-pass data to the third-party service.

Mitigation: Install only when the user or organization trusts Aerobase for those data categories and has reviewed the skill before use.

## Reference(s):

- [Aerobase API Reference](references/aerobase-api.md)
- [Aerobase Homepage](https://aerobase.app)
- [Aerobase OpenClaw Travel Agent](https://aerobase.app/openclaw-travel-agent)
- [Aerobase OpenAPI Spec](https://aerobase.app/api/v1/openapi)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Configuration]

**Output Format:** [Concise Markdown travel recommendations with endpoint-backed options and next actions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AEROBASE_API_KEY; responses should redact raw API keys and prioritize top options.]

## Skill Version(s):

3.3.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
