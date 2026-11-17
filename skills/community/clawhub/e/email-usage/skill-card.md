## Description:

Uses local mail server scripts to send email, read recent inbox headers, and create mailbox accounts for a managed domain.

This skill is ready for commercial/non-commercial use.

## Publisher:

[axelhu](https://clawhub.ai/user/axelhu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and mail administrators use this skill to operate a local domain mail server by sending messages, reading recent inbox headers, and creating mailbox accounts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles mailbox passwords for SMTP and IMAP workflows.

Mitigation: Install only in a controlled mail-admin environment and revise password handling to use secure prompts or managed secrets before broader deployment.

Risk: The skill can create persistent mailbox accounts through Docker access.

Mitigation: Restrict account creation to an admin-only workflow and verify Docker permissions before use.

Risk: SMTP authentication errors may not stop the send workflow.

Mitigation: Revise the send workflow to fail closed on authentication errors before using it outside a trusted network.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/axelhu/skills/email-usage)
- [Publisher profile](https://clawhub.ai/user/axelhu)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash commands and plain-text script output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires access to a local mail server and Docker for mailbox account creation.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact _meta.json reports 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
