## Description: <br>
Run cold email sequences and manage sales outreach campaigns through the SalesBlink API, including lists, contacts, templates, senders, inbox replies, deliverability tests, reports, billing links, and API-key administration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sheksushant](https://clawhub.ai/user/sheksushant) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and sales operators use this skill to configure and operate SalesBlink outreach workflows from an agent, including creating contact lists, writing templates, connecting senders, launching sequences after confirmation, and checking campaign analytics. Developers can also use it to form SalesBlink API requests and payloads. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a powerful SalesBlink API key and can manage account, campaign, billing, and credential-administration actions. <br>
Mitigation: Configure SALESBLINK_API_KEY through a secure secret or environment setting, avoid pasting it into chat, and use a least-privilege key when SalesBlink supports one. <br>
Risk: Campaign launches can send email to many recipients and create persistent outreach activity. <br>
Mitigation: Create sequences paused by default and require explicit confirmation of recipients, sender accounts, templates, schedule, and stop conditions before launch. <br>
Risk: Billing links and Done-For-You domain or mailbox orders can affect payment methods or recurring costs. <br>
Mitigation: Require explicit approval for billing links and orders, including exact domains, mailbox counts, provider, price, and cancellation limits. <br>
Risk: Sender connection and API-key management actions can expose or revoke credentials. <br>
Mitigation: Confirm the exact sender, key, and downstream impact before connecting senders, refreshing keys, deleting keys, or changing credential settings. <br>
Risk: Bulk imports and campaign data can include private lead information. <br>
Mitigation: Upload only user-approved lead data and review CSV or contact payloads to avoid unrelated sensitive personal information. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/sheksushant/cold-email-salesblink) <br>
- [SalesBlink Public REST API base URL](https://run.salesblink.io/api/public/v1.0.0) <br>
- [SalesBlink API key settings](https://run.salesblink.io/account/integration/api) <br>
- [Lists](references/lists.md) <br>
- [Contacts and Leads](references/contacts.md) <br>
- [Email Templates](references/templates.md) <br>
- [Sequences](references/sequences.md) <br>
- [Email Senders and OAuth](references/senders.md) <br>
- [Inbox and Outreach](references/inbox.md) <br>
- [Workflow Examples](references/workflows.md) <br>
- [Billing and Payment Methods](references/billing.md) <br>
- [Done-For-You Domains and Mailboxes](references/dfy.md) <br>
- [API Key Management](references/api-keys.md) <br>
- [Inbox Placement Tests](references/inbox-placement.md) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with HTTP request examples, JSON payloads, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SALESBLINK_API_KEY and network access to run.salesblink.io.] <br>

## Skill Version(s): <br>
1.0.9 (source: server release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
