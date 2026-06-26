## Description: <br>
Plan and manage church events from start to finish with church-specific intelligence for ministry team coordination, volunteer rotation tracking, sermon series alignment, and liturgical calendar awareness. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chris-openclaw](https://clawhub.ai/user/chris-openclaw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Church staff and ministry coordinators use this skill to plan events, maintain task lists, coordinate volunteers and vendors, track budgets, and connect events with ministry teams, sermon series, and liturgical seasons. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores volunteer contact details, preferences, availability, workload notes, vendor information, and church event records in a persistent local event-data.json file. <br>
Mitigation: Store only necessary details, get consent for volunteer contact and preference data, periodically remove stale records, and limit access to the local data file. <br>
Risk: Broad event-planning triggers could activate the skill when the user did not intend to manage church records. <br>
Mitigation: Use explicit church-related prompts before creating or changing records, and confirm user intent before writing new event, volunteer, vendor, or budget data. <br>


## Reference(s): <br>
- [Church Event Planner release page](https://clawhub.ai/chris-openclaw/church-event-planner) <br>
- [README](README.md) <br>
- [Changelog](CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, configuration, guidance] <br>
**Output Format:** [Conversational Markdown with structured updates to event-data.json when event records change] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a local event-data.json file for events, tasks, vendors, volunteers, ministry teams, sermon series, and liturgical calendar data] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter, release evidence, README, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
