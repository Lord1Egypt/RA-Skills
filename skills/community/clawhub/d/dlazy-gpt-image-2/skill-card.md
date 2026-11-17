## Description:

GPT Image 2 model for text-to-image and image editing. Supports generating images from text as well as editing and synthesizing images with reference inputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators use this skill to generate images from text prompts or edit and synthesize images with reference inputs through dLazy's hosted service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment reports an unexplained CLI login step and incomplete scan coverage because some local references could not be resolved.

Mitigation: Before installing, verify what the CLI login authorizes and that it is for the intended image service; review the CLI and service behavior before sending prompts or reference images.

## Reference(s):

- [dLazy](https://dlazy.com)
- [@dlazy/cli on npm](https://www.npmjs.com/package/@dlazy/cli)

## Skill Output:

**Output Type(s):** [Images, API Calls, JSON]

**Output Format:** [Image files (JPEG, PNG, or WebP) with JSON result metadata and hosted output URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can return an asynchronous task identifier; generated images can be saved to a local path.]

## Skill Version(s):

1.3.42 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
