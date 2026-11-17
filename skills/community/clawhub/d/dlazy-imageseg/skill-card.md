## Description:

Separates image foregrounds from backgrounds and returns a transparent-background image URL for product photos, portraits, and compositing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content creators can use the skill to remove an image background for product photos, portraits, and compositing. It sends the image to dLazy's hosted service and returns a transparent-background image URL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review notes that the documented login and authentication commands do not match the image-processing purpose, despite a benign verdict.

Mitigation: Review the CLI setup and confirm its authentication behavior before providing an API key.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/dlazyai/skills/dlazy-imageseg)
- [dLazy CLI package](https://www.npmjs.com/package/@dlazy/cli)
- [dLazy service](https://dlazy.com)
- [dLazy API key setup](https://dlazy.com/dashboard/organization/api-key)
- [CLI repository (listed in skill metadata)](https://github.com/dlazy-ai/cli)

## Skill Output:

**Output Type(s):** [Image, URL, JSON]

**Output Format:** [JSON containing the hosted URL and image metadata for the transparent-background result]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The result is hosted at files.dlazy.com; asynchronous mode can return a task ID before the image is ready.]

## Skill Version(s):

1.3.41 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
