## Description:

Interact with the Fibek B2B collections platform API to manage invoices, clients, payment agreements, campaigns, and financial metrics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fibekdev](https://clawhub.ai/user/fibekdev)

### License/Terms of Use:

MIT-0

## Use Case:

Collections, finance, and operations teams use this skill to authenticate to Fibek, review receivables, inspect client and invoice status, create payment agreements, send reminders or statements, and monitor portfolio KPIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles credentials and long-lived bearer tokens.

Mitigation: Require secure token storage and clearing, and re-authenticate users when authorization fails.

Risk: The skill accesses sensitive financial, client, and contact data.

Mitigation: Deploy only with the legitimate HTTPS Fibek API pinned in FIBEK_BASE_URL and restrict network egress.

Risk: The skill can initiate outbound reminders, account statements, and campaign communications.

Mitigation: Require user review of recipients, channels, and campaign audiences before any message or campaign is sent.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fibekdev/skills/fibek-cleo)
- [Publisher profile](https://clawhub.ai/user/fibekdev)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, shell commands, configuration, guidance]

**Output Format:** [Spanish natural-language responses with numbered Markdown blocks, API request guidance, and occasional shell commands for endpoint discovery.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires FIBEK_BASE_URL and per-user authentication; should not expose raw JSON, internal IDs, or infrastructure details to end users.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
