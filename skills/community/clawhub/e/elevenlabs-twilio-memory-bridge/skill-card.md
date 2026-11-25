## Description:

Adds persistent caller memory and per-call context to ElevenLabs Conversational AI agents connected through Twilio.

This skill is ready for commercial/non-commercial use.

## Publisher:

[britrik](https://clawhub.ai/user/britrik)

### License/Terms of Use:

MIT

## Use Case:

Developers operating ElevenLabs voice agents through Twilio use this bridge to personalize incoming calls with caller-specific history, stored facts, and notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Caller names, stored memories, notes, and live call transcripts may be shared with ElevenLabs and the LLM configured on the agent, under each provider's own terms and retention policy.

Mitigation: Tell callers how their information is processed, obtain consent where required, and avoid storing sensitive personal details.

Risk: ClawScan reports a benign verdict with medium confidence and partial coverage; a malformed manifest and unresolved local references leave some evidence incomplete.

Mitigation: Review the package configuration and behavior before deployment, as recommended by the security guidance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/britrik/skills/elevenlabs-twilio-memory-bridge)
- [Project page listed in the artifact](https://github.com/britrik/elevenlabs-twilio-memory-bridge)

## Skill Output:

**Output Type(s):** [JSON, System prompt context, Dynamic variables]

**Output Format:** [JSON webhook response containing a personalized prompt override and call variables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated per inbound call from stored caller context and the configured personality template]

## Skill Version(s):

1.2.4 (source: SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
