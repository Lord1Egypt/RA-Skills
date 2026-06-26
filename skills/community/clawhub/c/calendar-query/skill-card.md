## Description: <br>
Query Matt's calendars with the gog CLI, prioritizing the Flowcode work calendar and adding personal calendar context when relevant. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[williamsmatt](https://clawhub.ai/user/williamsmatt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
People authorized to access Matt's calendars use this skill to answer schedule, availability, event, reminder, and keyword-search questions from the configured work and personal calendars. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read work and personal calendar details through an already-authenticated local gog account. <br>
Mitigation: Install only where the agent is authorized to access those calendars, and avoid use in shared environments where private calendar details could be exposed. <br>
Risk: Broad calendar queries may return more schedule or personal context than needed. <br>
Mitigation: Use narrow date ranges, specify the calendar to check, and include personal calendar notes only when relevant to the user's request. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/williamsmatt/calendar-query) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and chronological calendar summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses narrow date ranges and calendar-specific queries where possible; reports gog errors and suggests retrying or re-authenticating.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
