## Description:

Synthesize text into natural and fluent speech using Doubao TTS. 使用豆包 (Doubao) TTS 文本转语音模型，将文字合成为自然流畅的语音播报。

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content creators use the skill to turn Chinese or English text into spoken audio with Doubao TTS, selecting a voice and speech speed. It requires a dLazy API key and sends prompts to dLazy's hosted service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review was partial and flagged an undeclared CLI login step and unverified install context.

Mitigation: Review the pinned CLI package and its login flow before installing it or entering an API key.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/dlazyai/skills/dlazy-doubao-tts)
- [dLazy CLI repository (listed in skill metadata)](https://github.com/dlazy-ai/cli)
- [dLazy CLI npm package](https://www.npmjs.com/package/@dlazy/cli)
- [dLazy service](https://dlazy.com)

## Skill Output:

**Output Type(s):** [Audio, Files]

**Output Format:** [Generated audio asset returned through a JSON result with a URL; optionally downloaded to a local file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Voice language, voice ID, and speech speed can be selected; asynchronous generation is available.]

## Skill Version(s):

1.3.44 (source: server-resolved release metadata; artifact frontmatter reports 1.3.4)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
