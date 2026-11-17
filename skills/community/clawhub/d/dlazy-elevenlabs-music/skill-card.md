## Description:

Generates 10–300 seconds of original music from a natural-language prompt with the ElevenLabs music_v1 model.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can create original background music, advertising tracks, and short-video soundtracks from natural-language prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The reported command does not establish the declared music-generation capability, and scanner coverage is partial with medium confidence.

Mitigation: Check `dlazy elevenlabs-music -h` and confirm the returned result is the expected music asset before relying on it for music-generation tasks.

## Reference(s):

- [dLazy CLI repository (linked by the skill metadata)](https://github.com/dlazy-ai/cli)
- [@dlazy/cli on npm](https://www.npmjs.com/package/@dlazy/cli)
- [dLazy](https://dlazy.com)

## Skill Output:

**Output Type(s):** [Audio files, JSON]

**Output Format:** [Generated audio asset with a JSON result containing its URL and task details]

**Output Parameters:** [Natural-language prompt and duration (10–300 seconds)]

**Other Properties Related to Output:** [Can return an asynchronous task ID or save the generated audio to a local path.]

## Skill Version(s):

1.3.42 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
