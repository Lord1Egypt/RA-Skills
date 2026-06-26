## Description: <br>
Query China domestic flights with schedules, airline details, airport resolution, and Juhe reference prices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[baizhexue](https://clawhub.ai/user/baizhexue) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-support agents use this skill to look up China domestic one-way flight options for a specified route and date, including airport resolution, schedule details, and provider reference fares. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional local HTTP server can expose a sample_response parameter that reads caller-chosen local JSON files. <br>
Mitigation: Use CLI search mode or keep HTTP mode bound to localhost only; do not expose the service to other machines, and avoid sample_response unless it is restricted to bundled fixtures or removed from the HTTP API. <br>
Risk: Flight availability and fares are provider reference data and may be stale or differ from bookable ticket prices. <br>
Mitigation: Present ticket_price as a reference fare and ask users to verify itinerary and final price with a booking source before purchase. <br>


## Reference(s): <br>
- [Domestic Flight Search on ClawHub](https://clawhub.ai/baizhexue/domestic-flight-search-skill) <br>
- [Juhe Flight API Documentation](https://www.juhe.cn/docs/api/id/818) <br>
- [Juhe Provider Notes](references/provider-juhe.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON flight-search results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, network access to Juhe, and a user-provided JUHE_FLIGHT_API_KEY.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
