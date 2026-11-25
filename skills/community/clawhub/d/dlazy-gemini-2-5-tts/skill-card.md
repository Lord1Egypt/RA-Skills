## Description:

Generate multilingual, highly natural audio using Gemini 2.5 text-to-speech.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content creators use this skill to turn prompts into multilingual spoken audio with Gemini 2.5 text-to-speech, selecting a supported language and voice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The reported `dlazy login` step is not clearly tied to the text-to-speech purpose, and its credential handling and the CLI package were not fully assessed.

Mitigation: Before installing or authenticating, confirm the login step is expected for this workflow and review the pinned CLI package and how it stores and uses API credentials.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/dlazyai/skills/dlazy-gemini-2-5-tts)
- [CLI project homepage (metadata link)](https://github.com/dlazy-ai/cli)
- [@dlazy/cli package](https://www.npmjs.com/package/@dlazy/cli)
- [dLazy service](https://dlazy.com)

## Skill Output:

**Output Type(s):** [Audio, JSON, Shell commands]

**Output Format:** [Hosted audio output referenced by URLs, with JSON result metadata; invoked through CLI commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports Mandarin and English voices; output URLs are hosted by dLazy.]

## Skill Version(s):

1.3.44 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
