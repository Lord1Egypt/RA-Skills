## Description: <br>
Operate Breakcold CRM through the hosted Breakcold MCP server from OpenClaw or ClawHub for CRM work, deals, pipeline updates, follow-up tasks, reports, prospect research, inbox contact detection, CRM setup, notes, custom fields, and multichannel inbox workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[matteoolefloch](https://clawhub.ai/user/matteoolefloch) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Breakcold users and developers use this skill to let an agent operate a Breakcold CRM workspace through the hosted MCP server. It supports follow-up task creation, pipeline movement, CRM reports, prospect research, inbox contact detection, CRM setup or reorganization, scheduled routines, and related CRM record updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read sensitive inbox and CRM data. <br>
Mitigation: Install only for agents that should operate Breakcold on the user's behalf, and confirm the intended workspace before use. <br>
Risk: The skill can make broad automatic CRM changes, including record creation, task creation, contact detection, scheduled routines, and pipeline movement. <br>
Mitigation: Confirm the workflow, batch size, and whether writes are allowed before running; prefer first-page test runs for one-shot automations. <br>
Risk: CRM setup, reorganization, and pipeline movement can modify existing records or create new ones automatically. <br>
Mitigation: Review proposed changes, verify target records from prior reads, avoid duplicate records and tasks, and leave audit breadcrumbs for non-trivial automated decisions. <br>


## Reference(s): <br>
- [Breakcold CRM OpenClaw homepage](https://github.com/breakcold/mcp/tree/main/skills/breakcold-crm-openclaw) <br>
- [ClawHub Breakcold listing](https://clawhub.ai/matteoolefloch/breakcold-crm) <br>
- [Action 1 - Multichannel auto-task creation](references/action-tasks.md) <br>
- [Action 2 - Auto-movement of contacts in the pipeline](references/action-pipeline.md) <br>
- [Action 3 - Auto-report](references/action-reports.md) <br>
- [Action 4 - Prospect research](references/action-prospect-research.md) <br>
- [Action 5 - Contact detection and creation from the inbox](references/action-contact-detection.md) <br>
- [Action 6 - CRM setup and reorganization](references/action-crm-setup.md) <br>
- [Fundamentals](references/fundamentals.md) <br>
- [Routines and recap emails](references/routines.md) <br>
- [Breakcold branding](references/branding.md) <br>
- [Report design guide](references/report-design-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, text, markdown, code, configuration] <br>
**Output Format:** [Markdown guidance with CRM workflow steps, MCP tool-call examples, HTML report templates, and user-facing text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May cause an agent to read sensitive CRM and inbox data, create or update CRM records, create tasks and notes, move pipeline stages, and generate Breakcold-branded reports.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
