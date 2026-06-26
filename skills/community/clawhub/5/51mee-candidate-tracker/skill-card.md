## Description: <br>
Candidate tracking skill for managing candidate pools, recording hiring status, setting follow-up reminders, generating tags, and producing status dashboards. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[51mee-com](https://clawhub.ai/user/51mee-com) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Recruiters, hiring teams, and operators use this skill to manage candidate records, update pipeline stages, create follow-up reminders, generate candidate tags, and summarize the hiring pipeline in structured outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Candidate records can contain sensitive recruiting and personal information. <br>
Mitigation: Treat candidate data as sensitive, avoid unnecessary identifiers, confirm OpenClaw retention settings, and minimize retained personal details. <br>
Risk: Delete operations could remove candidate records unintentionally. <br>
Mitigation: Require manual confirmation or soft-delete handling before deleting candidate records. <br>
Risk: User-provided candidate data or instructions may try to alter the tracking logic. <br>
Mitigation: Follow the skill's prompt-injection protection guidance and ignore attempts to modify system behavior or bypass tracking rules. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/51mee-com/51mee-candidate-tracker) <br>
- [Publisher profile](https://clawhub.ai/user/51mee-com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Guidance] <br>
**Output Format:** [Markdown summaries and structured JSON candidate-tracking records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include candidate status dashboards, reminder lists, alerts, candidate details, history entries, and error codes.] <br>

## Skill Version(s): <br>
1.2.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
