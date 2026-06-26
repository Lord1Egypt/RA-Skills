## Description: <br>
Find accommodation contact details and run AI-assisted booking calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[arein](https://clawhub.ai/user/arein) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Travelers, assistants, and developers use this skill to find public contact details for accommodation listings and run AI-assisted calls for booking, reservation, cancellation, or negotiation tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place real AI phone calls that may disclose personal data or affect bookings, cancellations, or reservations. <br>
Mitigation: Use test numbers first and require explicit confirmation before booking, cancelling, or sharing personal data. <br>
Risk: The skill may expose a local webhook endpoint through ngrok and send audio, transcripts, and booking details to third-party AI and telephony providers. <br>
Mitigation: Restrict and rotate API keys, protect the config directory and logs, review provider data handling, and avoid sensitive healthcare or financial calls. <br>
Risk: Provider usage can incur telephony, speech, voice, tunnel, or model charges. <br>
Mitigation: Set billing limits, monitor quotas and balances, and verify call preflight results before dialing. <br>


## Reference(s): <br>
- [Travel Concierge README](README.md) <br>
- [Travel Concierge Skill](SKILL.md) <br>
- [Voice Call Setup Guide](CALL-SETUP.md) <br>
- [Phone Call Skill](skills/phone-call/SKILL.md) <br>
- [Twilio Console](https://console.twilio.com) <br>
- [Deepgram Console](https://console.deepgram.com/signup) <br>
- [ElevenLabs Sign Up](https://elevenlabs.io/sign-up) <br>
- [Anthropic Console](https://console.anthropic.com) <br>
- [ngrok](https://ngrok.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and optional JSON CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide calls that use local configuration, provider API keys, a local webhook tunnel, and provider billing.] <br>

## Skill Version(s): <br>
1.5.0 (source: server release metadata; artifact frontmatter lists 1.3.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
