## Description: <br>
discava helps agents search local businesses worldwide through the discava API and return structured business data with confidence scores and demand rankings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sebastian1747](https://clawhub.ai/user/sebastian1747) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and users use discava to find local businesses, services, restaurants, doctors, craftsmen, and other local providers by query, city, country, or category. It supports search, detailed business lookup, demand rankings, autocomplete suggestions, and data-quality feedback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms, locations, optional coordinates, and feedback comments are sent to discava.ai. <br>
Mitigation: Avoid private personal, medical, legal, or confidential details, and send only the minimum location or feedback data needed for the search. <br>
Risk: Interactive HTML cards may include click tracking for phone, email, website, and navigation actions. <br>
Mitigation: Prefer JSON output for ordinary searches and use HTML cards only when an interactive display is needed. <br>


## Reference(s): <br>
- [discava API](https://discava.ai/api/v1) <br>
- [discava ClawHub page](https://clawhub.ai/sebastian1747/discava) <br>
- [OpenStreetMap](https://www.openstreetmap.org) <br>
- [Open Data Commons Open Database License](https://opendatacommons.org/licenses/odbl/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with curl examples and JSON or HTML API responses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results may include confidence scores, demand scores, relevance scores, pagination metadata, contact details, opening hours, and optional interactive HTML cards.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
