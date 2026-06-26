## Description: <br>
Plans Grand Slam tennis trips by combining tournament calendar data with flyai travel searches for flights, hotels, tickets, attractions, and practical travel tips. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lokwq](https://clawhub.ai/user/lokwq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travelers and tennis fans use this skill to plan trips around the Australian Open, French Open, Wimbledon, or US Open. It helps choose tournament dates and rounds, search travel options, and assemble a venue-centered itinerary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses the third-party flyai CLI and may send travel search details such as origin city, dates, and destination to that service. <br>
Mitigation: Install and run it only if you are comfortable using flyai for the trip details involved. <br>
Risk: Visa and entry guidance can be incomplete or change before travel. <br>
Mitigation: Verify visa requirements with official government or consular sources for the traveler's passport before booking. <br>
Risk: The helper script writes raw travel search results to /tmp/slam-trip-results, which may remain on shared machines. <br>
Mitigation: Delete /tmp/slam-trip-results after use, especially on shared or managed systems. <br>


## Reference(s): <br>
- [Grand Slam Calendar](artifact/references/grand-slam-calendar.md) <br>
- [flyai CLI Commands Reference](artifact/references/flyai-commands.md) <br>
- [Grand Slam Travel Tips](artifact/references/travel-tips.md) <br>
- [Itinerary Template](artifact/assets/itinerary-template.md) <br>
- [ClawHub skill page](https://clawhub.ai/lokwq/ace-trip) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown itinerary with tables, booking links, image references, and optional shell commands for flyai searches] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use flyai real-time travel results and temporary JSON files under /tmp/slam-trip-results when the helper script is run.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
