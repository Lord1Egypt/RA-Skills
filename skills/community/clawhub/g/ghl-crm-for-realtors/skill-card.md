## Description: <br>
Use this skill for GoHighLevel CRM work for realtors: contact lookup and updates, opportunity and pipeline actions, conversation messaging, calendar slots, and workflow enrollment using GoHighLevel API v2. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[danielfoch](https://clawhub.ai/user/danielfoch) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External realtor teams and their agents use this skill to connect an assistant to GoHighLevel for lead intake, contact management, pipeline tracking, follow-up messaging, calendar availability, and workflow enrollment. It is intended for live CRM assistance when the user has valid GoHighLevel credentials and clear authorization for the account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use a GoHighLevel private integration token to access live CRM data and perform account actions. <br>
Mitigation: Use a least-privilege sub-account token, keep the token out of chat output, and rotate or revoke it if exposure is suspected. <br>
Risk: Write operations can send messages, change contacts, create appointments, enroll workflows, delete records, or otherwise make real business changes. <br>
Mitigation: Require explicit user confirmation before any live POST, PUT, or DELETE action and review the target record IDs before execution. <br>
Risk: CRM records may contain personal, lead, or customer communication data. <br>
Mitigation: Limit queries to the needed contacts or opportunities and avoid exposing unnecessary CRM response data in assistant output. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/danielfoch/ghl-crm-for-realtors) <br>
- [Contacts API Reference](references/contacts.md) <br>
- [Opportunities & Pipelines API Reference](references/opportunities.md) <br>
- [Conversations & Messaging API Reference](references/conversations.md) <br>
- [Calendars & Appointments API Reference](references/calendars.md) <br>
- [Troubleshooting Reference](references/troubleshooting.md) <br>
- [GoHighLevel API base](https://services.leadconnectorhq.com) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls, Markdown] <br>
**Output Format:** [Markdown with inline shell commands and JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce live GoHighLevel API requests when credentials are configured and the user confirms write actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
