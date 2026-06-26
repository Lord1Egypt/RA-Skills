## Description: <br>
Self-hosted SMS via Android phone HTTP API. Use when you need to send/receive SMS messages using an Android device as a gateway. Supports popular SMS Gateway apps (SMS Gateway API, SMSGate, etc.). Ideal for security teams wanting full control without third-party SMS providers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[NadjiHamid](https://clawhub.ai/user/NadjiHamid) <br>

### License/Terms of Use: <br>
Apache-2.0 <br>


## Use Case: <br>
Developers, security teams, and operators use this skill to send, receive, and monitor SMS messages through an Android phone gateway instead of a third-party SMS provider. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send, read, and forward real SMS messages, including sensitive messages such as OTPs or personal data. <br>
Mitigation: Install and use it only when SMS gateway access is intended, and limit access to trusted agents, users, devices, and workflows. <br>
Risk: Gateway credentials can be exposed through shared files, repositories, shell history, or transcripts. <br>
Mitigation: Store credentials in protected config files or a secrets manager, keep them out of shared materials, and rotate credentials if exposure is suspected. <br>
Risk: Cloud mode or externally exposed endpoints add a third-party or public-network trust boundary. <br>
Mitigation: Prefer local or private HTTPS endpoints where possible, use cloud mode only after accepting that trust boundary, and register webhooks only to endpoints you control. <br>


## Reference(s): <br>
- [API Reference](references/api_reference.md) <br>
- [capcom6/android-sms-gateway Quick Reference](references/capcom6_reference.md) <br>
- [SMS Gateway API](https://github.com/itsmeichigo/SMSGateway) <br>
- [SMSGate](https://github.com/iamsmgate/smsgate) <br>
- [SMS Forwarder](https://github.com/pppscn/SmsForwarder) <br>
- [capcom6/android-sms-gateway](https://github.com/capcom6/android-sms-gateway) <br>
- [capcom6 Private Server Documentation](https://docs.sms-gate.app/getting-started/private-server/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, API calls] <br>
**Output Format:** [Markdown with inline shell commands, JSON configuration examples, and API request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce commands that send, read, or forward real SMS messages through a configured Android gateway.] <br>

## Skill Version(s): <br>
2.0.0 (source: package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
