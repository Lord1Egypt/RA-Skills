## Description: <br>
Domains and emails for AI agents: search, register, and manage domains; create mailboxes; and send and receive email. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gwendall](https://clawhub.ai/user/gwendall) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to let an agent search and purchase domains, configure DNS and hosting records, transfer or renew domains, and manage Domani mailboxes and messages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad authority over a Domani account, including DNS, billing, tokens, and email. <br>
Mitigation: Install only when the agent should manage the account, keep the token private, and use a least-privilege token where possible. <br>
Risk: Domain purchases, transfers, renewals, DNS or nameserver changes, mailbox deletion, email forwarding, inbound webhooks, token changes, and account deletion can have financial or operational impact. <br>
Mitigation: Require explicit user confirmation before performing those sensitive actions. <br>


## Reference(s): <br>
- [Domani homepage](https://domani.run) <br>
- [Domani ClawHub listing](https://clawhub.ai/gwendall/domani) <br>
- [Email Reference](references/email.md) <br>
- [Recipes Reference](references/recipes.md) <br>
- [Transfer Reference](references/transfer.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline curl commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses DOMANI_API_KEY for authenticated account actions and public API calls for read-only discovery.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
