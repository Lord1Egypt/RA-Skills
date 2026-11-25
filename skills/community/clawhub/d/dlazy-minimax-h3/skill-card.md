## Description:

MiniMax Hailuo omni-modal video model with native stereo audio, producing 5-15 second clips at up to 2K. Supports text-to-video, first/last frame transitions and multi-asset references for character and scene consistency.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators use this skill to request short MiniMax Hailuo video clips from text prompts or reference media, with controls for frames, assets, duration, aspect ratio, and resolution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan reports a mismatch between the advertised video-generation purpose and some CLI descriptions; the referenced local materials were missing, the external CLI package was not inspected, and scan coverage is incomplete.

Mitigation: Before installing, review the @dlazy/cli package and its installation details, and check whether the described login flow and 4K option match the intended use.

## Reference(s):

- [dLazy CLI repository (metadata link)](https://github.com/dlazy-ai/cli)
- [dLazy CLI package on npm](https://www.npmjs.com/package/@dlazy/cli)
- [dLazy website](https://dlazy.com)

## Skill Output:

**Output Type(s):** [Generated video assets, JSON result metadata, Generation status and result URLs]

**Output Format:** [JSON result with generated media URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [With asynchronous execution, a task ID may be returned before the generated asset is ready.]

## Skill Version(s):

1.2.41 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
