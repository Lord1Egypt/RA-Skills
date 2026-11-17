## Description:

Fast version of ByteDance's Seedance 2.0. Generates videos faster with support for multi-modal references, first/last frame, and text-to-video.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and creators use this skill to generate short videos from text prompts and optional image, video, audio, or first/last-frame references.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports a purpose mismatch and incomplete scan coverage because some local references could not be resolved.

Mitigation: Review the skill commands and referenced material before use, especially if relying on video-generation behavior.

Risk: Local image, video, or audio inputs are uploaded to dLazy media storage for processing.

Mitigation: Only provide media you are permitted to share with the service.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/dlazyai/skills/dlazy-seedance-2-0-fast)
- [dLazy CLI package on npm](https://www.npmjs.com/package/@dlazy/cli)
- [dLazy service](https://dlazy.com)
- [CLI project information (listed in skill metadata)](https://github.com/dlazy-ai/cli)

## Skill Output:

**Output Type(s):** [Media files, JSON]

**Output Format:** [JSON result metadata with hosted media URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated media URLs; duration and resolution can be configured.]

## Skill Version(s):

1.3.40 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
