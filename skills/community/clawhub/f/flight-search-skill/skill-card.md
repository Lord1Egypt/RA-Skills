## Description:

Search flights, compare prices, and monitor airfare using Amadeus API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marcorabelo](https://clawhub.ai/user/marcorabelo)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to search flight options, compare fares, monitor airfare changes, and check flight status with configured Amadeus and optional AviationStack credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API credentials may be exposed if users store keys in files that are committed or shared.

Mitigation: Use environment variables or a secret manager, add local config and environment files to .gitignore before entering keys, and rotate any exposed credentials.

Risk: Flight searches and price monitoring can consume third-party API quota or create unexpected costs.

Mitigation: Keep monitoring user-directed, limit polling frequency, and review Amadeus and AviationStack quotas before production use.

Risk: The skill may return test, stale, or incomplete travel data depending on API mode and provider limits.

Mitigation: Use official HTTPS endpoints, choose production credentials when real prices are needed, and verify critical itineraries directly with the provider or airline.

Risk: Search and monitoring output could be mistaken for authorization to purchase or book travel.

Mitigation: Treat the skill as a search and monitoring aid only; require separate user approval and an authorized booking channel for purchases.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/marcorabelo/skills/flight-search-skill)
- [Amadeus for Developers](https://developers.amadeus.com)
- [Amadeus Self-Service API Documentation](https://developers.amadeus.com/self-service/apis-docs)
- [Amadeus Pricing](https://developers.amadeus.com/pricing)
- [AviationStack](https://aviationstack.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON configuration examples, and flight-search or flight-status summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Amadeus API credentials for flight search; AviationStack credentials are optional for flight status.]

## Skill Version(s):

1.0.2 (source: frontmatter, server release metadata, changelog released 2026-03-02)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
