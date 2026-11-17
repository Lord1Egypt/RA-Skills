## Description:

Compose or edit a local Dawn song in TypeScript, check its score, and render audio or MIDI with an installed Dawn CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hraness](https://clawhub.ai/user/hraness)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to compose or revise a song in a local Dawn project, check the score, and render review audio or MIDI with an installed Dawn CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security analysis coverage was partial because some local references could not be resolved.

Mitigation: Review the unresolved local references and relevant project files before deciding whether to install or use the skill.

Risk: Song scores are executable TypeScript and may contain unfamiliar code.

Mitigation: Review unfamiliar source before running it, as the skill recommends.

## Reference(s):

- [Dawn install guide](https://dawnav.com/install)
- [Dawn agent guide](https://dawnav.com/docs/agents)
- [Dawn SDK guide](https://dawnav.com/docs/sdk)
- [Dawn CLI reference](https://dawnav.com/docs/cli)

## Skill Output:

**Output Type(s):** [TypeScript code, Shell commands, WAV audio files, MIDI files]

**Output Format:** [TypeScript song scores, shell commands, WAV audio, and MIDI]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Works with the local Dawn project and installed CLI; review rendering output by listening when audio playback is available.]

## Skill Version(s):

0.1.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
