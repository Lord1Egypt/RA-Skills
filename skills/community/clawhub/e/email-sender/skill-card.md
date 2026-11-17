## Description:

Send plain-text emails with optional file attachments through a Gmail SMTP account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elodyzen](https://clawhub.ai/user/elodyzen)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill when a workflow needs to send a report, log, message, or readable local file by email with a recipient, subject, body, and optional attachment path.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Embedded Gmail app password can expose the sender account if the skill package is shared or inspected.

Mitigation: Revoke and replace the embedded password before use, and store credentials in a protected secret store.

Risk: The tool can send any readable local file as an attachment when given an attachment path.

Mitigation: Require explicit user confirmation and restrict attachment paths to approved directories or file types.

Risk: Email can be sent to arbitrary recipients without a built-in approval step.

Mitigation: Add a confirmation gate that shows recipient, subject, body, and attachment details before sending.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/elodyzen/skills/email-sender)
- [Publisher Profile](https://clawhub.ai/user/elodyzen)

## Skill Output:

**Output Type(s):** [text, API Calls]

**Output Format:** [Plain-text send status returned by the email tool]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces an email delivery result string after attempting to send through SMTP.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
