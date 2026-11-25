## Description:

ElevenLabs music_v1 generates 10–300 seconds of original music from a natural-language prompt.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and developers use the skill to generate original background music, advertising music, and short-video soundtracks from text prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports a mismatch between the music-generation purpose and observed dLazy login/authentication commands; the scan was partial.

Mitigation: Review the CLI authentication behavior and credential handling before providing an API key; treat the benign verdict as incomplete assurance.

## Reference(s):

- [CLI project listed in skill metadata](https://github.com/dlazy-ai/cli)
- [dLazy CLI on npm](https://www.npmjs.com/package/@dlazy/cli)
- [dLazy](https://dlazy.com)

## Skill Output:

**Output Type(s):** [Audio files, JSON, Shell commands, Configuration guidance]

**Output Format:** [JSON result with generated music asset URL; optionally a downloaded audio file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prompt-based music generation; duration can be set from 10 to 300 seconds.]

## Skill Version(s):

1.3.45 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
