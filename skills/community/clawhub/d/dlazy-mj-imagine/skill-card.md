## Description:

Generates Midjourney-style images from prompts with configurable aspect ratio, bot type, and grid or upscaled output selection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use the skill to request artistic, strongly stylized images from an agent, selecting an aspect ratio, Midjourney or Niji Journey mode, and grid or individual upscale output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review notes that the documented image generation purpose does not fully explain reported login and authentication behavior, and that some package or local-path details were not fully resolved.

Mitigation: Review the skill purpose and pinned CLI installation requirements before installing; only provide prompts, files, and credentials you are comfortable sending to dLazy services.

Risk: The skill sends prompts to dLazy's hosted API and uploads supplied local media files to its media storage; the CLI requires a dLazy API key.

Mitigation: Use the skill only with prompts and media approved for that service, keep the API key in the user-level configuration or environment, and rotate or revoke it if needed.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/dlazyai/skills/dlazy-mj-imagine)
- [CLI repository listed in skill metadata](https://github.com/dlazy-ai/cli)
- [dLazy CLI package on npm](https://www.npmjs.com/package/@dlazy/cli)
- [dLazy website](https://dlazy.com)

## Skill Output:

**Output Type(s):** [Image files, JSON]

**Output Format:** [Generated image assets referenced by hosted URLs in a JSON response; asynchronous requests can return task status.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports configurable aspect ratio, Midjourney or Niji Journey mode, grid or U1–U4 output, and an optional local save path.]

## Skill Version(s):

1.3.40 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
