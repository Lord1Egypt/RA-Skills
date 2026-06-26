## Description: <br>
Manage a sales pipeline through natural language by adding leads, updating stages, logging interactions, setting follow-up reminders, and generating pipeline reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PhilipStark](https://clawhub.ai/user/PhilipStark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users such as solo founders, small sales teams, and freelancers use this skill to track leads, deals, follow-ups, revenue forecasts, and sales activity from chat instead of a full CRM system. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores prospect, outreach, and sales pipeline information in local plaintext JSON files. <br>
Mitigation: Keep the local workspace protected, avoid committing CRM data to public repositories, and use appropriate endpoint and filesystem controls. <br>
Risk: Generated outreach or follow-up content could be inaccurate, poorly targeted, or sent prematurely if automated. <br>
Mitigation: Review generated emails and follow-up actions before sending, and avoid enabling auto-send or scheduled autopilot behavior until the workflow is verified. <br>
Risk: Pipeline data may include sensitive contact details and commercial opportunity information. <br>
Mitigation: Do not store passwords, payment card numbers, SSNs, or other unrelated secrets, and redact sensitive records before sharing exports. <br>


## Reference(s): <br>
- [CRM Pipeline Manager on ClawHub](https://clawhub.ai/PhilipStark/fl-crm-pipeline) <br>
- [Publisher profile: PhilipStark](https://clawhub.ai/user/PhilipStark) <br>
- [Creator profile referenced by artifact](https://threads.net/@felipe_bmottaa) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Files, Configuration, Guidance] <br>
**Output Format:** [Markdown responses with local JSON pipeline data and optional CSV exports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores prospect, deal, interaction, reminder, and forecast data in local plaintext files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
