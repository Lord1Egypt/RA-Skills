## Description:

Bridge Twilio phone calls to Google Gemini Live API for real-time AI voice conversations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[quantdeveloperusa](https://clawhub.ai/user/quantdeveloperusa)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to run a phone bridge that connects Twilio voice calls to Gemini Live for real-time AI audio conversations, including inbound and outbound call flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bridge exposes internet-facing phone-call and live-audio paths.

Mitigation: Run it only behind strong authentication, Twilio signature validation, trusted-host enforcement, and rate limits.

Risk: Outbound calling can contact unintended destinations if it is not scoped.

Mitigation: Use destination and caller-ID allowlists and explicitly configure PUBLIC_URL, TWILIO_ACCOUNT_SID, and TWILIO_FROM before deployment.

Risk: Live audio and optional recording can create privacy and consent obligations.

Mitigation: Define clear consent, retention, and privacy handling before enabling production traffic or recordings.

Risk: Unpinned dependencies can change behavior after deployment.

Mitigation: Pin Python dependencies and review updates before redeploying.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/quantdeveloperusa/skills/gemini-live-phone)
- [Publisher profile](https://clawhub.ai/user/quantdeveloperusa)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands, endpoint examples, and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runtime use depends on Google Gemini API credentials, Twilio credentials, and an internet-accessible webhook/WebSocket endpoint.]

## Skill Version(s):

1.0.1 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
