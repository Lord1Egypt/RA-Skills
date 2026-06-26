## Description: <br>
Provides flight prices with Amadeus, train itineraries and schedules with Navitia, and nearby EV charge points using Open Charge Map. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aaureli](https://clawhub.ai/user/aaureli) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Travelers, mobility planners, and supporting agents use this skill to compare flight offers, plan public transport or train journeys, and find nearby EV charging points from third-party travel APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Configurable API host environment variables can send live API credentials to non-default endpoints. <br>
Mitigation: Keep host override variables unset unless the endpoint is intentionally trusted, and use low-privilege or test credentials where possible. <br>
Risk: Travel and location queries are transmitted to third-party services. <br>
Mitigation: Avoid submitting sensitive itinerary, place, coordinate, or account data unless sharing it with the selected travel API provider is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aaureli/air-train-ev) <br>
- [Open Charge Map API documentation](https://openchargemap.org/site/develop/api) <br>
- [Open Charge Map POI endpoint](https://api.openchargemap.io/v3/poi/) <br>
- [Navitia documentation](https://doc.navitia.io/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, command-line examples, environment variable setup, and plain-text travel or charging summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires API credentials for Amadeus, Navitia, and Open Charge Map; route, date, place, and coordinate queries are sent to the relevant third-party APIs.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
