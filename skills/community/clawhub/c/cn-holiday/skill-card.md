## Description: <br>
Queries Chinese public holidays, make-up workdays, and work schedules using timor.tech holiday data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deusyu](https://clawhub.ai/user/deusyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to answer China public-holiday, make-up workday, and work-schedule questions for a specific date, batch of dates, year, or next holiday/workday. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad trigger words such as holiday, workday, 上班, or 放假 may activate the skill unintentionally. <br>
Mitigation: Confirm the user's intended China holiday or workday lookup before running commands for ambiguous requests. <br>
Risk: Queried dates may be sent to timor.tech for lookup. <br>
Mitigation: Avoid sending sensitive or unnecessary date batches and disclose the external lookup when relevant. <br>


## Reference(s): <br>
- [Command Map](references/command-map.md) <br>
- [timor.tech Holiday API](https://timor.tech/api/holiday) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance, Text] <br>
**Output Format:** [Markdown with inline shell commands and JSON command output interpreted in natural language] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No API key is required; queried dates are sent to timor.tech for lookup.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
