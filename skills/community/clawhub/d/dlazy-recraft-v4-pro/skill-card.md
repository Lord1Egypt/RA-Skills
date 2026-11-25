## Description:

Generates 4MP high-resolution raster images with Recraft V4 Pro for print-ready and large-format assets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creative professionals use the skill to create high-resolution raster image assets from text prompts for print and large-format projects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and local media paths provided to the CLI are sent to dLazy's hosted service, and generated assets are hosted there.

Mitigation: Avoid submitting sensitive prompts or files unless dLazy's service terms and data handling are acceptable.

Risk: Security review confidence is medium because scanner coverage was partial and some local references were unresolved.

Mitigation: Review the CLI and service behavior before configuring credentials or relying on unresolved references.

## Reference(s):

- [dLazy homepage](https://dlazy.com)
- [@dlazy/cli package on npm](https://www.npmjs.com/package/@dlazy/cli)
- [CLI project link listed in skill metadata](https://github.com/dlazy-ai/cli)
- [dLazy API key dashboard](https://dlazy.com/dashboard/organization/api-key)

## Skill Output:

**Output Type(s):** [JSON, Image files]

**Output Format:** [JSON generation response with hosted image URLs; optional saved raster image file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The response may include an asynchronous task ID; generated image assets are hosted by dLazy and can optionally be saved locally.]

## Skill Version(s):

1.3.44 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
