## Description:

Helps agents list DuoPlus cloud numbers, read SMS messages, check packages, and manage purchases, renewals, and auto-renewal through the DuoPlus API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[duoplusofficial](https://clawhub.ai/user/duoplusofficial)

### License/Terms of Use:

MIT-0

## Use Case:

DuoPlus customers and their agents use this skill to retrieve cloud-number SMS messages, inspect available packages, and manage cloud-number billing actions with explicit confirmation.

### Deployment Geography for Use:

Global; use the mainland China API endpoint for mainland China deployments.

## Known Risks and Mitigations:

Risk: SMS verification messages and API credentials contain sensitive information.

Mitigation: Limit access to intended users and tasks; avoid echoing or storing the API key and handle SMS messages discreetly.

Risk: Purchases, renewals, and enabling auto-renewal can incur charges.

Mitigation: Review the current package and billing details and obtain explicit approval before confirming each action; do not automatically retry billing requests.

Risk: An untrusted API base override could send credentials to a third party.

Mitigation: Use only the official DuoPlus global or mainland China API domains for the deployment.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/duoplusofficial/skills/duoplus-cloud-number)
- [DuoPlus Cloud Number API reference](references/api.md)
- [DuoPlus API documentation](https://help.duoplus.net/docs/4D2HCXVy)

## Skill Output:

**Output Type(s):** [Text, Guidance, Shell commands]

**Output Format:** [Markdown guidance with shell commands and JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Purchase and renewal previews require explicit approval before an order is placed.]

## Skill Version(s):

1.0.0 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
