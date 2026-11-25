## Description:

ElevenLabs eleven_v3 text-to-speech with 12 curated multilingual voices and stability, similarity, and style controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content creators use the skill to generate multilingual speech for dubbing, audiobooks, and character dialogue, with configurable voice and delivery controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review is partial: referenced paths were missing and the dLazy CLI package was not inspected.

Mitigation: Before installing, review the CLI package and confirm its authentication and ElevenLabs TTS behavior match the intended use.

Risk: The security guidance notes a purpose mismatch and a hidden-content concern in the Chinese-language file.

Mitigation: Compare the English and Chinese skill files and confirm the described purpose and authentication commands before use.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/dlazyai/skills/dlazy-elevenlabs-tts)
- [dLazy CLI project page](https://github.com/dlazy-ai/cli)
- [dLazy CLI package on npm](https://www.npmjs.com/package/@dlazy/cli)
- [dLazy](https://dlazy.com)

## Skill Output:

**Output Type(s):** [Audio, JSON]

**Output Format:** [JSON result envelope with hosted media URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Asynchronous generation may return a task ID before completion.]

## Skill Version(s):

1.3.45 (source: server-resolved release metadata; artifact frontmatter lists 1.3.4)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
