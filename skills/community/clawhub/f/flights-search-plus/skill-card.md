## Description: <br>
Searches flight prices through the 51smart API for one-way, round-trip, and price-calendar queries, with Chinese and English city-to-IATA handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[syf8888](https://clawhub.ai/user/syf8888) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to collect flight search details, call a disclosed third-party flight API, and present route, price, baggage, tax, and availability results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Flight search details are sent to the disclosed 51smart API. <br>
Mitigation: Avoid including unrelated personal information in travel queries and share only the route, dates, passenger counts, cabin class, and trip type needed for the search. <br>
Risk: Flight prices, baggage rules, taxes, airport codes, and seat availability can change or be returned incorrectly. <br>
Mitigation: Verify airports, dates, baggage, taxes, and prices before relying on the results or purchasing travel. <br>


## Reference(s): <br>
- [51smart flight search API endpoint](https://skill.flight.51smart.com/api/search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, guidance] <br>
**Output Format:** [Markdown flight search summaries with structured route, price, baggage, tax, and availability details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May ask follow-up questions for missing origin, destination, dates, passenger counts, cabin class, or trip type.] <br>

## Skill Version(s): <br>
1.1.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
