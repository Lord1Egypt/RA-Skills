## Description: <br>
Search flights, compare prices, and monitor airfare using Amadeus API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MarcoRabelo](https://clawhub.ai/user/MarcoRabelo) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and travel-planning agents use this skill to search flight options, compare fares, monitor price drops, and optionally check flight status with user-supplied API credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Travel queries are sent to third-party flight APIs and may reveal itinerary interests. <br>
Mitigation: Use only API providers and account settings you trust, review provider terms, and avoid submitting sensitive routes when unnecessary. <br>
Risk: API keys and local configuration can be exposed if config.json is committed or shared. <br>
Mitigation: Keep config.json out of version control, prefer environment variables or protected config storage, and rotate keys if exposed. <br>
Risk: API quotas and pay-as-you-go usage can create unexpected costs. <br>
Mitigation: Start in sandbox mode, monitor API usage and quotas, and switch to production mode only when real pricing data is needed. <br>
Risk: Local price monitoring data can reveal sensitive travel plans. <br>
Mitigation: Delete or protect .monitored_flights.json and limit monitored routes to trips users are comfortable storing locally. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/MarcoRabelo/flight-search-skill) <br>
- [Publisher profile](https://clawhub.ai/user/MarcoRabelo) <br>
- [Amadeus for Developers](https://developers.amadeus.com) <br>
- [Amadeus API documentation](https://developers.amadeus.com/self-service/apis-docs) <br>
- [Amadeus pricing](https://developers.amadeus.com/pricing) <br>
- [AviationStack](https://aviationstack.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-supplied Amadeus credentials; optional AviationStack credentials enable flight status.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter, release evidence, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
