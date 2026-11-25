## Description:

ElevenLabs text-to-sound model — generates 1–22 second sound effects from a description for foley, ambience, alerts, and game SFX.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

Creative teams and agents use text descriptions to generate short sound effects for foley, ambience, alerts, and game audio.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review notes that the dLazy login step is not clearly connected to sound generation.

Mitigation: Before signing in, confirm you trust dLazy's authentication flow and review what will be stored in the local CLI configuration; use a revocable API key where possible.

## Reference(s):

- [dLazy CLI repository (metadata link)](https://github.com/dlazy-ai/cli)
- [dLazy CLI on npm](https://www.npmjs.com/package/@dlazy/cli)
- [dLazy homepage](https://dlazy.com)
- [ClawHub skill release](https://clawhub.ai/dlazyai/skills/dlazy-elevenlabs-sfx)

## Skill Output:

**Output Type(s):** [Audio files, JSON]

**Output Format:** [Generated sound effects delivered as audio assets with JSON task and result metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Sound effects are 1–22 seconds; generation can run asynchronously, and results can be saved to a local path.]

## Skill Version(s):

1.3.45 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
