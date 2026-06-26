## Description: <br>
Triage, categorize, and draft responses to emails. Sorts by urgency, flags action items, and generates context-aware reply drafts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1kalin](https://clawhub.ai/user/1kalin) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Employees and external users use this skill to triage pasted or forwarded emails, sort them by urgency and next action, extract deadlines and action items, and draft concise replies for actionable messages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Email content can contain secrets, credentials, regulated data, or unnecessary personal details. <br>
Mitigation: Redact sensitive content before asking the agent to triage or draft from emails. <br>
Risk: Generated reply drafts may be incomplete, inaccurate, or inappropriate for the thread context. <br>
Mitigation: Review and edit every draft before sending. <br>
Risk: The skill references an external context-pack URL. <br>
Mitigation: Inspect or avoid the external site unless it is trusted for the intended use. <br>


## Reference(s): <br>
- [Email Triager on ClawHub](https://clawhub.ai/1kalin/afrexai-email-triager) <br>
- [Industry context packs](https://afrexai-cto.github.io/context-packs) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown with categorized email summaries, action items, and reply drafts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include grouped triage categories, checklists, deadline flags, escalation notes, and draft replies.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
