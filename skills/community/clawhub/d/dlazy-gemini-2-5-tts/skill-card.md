## Description:

Generates multilingual speech audio from text using dLazy’s Gemini 2.5 text-to-speech command.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use the skill to turn text into spoken audio in Chinese or English and select a supported voice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment has medium confidence and was partial; it reports a mismatch between the stated TTS purpose and the command it observed, and did not assess the pinned CLI package.

Mitigation: Before installing, review the full skill and pinned CLI package source, and check that the observed `dlazy login` behavior matches your needs for text-to-speech.

## Reference(s):

- [dLazy service](https://dlazy.com)
- [dLazy CLI npm package](https://www.npmjs.com/package/@dlazy/cli)

## Skill Output:

**Output Type(s):** [Audio, API result metadata and output URLs]

**Output Format:** [Generated audio hosted at a result URL, with JSON status and output metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Voice language and voice are selectable; the documented languages are Chinese (cmn) and English (en).]

## Skill Version(s):

1.3.41 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
