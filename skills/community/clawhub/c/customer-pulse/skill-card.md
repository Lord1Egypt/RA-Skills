## Description:

Customer Pulse is a lightweight CRM assistant for managing customer records, recording follow-ups, tracking sales funnels, and flagging churn risk.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hanjing5024064](https://clawhub.ai/user/hanjing5024064)

### License/Terms of Use:

MIT-0

## Use Case:

Sales teams and individual CRM users use this skill to maintain a local customer ledger, record follow-up activity, review sales pipeline status, and identify customers that may need attention.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores customer names, phone numbers, budgets, and follow-up notes in plaintext local files.

Mitigation: Protect the configured data directory, restrict local file access, and avoid placing sensitive customer details in shared workspaces.

Risk: CSV export can create portable copies of customer personal and commercial data.

Mitigation: Export only when needed, store exported files securely, and avoid sending raw exported customer data into chat output.

Risk: Deletion actions can remove customer records from the local ledger.

Mitigation: Confirm deletion intent and identifiers before asking the agent to remove records.

## Reference(s):

- [CRM practice guide](references/crm-guide.md)
- [ClawHub skill page](https://clawhub.ai/hanjing5024064/skills/customer-pulse)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Chinese conversational responses with Markdown tables, JSON-backed local file operations, and shell command invocations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses optional CP_SUBSCRIPTION_TIER and CP_DATA_DIR environment variables; customer data is stored in local JSON files.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
