## Description:

Email Sender Policy formats outbound email by encoding subjects with UTF-8 Base64, converting Markdown tables into readable lists, building RFC 822 plain-text messages, and sending through the current Gmail connection via Maton.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sean810720](https://clawhub.ai/user/sean810720)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to apply consistent outbound email formatting and send Gmail messages from automated workflows. It is suited for plain-text notices, reports, and newsletters that need RFC-compatible subject encoding and table-to-list conversion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send email from an account-linked Gmail connection without a separate confirmation step.

Mitigation: Use --test first and require human review of the rendered message before allowing live sends from sensitive or business Gmail accounts.

Risk: Weak recipient-header validation could allow unintended recipients or Bcc values if recipient strings are untrusted.

Mitigation: Only pass trusted recipient, Cc, and Bcc values; verify every recipient before sending.

Risk: Email content and credentials route through Maton/Gmail using MATON_API_KEY.

Mitigation: Install only where routing email content through Maton/Gmail is acceptable and protect MATON_API_KEY as a sending credential.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sean810720/skills/email-sender-policy)
- [Maton account settings](https://maton.ai/settings)
- [Maton connection management](https://ctrl.maton.ai/connections)
- [Maton Gmail send endpoint](https://gateway.maton.ai/google-mail/gmail/v1/users/me/messages/send)

## Skill Output:

**Output Type(s):** [API Calls, Text, Markdown, Shell commands, Configuration]

**Output Format:** [RFC 822 plain-text email sent through Gmail/Maton, with CLI status output and formatted message text in test mode]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MATON_API_KEY and an active google-mail OAuth connection; supports a test mode that prints the formatted message without sending.]

## Skill Version(s):

2.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
