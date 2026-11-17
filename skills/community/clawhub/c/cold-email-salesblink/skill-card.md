## Description:

Automates SalesBlink cold email outreach by helping agents manage sequences, contacts, templates, senders, inbox replies, deliverability tests, reports, and SalesBlink API requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sheksushant](https://clawhub.ai/user/sheksushant)

### License/Terms of Use:

MIT-0

## Use Case:

Sales, growth, and developer users use this skill to operate SalesBlink outreach workflows through an agent, including lead list management, campaign setup, sender configuration, inbox handling, analytics, deliverability checks, billing-sensitive operations, and API-key administration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive SalesBlink API keys, signup credentials, or sender passwords could be exposed if pasted into chat or logs.

Mitigation: Configure SALESBLINK_API_KEY through the platform secret or environment mechanism, avoid placing passwords in chat, and review OAuth/provider permissions before connecting senders.

Risk: The skill can send cold email campaigns, import lead data, and interact with replies, which may affect recipients and process personal data.

Mitigation: Require explicit user review of approved lead lists, sender accounts, templates, schedule, stop conditions, and estimated recipient count before imports or campaign launches.

Risk: Billing, DFY domain/mailbox orders, and API-key administration can create costs or disrupt integrations.

Mitigation: Require explicit confirmation of exact domains, mailbox counts, provider, price, card action, key name or ID, and integration impact before executing those actions.

Risk: Persistent or evergreen campaigns may continue sending beyond the user's intended scope.

Mitigation: Create sequences paused by default, default to non-evergreen campaigns, document stop conditions, and periodically audit active or recurring items.

## Reference(s):

- [SalesBlink public API base URL](https://run.salesblink.io/api/public/v1.0.0)
- [SalesBlink API key settings](https://run.salesblink.io/account/integration/api)
- [Skill source](artifact/SKILL.md)
- [Lists](artifact/references/lists.md)
- [Contacts and Leads](artifact/references/contacts.md)
- [Email Templates](artifact/references/templates.md)
- [Sequences](artifact/references/sequences.md)
- [Email Senders and OAuth](artifact/references/senders.md)
- [Inbox and Outreach](artifact/references/inbox.md)
- [Activity Tracking](artifact/references/activity.md)
- [Reports](artifact/references/reports.md)
- [Inbox Placement Tests](artifact/references/inbox-placement.md)
- [Done-For-You Domains and Mailboxes](artifact/references/dfy.md)
- [Billing and Payment Methods](artifact/references/billing.md)
- [API Key Management](artifact/references/api-keys.md)
- [Organization Users and Workspaces](artifact/references/organization.md)
- [Folders](artifact/references/folders.md)
- [Account Config](artifact/references/account-config.md)
- [Workflow Examples](artifact/references/workflows.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON payloads, HTTP examples, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SALESBLINK_API_KEY and network access to run.salesblink.io for live API operations.]

## Skill Version(s):

1.0.9 (source: server release metadata; artifact SKILL.md frontmatter is 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
