## Description: <br>
Email Sender Policy formats and sends Gmail messages by applying RFC 2047 subject encoding, Markdown-table-to-list conversion, RFC 822 plain-text formatting, and Maton/Gmail delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sean810720](https://clawhub.ai/user/sean810720) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to prepare plain-text outbound email with consistent subject encoding, table conversion, newsletter formatting, and Gmail sending through an active Maton connection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send live email through the connected Maton/Gmail account without an enforced confirmation step. <br>
Mitigation: Use --test or a draft/preview workflow before sending, and verify To, CC, BCC, subject, body, and the active Gmail connection. <br>
Risk: Message content and recipients are processed through Maton/Gmail when real sends are executed. <br>
Mitigation: Avoid regulated or confidential content unless that processing is acceptable for the user's environment and policies. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sean810720/email-sender-policy) <br>
- [Maton settings](https://maton.ai/settings) <br>
- [Maton connections](https://ctrl.maton.ai/connections) <br>
- [Maton Gmail send endpoint](https://gateway.maton.ai/google-mail/gmail/v1/users/me/messages/send) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, API Calls, Configuration] <br>
**Output Format:** [Plain-text email content, RFC 822 preview output, and send-status text with message identifiers] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js, MATON_API_KEY, and an active Maton Google Mail connection; --test previews the RFC 822 message without sending.] <br>

## Skill Version(s): <br>
2.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
