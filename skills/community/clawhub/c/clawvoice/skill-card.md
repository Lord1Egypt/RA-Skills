## Description: <br>
ClawVoice lets OpenClaw agents place and receive phone calls, send SMS, guide telephony and voice-provider setup, and capture post-call outcomes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[neocody](https://clawhub.ai/user/neocody) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use ClawVoice to connect an agent to Twilio or Telnyx phone service, run inbound and outbound voice or SMS workflows, and receive summaries, transcripts, or campaign reports after calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can call and text real phone numbers, including batch campaigns. <br>
Mitigation: Require explicit user approval before outbound calls, texts, or campaigns, keep daily and per-call limits enabled, and review consent, recording, retention, and automated-calling requirements before use. <br>
Risk: The setup flow needs provider API keys, auth tokens, phone numbers, and voice-service credentials. <br>
Mitigation: Enter secrets through the local setup wizard, environment variables, or a secret manager instead of chat, and rotate any credential that was shared in conversation. <br>
Risk: Inbound calls, SMS, webhooks, and media streams expose a reachable service. <br>
Mitigation: Keep tunnel exposure narrow, use provider webhook verification or webhook secrets where supported, avoid placeholder URLs, and run diagnostics before placing calls. <br>
Risk: Call transcripts, summaries, and notifications can contain personal or sensitive information. <br>
Mitigation: Disable transcript forwarding and SMS auto-reply unless needed, limit transcript retention, and review post-call destinations such as Telegram, Discord, or Slack. <br>


## Reference(s): <br>
- [ClawVoice ClawHub page](https://clawhub.ai/neocody/clawvoice) <br>
- [ClawVoice website](https://clawvoice.io) <br>
- [OpenClaw voice-call plugin documentation](https://docs.openclaw.ai/plugins/voice-call) <br>
- [Twilio A2P 10DLC guidance](https://www.twilio.com/docs/messaging/guides/10dlc) <br>
- [Cloudflare Tunnel WebSocket issue referenced by the artifact](https://github.com/cloudflare/cloudflared/issues/1465) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and text guidance with CLI commands, configuration values, call or SMS status, transcripts, summaries, and CSV campaign reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May initiate real phone calls and SMS through configured providers; outputs can include call transcripts and post-call notifications.] <br>

## Skill Version(s): <br>
1.1.3 (source: server release metadata; artifact package metadata lists 1.1.2 and plugin manifest lists 1.0.4) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
