## Description: <br>
Build AI phone call reminders with ElevenLabs Conversational AI and Twilio. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dAAAb](https://clawhub.ai/user/dAAAb) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External developers and technical users use this skill as a setup guide for creating outbound AI phone reminders with ElevenLabs Conversational AI and Twilio. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Outbound phone calls can create consent, disclosure, recording, and calling-rule compliance obligations. <br>
Mitigation: Place calls only to recipients who have consented and confirm the use complies with applicable calling, disclosure, and recording rules. <br>
Risk: ElevenLabs API keys and Twilio credentials could be exposed if committed, logged, or shared. <br>
Mitigation: Protect API keys and auth tokens, avoid committing or logging secrets, and use a dedicated or restricted Twilio setup where possible. <br>
Risk: Phone-number rental and outbound calling can create unexpected billing charges. <br>
Mitigation: Monitor ElevenLabs and Twilio usage and billing, especially when enabling international calling. <br>
Risk: The Lite guide omits scheduling, automation, retry, and error-handling examples. <br>
Mitigation: Review and add production controls before relying on the setup for unattended reminders. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/dAAAb/elevenlabs-phone-reminder-lite) <br>
- [ElevenLabs signup](https://try.elevenlabs.io/clawhub) <br>
- [Twilio](https://twilio.com) <br>
- [ElevenLabs create agent endpoint](https://api.elevenlabs.io/v1/convai/agents/create) <br>
- [ElevenLabs phone number endpoint](https://api.elevenlabs.io/v1/convai/phone-numbers/create) <br>
- [ElevenLabs outbound call endpoint](https://api.elevenlabs.io/v1/convai/twilio/outbound-call) <br>
- [Virtuals ACP listing](https://app.virtuals.io/acp/agents/u34u4m317ot8z5tgll3jpjkl) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash and curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes credential placeholders for ElevenLabs and Twilio; does not execute calls by itself.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
