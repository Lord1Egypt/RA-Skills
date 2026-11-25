## Description:

Text-to-image generation with Jimeng, quickly converting text to high-quality images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other users can submit text prompts, optionally with reference images, to create images with Jimeng through the dLazy service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan reports partial coverage and a mismatch between the advertised image-generation purpose and a login-only command; it found no confirmed harmful behavior.

Mitigation: Before installing or relying on the skill, review the dLazy CLI/package and confirm that the generation command behaves as expected.

Risk: The documentation says prompts are sent to dLazy and local reference images are uploaded to its media storage.

Mitigation: Only submit prompts and reference images that you are authorized to share with the service.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/dlazyai/skills/dlazy-jimeng-t2i)
- [dLazy CLI package on npm](https://www.npmjs.com/package/@dlazy/cli)
- [dLazy service](https://dlazy.com)
- [dLazy API key settings](https://dlazy.com/dashboard/organization/api-key)

## Skill Output:

**Output Type(s):** [Images, JSON]

**Output Format:** [JSON result envelope with generated image URLs and metadata; image files can be saved locally.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return a task identifier for asynchronous generation; reference images are optional inputs.]

## Skill Version(s):

1.3.44 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
