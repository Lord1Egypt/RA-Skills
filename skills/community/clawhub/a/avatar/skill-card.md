## Description:

Interactive AI avatar with Simli video rendering and ElevenLabs TTS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johannes-berggren](https://clawhub.ai/user/johannes-berggren)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use Avatar to run a local interactive AI avatar frontend that speaks concise responses, renders lip-synced video, and shows detailed Markdown output for OpenClaw-style agent responses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill exposes powerful agent, messaging, and provider-key capabilities with weak access controls.

Mitigation: Run it only on a trusted local machine, bind the server to localhost, and add authentication before exposing any port.

Risk: Slack, email, and Stream Deck actions can send or forward generated content when enabled.

Mitigation: Keep those integrations disabled until confirmations and recipient limits are configured.

Risk: Provider API keys may be exposed during testing or misconfiguration.

Mitigation: Store required keys in environment-backed configuration, rotate any exposed Simli key, and review provider-key handling before deployment.

Risk: Unpinned or outdated dependencies can increase deployment risk.

Mitigation: Update and pin dependencies before production use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/johannes-berggren/skills/avatar)
- [ClawHub Publisher Profile](https://clawhub.ai/user/johannes-berggren)
- [Simli](https://simli.com)
- [ElevenLabs](https://elevenlabs.io)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Structured text with <spoken> and <detail> sections; detail may contain Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Spoken text is intended for TTS, while detail text is intended for the avatar detail panel.]

## Skill Version(s):

1.0.0 (source: evidence.release.version and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
