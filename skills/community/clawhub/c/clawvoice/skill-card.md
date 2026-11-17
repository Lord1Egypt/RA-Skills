## Description:

ClawVoice gives OpenClaw agents phone calling and SMS workflows with guided setup, voice-provider configuration, batch calling, and post-call outcome capture.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neocody](https://clawhub.ai/user/neocody)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use ClawVoice to let an agent place and receive PSTN calls, send SMS messages, run batch call workflows, and capture post-call summaries and transcripts. It is intended for telephony automation where users provide provider credentials, public webhook endpoints, and compliance decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Provider API keys and telephony auth tokens are required for setup and could be exposed if pasted into chat or stored insecurely.

Mitigation: Use the local setup wizard or environment/config secrets for credentials, and avoid sharing provider keys or tokens in agent conversation.

Risk: Call transcripts, summaries, and campaign reports may contain sensitive personal or business information and can be stored locally or sent to notification services.

Mitigation: Disable transcript notification or export features when not needed, protect the voice-memory workspace, and review Telegram, Discord, or Slack recipients before enabling notifications.

Risk: Voice calls and SMS messages are untrusted input channels that may try to influence agent memory or follow-up actions.

Mitigation: Keep restricted tools enabled, set mainMemoryAccess to none for sensitive workspaces, and require explicit review before promoting voice memories to main memory.

Risk: Inbound webhooks and media streams require public endpoints that expose a local service to external traffic.

Mitigation: Avoid inbound public exposure until needed, use webhook signing secrets where available, run diagnostics before calls, and configure only real HTTPS/WSS tunnel URLs.

Risk: Automated calling, SMS, and batch campaigns can create consent, telemarketing, and carrier-registration obligations.

Mitigation: Confirm consent and applicable TCPA, state, and A2P 10DLC requirements before using outbound calling or SMS campaign features.

## Reference(s):

- [ClawHub ClawVoice listing](https://clawhub.ai/neocody/skills/clawvoice)
- [ClawVoice website](https://clawvoice.io)
- [npm package: clawvoice](https://www.npmjs.com/package/clawvoice)
- [OpenClaw voice-call plugin docs](https://docs.openclaw.ai/plugins/voice-call)
- [Twilio A2P 10DLC messaging guide](https://www.twilio.com/docs/messaging/guides/10dlc)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance and plain-text tool responses with structured data, inline shell commands, and CSV campaign reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include call status, SMS status, summaries, transcripts, generated CSV paths, setup instructions, and configuration values.]

## Skill Version(s):

1.1.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
