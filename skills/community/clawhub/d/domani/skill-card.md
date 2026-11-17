## Description:

Operate internet identity with Domani: search and acquire domains, configure DNS and hosting, create professional mailboxes, read or send email, inspect deliverability, manage webhooks, and grant scoped access to humans or agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gwendall](https://clawhub.ai/user/gwendall)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and agents use this skill to manage domains, DNS, professional mailboxes, email delivery, inbound webhooks, and scoped access through Domani workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server security summary flags use of an unpinned runtime authentication CLI.

Mitigation: Before authentication, review the package source and prefer a pinned Domani CLI version instead of an @latest command.

Risk: The server security summary says newly authenticated users can be steered into provider activation before their original task.

Mitigation: Require clear, current user authorization before mailbox creation, webhook configuration, purchases, DNS changes, email sends, or permission grants.

## Reference(s):

- [Domani Skill Page](https://clawhub.ai/gwendall/skills/domani)
- [Domain workflows](references/domains.md)
- [Professional email workflows](references/email.md)
- [Safety and authorization](references/safety.md)
- [Trust, ownership, privacy, and pricing](references/trust.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Text]

**Output Format:** [Markdown with inline shell commands and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose domain, DNS, mailbox, webhook, and email actions that require live tool results and explicit user authorization before execution.]

## Skill Version(s):

1.3.0 (source: server evidence release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
