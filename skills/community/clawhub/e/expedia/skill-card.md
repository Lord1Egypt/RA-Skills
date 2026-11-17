## Description:

Search Expedia stays, packages, cars, and activities, compare real trip costs, and run partner-safe booking workflows with web and API modes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

Travelers, travel planners, and partner-integration developers use this skill to search and compare Expedia inventory, assess true trip cost, and prepare booking-safe web, redirect, or Rapid workflows before committing money.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Travel search details and optional partner search parameters may be sent to Expedia services.

Mitigation: Use the skill only when the user accepts sharing the relevant trip-planning context with Expedia, and keep local notes minimal and redacted.

Risk: Initial listing prices, redirect candidates, or package savings may not reflect the final bookable total.

Mitigation: Re-check taxes, mandatory fees, cancellation terms, inventory freshness, and exposed package costs before presenting an option as ready to book.

Risk: Partner API or live booking flows can expose credentials, traveler identity, billing data, or authorization material if used casually.

Mitigation: Run partner calls only with authorized Expedia credentials and explicit user approval, and do not store API keys, shared secrets, full authorization headers, payment data, or reusable booking tokens in markdown logs.

## Reference(s):

- [ClawHub Expedia Skill Page](https://clawhub.ai/ivangdavila/skills/expedia)
- [ClawHub Publisher Profile](https://clawhub.ai/user/ivangdavila)
- [Skill Homepage](https://clawic.com/skills/expedia)
- [Expedia Public Site](https://www.expedia.com/)
- [Expedia Travel Redirect Listings Endpoint](https://apim.expedia.com/hotels/listings)
- [Expedia Rapid API Endpoint Family](https://api.ean.com/v3/)
- [Expedia Rapid Test Endpoint Family](https://test.ean.com/v3/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with tables, concise status labels, and inline shell commands when partner workflows are authorized]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should identify web, redirect, or Rapid mode and separate search, price-check, and booking readiness.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
