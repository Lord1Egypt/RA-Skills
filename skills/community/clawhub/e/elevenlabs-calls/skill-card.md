## Description:

Make AI phone calls using ElevenLabs Conversational AI and Twilio.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luke-deltadesk](https://clawhub.ai/user/luke-deltadesk)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to configure ElevenLabs Conversational AI agents, place outbound Twilio-backed phone calls, and retrieve conversation transcripts or audio for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can let an agent place outbound calls through the user's ElevenLabs and Twilio setup.

Mitigation: Require explicit approval before each outbound call and confirm the destination number, agent ID, and phone number ID.

Risk: Dynamic variables, transcripts, and recordings may contain personal or sensitive information.

Mitigation: Pass only necessary context, avoid unnecessary sensitive data, and handle retrieved conversation records according to applicable privacy requirements.

Risk: Calling and recording obligations vary by recipient location and use case.

Mitigation: Confirm consent and comply with applicable telecom and call-recording rules before use.

Risk: Outbound calls and conversation time can incur ElevenLabs and Twilio costs.

Mitigation: Use account limits, review call duration, and monitor provider billing during operation.

## Reference(s):

- [ElevenLabs Agents Platform Overview](https://elevenlabs.io/docs/agents-platform/overview)
- [ElevenLabs Agents Console](https://elevenlabs.io/app/agents)
- [ElevenLabs Phone Numbers Console](https://elevenlabs.io/app/agents/phone-numbers)
- [ClawHub Skill Page](https://clawhub.ai/luke-deltadesk/skills/elevenlabs-calls)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and script output from ElevenLabs API calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scripts may return JSON-derived summaries, transcripts, or audio bytes depending on the command used.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
