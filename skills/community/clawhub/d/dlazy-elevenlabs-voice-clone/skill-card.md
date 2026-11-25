## Description:

Creates an ElevenLabs Instant Voice Clone from a clean voice sample for use with ElevenLabs text-to-speech.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators provide a clean voice sample to create a custom voice with ElevenLabs Instant Voice Cloning for TTS narration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports medium confidence and incomplete evidence, including an unresolved CLI package reference and an unclear connection between the voice-cloning purpose and the login command.

Mitigation: Review and decide whether you trust the CLI and its login flow before installing; investigate the package and login behavior if those details matter to your use.

Risk: Local audio files supplied to the skill are uploaded to dLazy media storage, and request parameters are sent to its hosted API.

Mitigation: Only submit audio and accompanying information that you are comfortable sending to the dLazy service.

## Reference(s):

- [ClawHub release](https://clawhub.ai/dlazyai/skills/dlazy-elevenlabs-voice-clone)
- [Publisher profile](https://clawhub.ai/user/dlazyai)
- [dLazy CLI package](https://www.npmjs.com/package/@dlazy/cli)
- [dLazy service](https://dlazy.com)
- [dLazy API key settings](https://dlazy.com/dashboard/organization/api-key)
- [CLI homepage listed in skill metadata](https://github.com/dlazy-ai/cli)

## Skill Output:

**Output Type(s):** [Audio, JSON]

**Output Format:** [JSON API response with generated voice output details and hosted result URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Voice generation may run asynchronously; generated output URLs are hosted by dLazy.]

## Skill Version(s):

1.3.44 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
