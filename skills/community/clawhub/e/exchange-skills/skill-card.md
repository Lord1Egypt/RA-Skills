## Description: <br>
Manages Microsoft Exchange/Outlook email, calendar, contacts, tasks, and notes for an agent through a terminal CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[derekhsu](https://clawhub.ai/user/derekhsu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees or agents acting for a mailbox owner use this skill to list, read, reply to, mark, and archive Exchange/Outlook emails and to inspect calendar events, contacts, tasks, and notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make broad mailbox changes, including batch archive and mark-read operations. <br>
Mitigation: List the affected messages first and avoid batch commands unless the mailbox owner has confirmed the exact scope. <br>
Risk: Exchange credentials may be exposed if environment variables or a local .env file are handled carelessly. <br>
Mitigation: Keep any .env file private and out of source control, and use only Exchange accounts appropriate for mailbox-management access. <br>
Risk: Disabling SSL verification can weaken transport security. <br>
Mitigation: Leave SSL verification enabled unless an approved corporate certificate workflow requires EXCHANGE_DISABLE_SSL_VERIFY=1. <br>
Risk: The security summary notes that archive behavior may move mail to Deleted Items without clear warning. <br>
Mitigation: Verify or clearly accept archive behavior before relying on it for cleanup workflows. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/derekhsu/exchange-skills) <br>
- [Publisher profile](https://clawhub.ai/user/derekhsu) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration] <br>
**Output Format:** [Terminal text or JSON, with markdown command examples and configuration guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Exchange connection environment variables and can read or mutate mailbox state through reply, mark-read, and archive commands.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
