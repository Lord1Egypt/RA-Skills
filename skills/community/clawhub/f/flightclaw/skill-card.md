## Description:

FlightClaw helps agents search Google Flights, compare dates and filters, track route prices over time, and report price-drop alerts through CLI scripts or an MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jackculpan](https://clawhub.ai/user/jackculpan)

### License/Terms of Use:


## Use Case:

External users and developers use FlightClaw to search flight routes, compare prices across dates and filters, track selected itineraries, and surface price-drop alerts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact says price history persists via R2 backup, but the evidence does not describe user controls for opting out or deleting backed-up travel history.

Mitigation: Verify whether R2 backup is enabled before installation, and confirm opt-out and deletion procedures before tracking routes.

Risk: The setup script installs mutable `flights` and `mcp` package versions.

Mitigation: Install in an isolated Python environment and review or pin dependency versions before use.

Risk: Flight search details are sent to Google Flights and tracked routes are stored locally.

Mitigation: Avoid entering sensitive itineraries unless that data sharing and local storage are acceptable; remove tracked routes when they are no longer needed.

## Reference(s):

- [ClawHub FlightClaw release page](https://clawhub.ai/jackculpan/skills/flightclaw)
- [Google Flights shopping results endpoint](https://www.google.com/_/FlightsFrontendUi/data/travel.frontend.flights.FlightsFrontendService/GetShoppingResults)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text and Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include flight options, route IDs, prices, currencies, price history summaries, and alert messages.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
