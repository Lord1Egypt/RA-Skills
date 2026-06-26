## Description: <br>
Complete Buildertrend automation via Browser Relay - 43 playbooks covering sales, project management, financials, scheduling, change orders, daily logs, RFIs, punch lists, invoicing, procurement, with no API required. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[elevateson](https://clawhub.ai/user/elevateson) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Construction operations teams and their agents use this skill to operate Buildertrend through Browser Relay for project setup, client communication, financial workflows, scheduling, documents, and QuickBooks Online reconciliation. The skill is intended for logged-in Buildertrend users who want guided browser automation rather than API-based integration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create or change financial records and sync items to QuickBooks Online. <br>
Mitigation: Test on a non-production project first and require explicit confirmation for every accounting or external-system action. <br>
Risk: Browser control of a logged-in Buildertrend account can modify live project and business data. <br>
Mitigation: Use the skill only with an authenticated user session, verify the page state before each action, and review each proposed change before execution. <br>
Risk: The skill may store project data in local memory, Google Drive, Reminders, or other agent workspaces. <br>
Mitigation: Confirm storage destinations before use, minimize sensitive data retention, and review workspace sharing and retention settings. <br>


## Reference(s): <br>
- [Buildertrend OpenClaw Skill Homepage](https://github.com/elevateson/buildertrend-openclaw) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>
- [Buildertrend Help Center](https://buildertrend.com/help-articles/) <br>
- [Buildertrend Job Management Help](https://buildertrend.com/help-article/job-management/) <br>
- [Playbook Index](playbooks/README.md) <br>
- [Buildertrend UI Patterns](bt-ui-patterns.md) <br>
- [QuickBooks Online Sync Guide](qbo-sync-guide.md) <br>
- [Buildertrend Workflows](workflows.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown playbooks with browser-action checklists, inline shell commands, and optional JSON or Markdown tables for extracted Buildertrend data.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an authenticated Buildertrend browser session through OpenClaw Browser Relay; financial and accounting actions should require explicit user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
