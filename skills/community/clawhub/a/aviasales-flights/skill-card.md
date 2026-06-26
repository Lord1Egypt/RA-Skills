## Description: <br>
Searches cheap flights and airfare through the Travelpayouts/Aviasales API, including date-specific search, price calendars, round trips, latest prices, popular destinations, and IATA lookup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aspalagin](https://clawhub.ai/user/aspalagin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to search Aviasales/Travelpayouts flight data, compare cheapest options, resolve IATA codes, and present booking links for travel queries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Flight searches send route details, dates, and preferences to Travelpayouts/Aviasales. <br>
Mitigation: Use the skill only when users are comfortable sharing those search details with the Travelpayouts/Aviasales service. <br>
Risk: The helper script requires a Travelpayouts API token for most searches. <br>
Mitigation: Store the token in the TRAVELPAYOUTS_TOKEN environment variable, use a dedicated token where possible, and avoid placing it in chat or logs. <br>
Risk: The helper script writes a low-sensitivity airline-name cache in /tmp for 24 hours. <br>
Mitigation: Treat the cache as operational metadata and clear /tmp according to local environment policy on shared systems. <br>


## Reference(s): <br>
- [Aviasales Flight Search on ClawHub](https://clawhub.ai/aspalagin/aviasales-flights) <br>
- [Airline Code Fallback Reference](references/airlines.md) <br>
- [Travelpayouts Flight Search API Endpoint](https://api.travelpayouts.com/aviasales/v3/prices_for_dates) <br>
- [Travelpayouts Latest Prices API Endpoint](https://api.travelpayouts.com/aviasales/v3/get_latest_prices) <br>
- [Travelpayouts Price Calendar API Endpoint](https://api.travelpayouts.com/aviasales/v3/grouped_prices) <br>
- [Travelpayouts City Directions API Endpoint](https://api.travelpayouts.com/v1/city-directions) <br>
- [Travelpayouts Places Autocomplete API Endpoint](https://autocomplete.travelpayouts.com/places2) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands and JSON stdout from the helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TRAVELPAYOUTS_TOKEN for flight searches; IATA lookup does not require the token.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
