## Description:

Generates PixVerse C1 videos from text prompts, reference images, or first and last frames.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creative teams use the skill to generate videos with PixVerse C1 from text prompts, reference images, or first and last frames, then retrieve the generated media.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan verdict is benign with medium confidence and partial coverage; it flagged a mismatch between the stated video-generation purpose and a login command, plus whitespace padding.

Mitigation: Before installing, review the login behavior and the padded section of the Chinese guide, as recommended by the security guidance.

Risk: Prompts and local media provided to the skill are sent to dLazy-hosted services for processing.

Mitigation: Only submit prompts and media that are approved for processing by the hosted service.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/dlazyai/skills/dlazy-pixverse-c1)
- [dLazy CLI repository](https://github.com/dlazy-ai/cli)
- [dLazy CLI on npm](https://www.npmjs.com/package/@dlazy/cli)
- [dLazy website](https://dlazy.com)

## Skill Output:

**Output Type(s):** [Video, JSON]

**Output Format:** [Generated video media with JSON result metadata and a hosted media URL.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Accepts a text prompt and optional reference media; supports generation mode, resolution, aspect ratio, duration, and audio settings. Tasks may return asynchronously.]

## Skill Version(s):

1.2.42 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
