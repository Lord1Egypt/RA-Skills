## Description:

Work with Microsoft Dynamics 365 CRM records, accounts, contacts, leads, opportunities, and activities - powered by ClawLink.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and CRM users use this skill to connect OpenClaw to Microsoft Dynamics 365 through ClawLink, discover available CRM tools, and work with records such as accounts, contacts, leads, opportunities, cases, invoices, and sales orders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access sensitive CRM data such as leads, invoices, opportunities, and sales orders.

Mitigation: Install only when ClawLink and the OpenClaw package source are trusted, and use a least-privileged Dynamics 365 account.

Risk: Create and update tools can modify Dynamics 365 CRM records.

Mitigation: Review CRM writes before confirming them and ensure the connected account has only the roles needed for the intended workflow.

## Reference(s):

- [Dynamics 365 Skill Page](https://clawhub.ai/hith3sh/skills/dynamics-365)
- [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=dynamics-365-crm)
- [ClawLink Dynamics 365 Dashboard](https://claw-link.dev/dashboard?add=dynamics-365)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance]

**Output Format:** [Markdown with inline shell and JavaScript code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides account pairing, integration setup, tool discovery, CRM read operations, and confirmed CRM write operations.]

## Skill Version(s):

1.0.5 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
