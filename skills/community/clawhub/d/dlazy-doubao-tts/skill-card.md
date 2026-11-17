## Description:

Synthesize text into natural and fluent speech using Doubao TTS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users can turn Chinese or English text into spoken audio, choosing from available voices and speech speeds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review found incomplete evidence for referenced package and command details and did not demonstrate how some CLI instructions relate to speech synthesis.

Mitigation: Review the CLI and package details and confirm they are needed before installing or using the skill.

Risk: Text submitted for synthesis is sent to dLazy-hosted services.

Mitigation: Avoid sending sensitive text unless its use with the service is approved.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/dlazyai/skills/dlazy-doubao-tts)
- [dLazy CLI repository listed in the skill metadata](https://github.com/dlazy-ai/cli)
- [dLazy CLI on npm](https://www.npmjs.com/package/@dlazy/cli)
- [dLazy](https://dlazy.com)

## Skill Output:

**Output Type(s):** [Audio, JSON]

**Output Format:** [Generated speech audio returned as a result URL or saved audio file, with result metadata in JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports Chinese and English voices with selectable voice and speed options.]

## Skill Version(s):

1.3.41 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
