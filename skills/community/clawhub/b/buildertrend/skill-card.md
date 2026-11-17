## Description:

Complete Buildertrend automation via Browser Relay, with 43 playbooks covering sales, project management, financials, scheduling, change orders, daily logs, RFIs, punch lists, invoicing, and procurement without using a public API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elevateson](https://clawhub.ai/user/elevateson)

### License/Terms of Use:

MIT

## Use Case:

Construction teams and operations staff use this skill to guide an agent through Buildertrend workflows in an attached browser session. It supports project setup, sales pipeline tasks, client and vendor coordination, financial workflows, reporting, scheduling, and closeout procedures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide live business actions in Buildertrend, including financial updates, recurring report delivery, cloud folder changes, reminders, and agent configuration changes.

Mitigation: Start with a dedicated test Buildertrend project and require explicit per-action approval before any live financial, reporting, cloud-storage, reminder, or configuration change.

Risk: Some playbooks include approval-on-behalf and e-signature steps that may require organizational authorization.

Mitigation: Remove or disable approval-on-behalf and e-signature steps unless the organization has a documented authorization policy for those actions.

Risk: Browser automation can act on the wrong project or stale page state if the session changes or the UI does not match expectations.

Mitigation: Use the documented snapshot, read, act, and verify pattern before each action, and stop for user guidance when login, loading, modal, or element identity checks fail.

## Reference(s):

- [ClawHub Buildertrend Skill Listing](https://clawhub.ai/elevateson/skills/buildertrend)
- [Buildertrend Skill Instructions](artifact/SKILL.md)
- [Buildertrend Skill README](artifact/README.md)
- [Buildertrend Playbook Index](artifact/playbooks/README.md)
- [Browser Relay UI Patterns](artifact/bt-ui-patterns.md)
- [QuickBooks Online Sync Guide](artifact/qbo-sync-guide.md)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [Buildertrend Help Articles](https://buildertrend.com/help-articles/)
- [Buildertrend Job Management Help](https://buildertrend.com/help-article/job-management/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, checklists, tables, and structured action summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an authenticated Buildertrend browser session through OpenClaw Browser Relay; financial and administrative actions should be reviewed before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
