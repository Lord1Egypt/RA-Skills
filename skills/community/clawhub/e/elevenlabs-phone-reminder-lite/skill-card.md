## Description:

Build AI phone call reminders with ElevenLabs Conversational AI + Twilio. Free starter guide.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daaab](https://clawhub.ai/user/daaab)

### License/Terms of Use:

MIT

## Use Case:

Developers and builders use this skill as a starter guide for configuring ElevenLabs Conversational AI with Twilio to place outbound AI reminder calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The guide involves sharing powerful Twilio credentials with ElevenLabs.

Mitigation: Use a dedicated Twilio subaccount or restricted credentials where possible, and rotate or revoke credentials after testing.

Risk: Outbound AI calls can create consent, privacy, billing, robocall, telemarketing, and call-recording obligations.

Mitigation: Only call recipients who have explicitly agreed to receive AI calls and check applicable rules for the deployment region before production use.

Risk: The Lite guide does not provide full scheduling, automation, error-handling, retry, or production hardening examples.

Mitigation: Review and extend the setup before operational deployment, including error handling, cost controls, and consent management.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/daaab/skills/elevenlabs-phone-reminder-lite)
- [ElevenLabs signup](https://try.elevenlabs.io/clawhub)
- [Twilio](https://twilio.com)
- [ElevenLabs Conversational AI create agent API](https://api.elevenlabs.io/v1/convai/agents/create)
- [ElevenLabs Conversational AI phone number API](https://api.elevenlabs.io/v1/convai/phone-numbers/create)
- [ElevenLabs Conversational AI outbound call API](https://api.elevenlabs.io/v1/convai/twilio/outbound-call)
- [Virtuals ACP premium agent](https://app.virtuals.io/acp/agents/u34u4m317ot8z5tgll3jpjkl)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash code blocks and API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires users to supply their own ElevenLabs and Twilio credentials.]

## Skill Version(s):

1.1.1 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
