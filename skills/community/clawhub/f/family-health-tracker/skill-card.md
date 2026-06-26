## Description: <br>
Family Health Tracker helps users maintain local family health records, including profiles, allergies, medications, visits, immunizations, insurance basics, growth logs, providers, and reminders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chris-openclaw](https://clawhub.ai/user/chris-openclaw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to organize family health records in a local file, prepare for appointments, look up allergies and medications, and track due dates for visits, immunizations, dental cleanings, and refills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles family health information in a local health-data.json file. <br>
Mitigation: Install only if local storage is acceptable, protect the workspace, and avoid entering SSNs, full insurance IDs, financial account numbers, or detailed therapy notes. <br>
Risk: Health schedules and reminders may be incomplete or unsuitable for a specific person. <br>
Mitigation: Use reminders as organization aids and verify medical decisions, immunization timing, and treatment questions with a clinician. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chris-openclaw/family-health-tracker) <br>
- [Publisher profile](https://clawhub.ai/user/chris-openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Guidance] <br>
**Output Format:** [Conversational text, markdown summaries, and local JSON record updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update health-data.json in the user's working directory when the user logs records.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter, changelog, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
