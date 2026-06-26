## Description: <br>
Discover, curate, and register for crypto conference side events via Luma and Google Sheets <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[surlebeat](https://clawhub.ai/user/surlebeat) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill with an OpenClaw agent to discover crypto conference side events, curate a ranked schedule from user preferences, monitor for new events, and register for selected Luma events. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can submit event registrations and required consent checkboxes using stored personal information or session cookies. <br>
Mitigation: Review curated.md and target event URLs before registration, use a conservative registration strategy when appropriate, and delete luma-session.json and custom-answers.json when they are no longer needed. <br>
Risk: Untrusted community Google Sheets or event pages may influence the events selected for registration. <br>
Mitigation: Use trusted event sources, review discovered events before curation and registration, and avoid untrusted Google Sheets. <br>
Risk: Scheduled monitoring and saved Luma authentication can continue background checks against event sources. <br>
Mitigation: Enable scheduled monitoring or Luma login only when the user accepts persistent cookies and recurring checks; disable scheduled monitoring when the conference workflow is complete. <br>


## Reference(s): <br>
- [Conference Intern on ClawHub](https://clawhub.ai/surlebeat/conference-intern) <br>
- [OpenClaw](https://openclaw.com) <br>
- [Luma](https://lu.ma) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown schedules, JSON event and status files, shell command workflows, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates per-conference workspace files such as config.json, events.json, curated.md, registration-status.json, optional luma-session.json, and custom-answers.json.] <br>

## Skill Version(s): <br>
2.1.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
