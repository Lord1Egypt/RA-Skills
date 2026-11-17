## Description:

Converts amounts between currencies using live exchange rates from the Open Exchange Rates API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sha-data](https://clawhub.ai/user/sha-data)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to answer currency-conversion requests with live exchange rates, converted amounts, and rate update timestamps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Exec-based command use with user-derived currency and amount arguments can create review-worthy execution risk.

Mitigation: Validate currency codes and amounts before execution and prefer a structured no-shell process call where possible.

Risk: Broad activation triggers may invoke the skill for ambiguous currency-related requests.

Mitigation: Narrow triggers to explicit conversion intent and confirm source currency, target currency, and amount when the request is unclear.

Risk: Open Exchange Rates receives the API key and requested currency symbols during live rate lookup.

Mitigation: Disclose the third-party API dependency, keep OXR_APP_ID secret, and avoid exposing the key in agent responses.

## Reference(s):

- [Currency Convert on ClawHub](https://clawhub.ai/sha-data/skills/currency-convert)
- [Open Exchange Rates](https://openexchangerates.org)
- [Open Exchange Rates Currency List](https://openexchangerates.org/currencies)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown response with conversion amount, exchange rate, and update timestamp]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3, exec tool access, and OXR_APP_ID for live Open Exchange Rates API calls.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
