## Description: <br>
Check flight schedules between supported airports, show timings, terminals, gates, delays, aircraft details, and optional departure countdowns using a local Python script backed by the Aviationstack API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[caddytan](https://clawhub.ai/user/caddytan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travelers, travel coordinators, and agents use this skill to check operating flight schedules between supported IATA airports, especially APAC routes and selected long-haul airports. It helps summarize flight times, terminals, gates, status, delays, aircraft details, and optional departure countdowns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Aviationstack API key and route lookup parameters are sent to Aviationstack for API-backed schedule checks. <br>
Mitigation: Use the skill only when that external API use is acceptable, keep AVIATIONSTACK_API_KEY private, and avoid committing ~/.openclaw/.env. <br>
Risk: Flight data and fallback lookup links may be incomplete or unavailable for unsupported airport codes or services. <br>
Mitigation: Use supported IATA airport codes from the built-in list and verify important travel details with an authoritative airline or airport source before acting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/caddytan/flight-tracker-apac) <br>
- [Aviationstack flight API endpoint](https://api.aviationstack.com/v1/flights) <br>
- [Google Flights fallback](https://www.google.com/travel/flights) <br>
- [FlightRadar24 fallback](https://www.flightradar24.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown summary with shell command examples and plain-text flight results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and AVIATIONSTACK_API_KEY for API-backed lookups; without the key, the script returns manual lookup links.] <br>

## Skill Version(s): <br>
1.0.1 (source: release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
