## Description:

Turns storyboard details into an ordered video-generation pipeline that can be added to a canvas.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creative teams use the skill to convert storyboard dialogue, visual prompts, aspect ratio, and resolution into a sequenced audio and video generation pipeline on a canvas.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment flags a mismatch between the storyboard purpose and authentication setup.

Mitigation: Review the authentication and installation instructions before installing or configuring the CLI.

Risk: The workflow sends prompts and supplied media to dLazy cloud services for generation, and may incur charges.

Mitigation: Review prompts and media before sending them, and confirm cloud processing and expected charges are acceptable.

Risk: The security assessment says coverage is incomplete because some local references could not be resolved.

Mitigation: Review the CLI and any unresolved references before using the skill.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/dlazyai/skills/dlazy-video-storyboard-generate)
- [dLazy website](https://dlazy.com)
- [dLazy CLI package on npm](https://www.npmjs.com/package/@dlazy/cli)
- [dLazy organization API key settings](https://dlazy.com/dashboard/organization/api-key)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [JSON pipeline with audio, image, and video generation steps, added to a canvas]

**Output Parameters:** [1D: one ordered pipeline, with length varying by storyboard count]

**Other Properties Related to Output:** [Original audio and scene image inputs are shared; cloned audio and generated video steps repeat for each storyboard.]

## Skill Version(s):

1.2.39 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
