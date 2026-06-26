## Description: <br>
Track flight prices using Google Flights data, search routes and dates, filter results, monitor routes over time, and expose the same workflow through an MCP server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jackculpan](https://clawhub.ai/user/jackculpan) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to search flight options, compare prices across routes and dates, and track selected itineraries for price changes. It can be used through command-line scripts or as an MCP server with tools for search, calendar date search, tracking, price checks, listing, and removal. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Flight search details are sent to Google Flights during searches and price checks. <br>
Mitigation: Use the skill only when sharing route, date, passenger, and filter details with Google Flights is acceptable. <br>
Risk: Tracked itinerary history is stored locally in the skill data file. <br>
Mitigation: Remove tracked routes when they are no longer needed and delete the tracked data file if local history should not be retained. <br>
Risk: The setup installs unpinned Python dependencies. <br>
Mitigation: Install in a virtual environment and review or pin dependency versions before using the skill in managed environments. <br>


## Reference(s): <br>
- [FlightClaw on ClawHub](https://clawhub.ai/jackculpan/flightclaw) <br>
- [jackculpan publisher profile](https://clawhub.ai/user/jackculpan) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text and Markdown responses with command examples and structured flight result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include flight prices, airline and timing details, route tracking status, price-change alerts, and local tracked-route summaries.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
