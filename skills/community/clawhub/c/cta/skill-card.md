## Description: <br>
Chicago CTA transit support for real-time L train arrivals, bus predictions, service alerts, and route information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brianleach](https://clawhub.ai/user/brianleach) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and agents use this skill to answer Chicago public transit questions, including train arrivals, bus predictions, service alerts, vehicle locations, nearby stops, and route details. <br>

### Deployment Geography for Use: <br>
Chicago, Illinois, United States <br>

## Known Risks and Mitigations: <br>
Risk: Train and bus commands require CTA developer API keys, which may be stored in environment variables or a skill-local .env file. <br>
Mitigation: Store keys outside shared files, avoid committing .env files, and rotate keys if they are exposed. <br>
Risk: CTA API keys are sent to official CTA services as HTTPS query parameters for authenticated train and bus lookups. <br>
Mitigation: Use CTA-issued keys only for this skill and avoid sharing logs or command output that could contain request URLs. <br>
Risk: The refresh-gtfs command creates or updates a local schedule cache under ~/.cta/gtfs/. <br>
Mitigation: Run refresh-gtfs only when a local CTA schedule cache is desired, and remove that directory if the cache should be cleared. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/brianleach/cta) <br>
- [Publisher profile](https://clawhub.ai/user/brianleach) <br>
- [CTA Train Tracker developer access](https://www.transitchicago.com/developers/traintrackerapply/) <br>
- [CTA Bus Tracker developer access](https://www.transitchicago.com/developers/bustracker/) <br>
- [CTA GTFS static feed](https://www.transitchicago.com/downloads/sch_data/google_transit.zip) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown or plain-text transit answers with optional shell commands for the bundled CTA CLI.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include arrival times, route names, stop identifiers, service-alert summaries, and setup guidance for CTA API keys.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
