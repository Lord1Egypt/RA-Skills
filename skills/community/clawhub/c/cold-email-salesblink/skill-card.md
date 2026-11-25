## Description:

Run cold email sequences on autopilot and manage full sales outreach campaigns via the SalesBlink API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sheksushant](https://clawhub.ai/user/sheksushant)

### License/Terms of Use:

MIT-0

## Use Case:

Sales teams and operators use this skill to manage contacts, senders, templates, and multi-step outreach campaigns through SalesBlink, then monitor replies and delivery activity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Contact imports may transfer contact details to SalesBlink.

Mitigation: Review imported fields and recipient scope before submitting an import.

Risk: Activating a campaign can schedule real outreach.

Mitigation: Review recipients, message content, sender accounts, and schedule before activation.

Risk: The security scan was partial, with two local references unresolved.

Mitigation: Review the lead-import and campaign examples and check any unresolved references before use.

## Reference(s):

- [SalesBlink Public API](https://run.salesblink.io/api/public/v1.0.0)
- [SalesBlink API key settings](https://run.salesblink.io/account/integration/api)
- [Campaign workflow examples](artifact/references/workflows.md)
- [Contacts and leads reference](artifact/references/contacts.md)
- [Sequences reference](artifact/references/sequences.md)
- [Email senders reference](artifact/references/senders.md)

## Skill Output:

**Output Type(s):** [Guidance, Configuration, Text]

**Output Format:** [Markdown guidance with HTTP examples and JSON request or response data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May initiate contact imports or scheduled outreach in SalesBlink when configured and authorized.]

## Skill Version(s):

1.2.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
