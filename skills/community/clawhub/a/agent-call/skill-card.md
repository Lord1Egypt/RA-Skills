## Description: <br>
Agent Call enables AI agents to place Twilio-powered outbound calls, send SMS notifications, and check call status from shell workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kieferhuan](https://clawhub.ai/user/kieferhuan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add phone-call and SMS workflows to an agent, including appointment reminders, urgent notifications, lead follow-up, call-status checks, and optional call recording or transcription through Twilio. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can contact real people by phone or SMS and can spend Twilio funds. <br>
Mitigation: Require explicit confirmation for every outbound call, SMS, or batch; use recipient allowlists where possible and enforce Twilio spend and rate limits. <br>
Risk: Twilio Account SID, Auth Token, phone numbers, call details, recordings, and transcripts are sensitive operational or personal data. <br>
Mitigation: Store credentials in an approved secret manager or tightly permissioned environment, use a restricted Twilio subaccount, avoid committing config files, and limit access to call artifacts. <br>
Risk: Recording or transcribing calls can create consent, retention, and privacy obligations. <br>
Mitigation: Keep recording and transcription disabled unless the caller consent, jurisdictional requirements, retention policy, and access controls are approved for the use case. <br>
Risk: Server security guidance identifies an unsafe message-handling bug in make-call.sh. <br>
Mitigation: Do not pass untrusted message text to make-call.sh until command construction is fixed; sanitize inputs and prefer safe API parameter construction before enabling untrusted or automated message sources. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kieferhuan/agent-call) <br>
- [Publisher profile](https://clawhub.ai/user/kieferhuan) <br>
- [Twilio Voice documentation](https://www.twilio.com/docs/voice) <br>
- [Artifact documentation](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Markdown and terminal-oriented guidance with shell commands, JSON credential configuration examples, and Twilio API-backed call or message status output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Twilio credentials and a Twilio phone number; outbound calls, SMS, recording, and transcription can incur provider charges and expose sensitive call data.] <br>

## Skill Version(s): <br>
1.0.8 (source: server release evidence and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
